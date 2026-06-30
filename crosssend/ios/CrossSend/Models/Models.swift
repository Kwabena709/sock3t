import Foundation

struct RemoteDevice: Identifiable, Equatable {
  let id: String
  let name: String
  let host: String
  let port: Int
  let pin: String

  var baseURL: URL {
    URL(string: "http://\(host):\(port)")!
  }

  static func from(pairingURL: URL) -> RemoteDevice? {
    guard pairingURL.scheme == "crosssend",
      pairingURL.host == "v1",
      let components = URLComponents(url: pairingURL, resolvingAgainstBaseURL: false),
      let queryItems = components.queryItems
    else {
      return nil
    }

    func value(_ name: String) -> String? {
      queryItems.first(where: { $0.name == name })?.value
    }

    guard let host = value("h"),
      let portString = value("p"),
      let port = Int(portString),
      let pin = value("pin")
    else {
      return nil
    }

    let name = value("n")?.removingPercentEncoding ?? "Android device"
    return RemoteDevice(
      id: "\(host):\(port)",
      name: name,
      host: host,
      port: port,
      pin: pin
    )
  }
}

struct FileToSend: Identifiable, Equatable {
  let id = UUID()
  let name: String
  let mimeType: String
  let size: Int64
  let data: Data
}

struct TransferProgress: Equatable {
  enum Phase: Equatable {
    case idle
    case offering
    case uploading(current: Int, total: Int, fileName: String)
    case completing
    case completed(fileCount: Int)
    case failed(message: String)
  }

  var phase: Phase = .idle
}

struct DeviceInfoResponse: Codable {
  let name: String
  let version: String
  let protocolVersion: Int

  enum CodingKeys: String, CodingKey {
    case name
    case version
    case protocolVersion = "protocol"
  }
}

struct FileOfferItem: Codable {
  let name: String
  let size: Int64
  let mime: String
}

struct OfferRequest: Codable {
  let pin: String
  let files: [FileOfferItem]
}

struct OfferResponse: Codable {
  let sessionId: String
  let accepted: Bool
}

struct UploadResponse: Codable {
  let received: Int64
  let savedAs: String
}

struct CompleteResponse: Codable {
  let ok: Bool
  let filesReceived: Int
}
