import Foundation

enum TransferError: LocalizedError {
  case invalidResponse
  case offerRejected
  case uploadFailed(String)
  case network(Error)

  var errorDescription: String? {
    switch self {
    case .invalidResponse:
      return "The Android device returned an unexpected response."
    case .offerRejected:
      return "The PIN did not match. Scan the QR code again."
    case .uploadFailed(let message):
      return message
    case .network(let error):
      return error.localizedDescription
    }
  }
}

@MainActor
final class TransferClient: ObservableObject {
  @Published var progress = TransferProgress()

  private let encoder: JSONEncoder = {
    let encoder = JSONEncoder()
    return encoder
  }()

  private let decoder: JSONDecoder = {
    let decoder = JSONDecoder()
    return decoder
  }()

  func verify(device: RemoteDevice) async throws -> DeviceInfoResponse {
    let url = device.baseURL.appendingPathComponent("v1/info")
    var request = URLRequest(url: url)
    request.httpMethod = "GET"
    request.timeoutInterval = 10

    let (data, response) = try await URLSession.shared.data(for: request)
    guard let http = response as? HTTPURLResponse, http.statusCode == 200 else {
      throw TransferError.invalidResponse
    }
    return try decoder.decode(DeviceInfoResponse.self, from: data)
  }

  func send(files: [FileToSend], to device: RemoteDevice) async {
    progress.phase = .offering

    do {
      let offer = OfferRequest(
        pin: device.pin,
        files: files.map { FileOfferItem(name: $0.name, size: $0.size, mime: $0.mimeType) }
      )

      let offerURL = device.baseURL.appendingPathComponent("v1/offer")
      var offerRequest = URLRequest(url: offerURL)
      offerRequest.httpMethod = "POST"
      offerRequest.setValue("application/json", forHTTPHeaderField: "Content-Type")
      offerRequest.httpBody = try encoder.encode(offer)

      let (offerData, offerResponse) = try await URLSession.shared.data(for: offerRequest)
      guard let offerHttp = offerResponse as? HTTPURLResponse else {
        throw TransferError.invalidResponse
      }

      if offerHttp.statusCode == 403 {
        throw TransferError.offerRejected
      }

      guard offerHttp.statusCode == 200 else {
        throw TransferError.invalidResponse
      }

      let offerResult = try decoder.decode(OfferResponse.self, from: offerData)
      guard offerResult.accepted else {
        throw TransferError.offerRejected
      }

      for (index, file) in files.enumerated() {
        progress.phase = .uploading(
          current: index + 1,
          total: files.count,
          fileName: file.name
        )

        try await upload(
          file: file,
          index: index,
          sessionId: offerResult.sessionId,
          device: device
        )
      }

      progress.phase = .completing
      try await complete(sessionId: offerResult.sessionId, device: device)
      progress.phase = .completed(fileCount: files.count)
    } catch let error as TransferError {
      progress.phase = .failed(message: error.localizedDescription)
    } catch {
      progress.phase = .failed(message: error.localizedDescription)
    }
  }

  func reset() {
    progress = TransferProgress()
  }

  private func upload(file: FileToSend, index: Int, sessionId: String, device: RemoteDevice) async throws {
    let url = device.baseURL
      .appendingPathComponent("v1/upload")
      .appendingPathComponent(sessionId)
      .appendingPathComponent(String(index))

    var request = URLRequest(url: url)
    request.httpMethod = "PUT"
    request.setValue("application/octet-stream", forHTTPHeaderField: "Content-Type")
    request.setValue(
      Data(file.name.utf8).base64EncodedString(),
      forHTTPHeaderField: "X-File-Name"
    )
    request.setValue(file.mimeType, forHTTPHeaderField: "X-File-Mime")
    request.setValue(String(file.size), forHTTPHeaderField: "X-File-Size")
    request.setValue(String(index), forHTTPHeaderField: "X-File-Index")
    request.httpBody = file.data

    let (data, response) = try await URLSession.shared.data(for: request)
    guard let http = response as? HTTPURLResponse, http.statusCode == 200 else {
      let body = String(data: data, encoding: .utf8) ?? "Upload failed"
      throw TransferError.uploadFailed(body)
    }
  }

  private func complete(sessionId: String, device: RemoteDevice) async throws {
    let url = device.baseURL
      .appendingPathComponent("v1/complete")
      .appendingPathComponent(sessionId)

    var request = URLRequest(url: url)
    request.httpMethod = "POST"

    let (data, response) = try await URLSession.shared.data(for: request)
    guard let http = response as? HTTPURLResponse, http.statusCode == 200 else {
      throw TransferError.invalidResponse
    }
    _ = try decoder.decode(CompleteResponse.self, from: data)
  }
}
