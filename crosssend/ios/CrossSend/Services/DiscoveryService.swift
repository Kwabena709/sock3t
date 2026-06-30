import Foundation
import Network

struct DiscoveredDevice: Identifiable, Equatable {
  enum State: Equatable {
    case resolving
    case ready
    case failed
  }

  let serviceName: String
  var displayName: String
  var host: String?
  var port: Int?
  var pin: String?
  var state: State

  var id: String { serviceName }

  var remoteDevice: RemoteDevice? {
    guard state == .ready,
      let host,
      let port,
      let pin
    else {
      return nil
    }
    return RemoteDevice(
      id: "\(host):\(port)",
      name: displayName,
      host: host,
      port: port,
      pin: pin
    )
  }
}

@MainActor
final class DiscoveryService: ObservableObject {
  @Published var nearbyDevices: [DiscoveredDevice] = []
  @Published var isScanning = false
  @Published var statusMessage = "Searching for Android devices on Wi‑Fi…"

  private var browser: NWBrowser?
  private var resolveTasks: [String: Task<Void, Never>] = [:]
  private var visibleServiceNames = Set<String>()

  func start() {
    stop()

    let parameters = NWParameters.tcp
    parameters.includePeerToPeer = true

    let descriptor = NWBrowser.Descriptor.bonjour(type: "_crosssend._tcp", domain: nil)
    let browser = NWBrowser(for: descriptor, using: parameters)

    browser.stateUpdateHandler = { [weak self] state in
      Task { @MainActor in
        self?.handleBrowserState(state)
      }
    }

    browser.browseResultsChangedHandler = { [weak self] results, _ in
      Task { @MainActor in
        self?.handleResults(results)
      }
    }

    browser.start(queue: .main)
    self.browser = browser
    isScanning = true
    statusMessage = "Searching for Android devices on Wi‑Fi…"
  }

  func stop() {
    browser?.cancel()
    browser = nil
    resolveTasks.values.forEach { $0.cancel() }
    resolveTasks.removeAll()
    visibleServiceNames.removeAll()
    nearbyDevices.removeAll()
    isScanning = false
    statusMessage = "Discovery stopped"
  }

  func addManualDevice(_ device: RemoteDevice) {
    let discovered = DiscoveredDevice(
      serviceName: "manual-\(device.id)",
      displayName: device.name,
      host: device.host,
      port: device.port,
      pin: device.pin,
      state: .ready
    )
    upsert(discovered)
  }

  private func handleBrowserState(_ state: NWBrowser.State) {
    switch state {
    case .ready:
      isScanning = true
      statusMessage = "Searching for Android devices on Wi‑Fi…"
    case .failed:
      isScanning = false
      statusMessage = "Discovery unavailable. Use QR scan instead."
    case .cancelled:
      isScanning = false
    default:
      break
    }
  }

  private func handleResults(_ results: Set<NWBrowser.Result>) {
    let serviceResults = results.compactMap { result -> (String, NWBrowser.Result)? in
      guard case .service(let name, _, _, _) = result.endpoint else { return nil }
      return (name, result)
    }

    let names = Set(serviceResults.map(\.0))
    visibleServiceNames = names

    nearbyDevices.removeAll { !names.contains($0.serviceName) && !$0.serviceName.hasPrefix("manual-") }
    resolveTasks = resolveTasks.filter { names.contains($0.key) }

    for (name, result) in serviceResults {
      if nearbyDevices.contains(where: { $0.serviceName == name && $0.state == .ready }) {
        continue
      }
      if resolveTasks[name] != nil {
        continue
      }

      if !nearbyDevices.contains(where: { $0.serviceName == name }) {
        upsert(
          DiscoveredDevice(
            serviceName: name,
            displayName: txtValue("name", in: result) ?? name,
            host: txtValue("host", in: result),
            port: nil,
            pin: txtValue("pin", in: result),
            state: .resolving
          )
        )
      }

      resolveTasks[name] = Task { [weak self] in
        await self?.resolve(result: result, serviceName: name)
      }
    }

    if names.isEmpty {
      statusMessage = "No Android devices found. Start receive mode on Android or scan QR."
    } else {
      statusMessage = "Found \(names.count) device(s) nearby"
    }
  }

  private func resolve(result: NWBrowser.Result, serviceName: String) async {
    let txtName = txtValue("name", in: result)
    let txtPin = txtValue("pin", in: result)
    let txtHost = txtValue("host", in: result)

    do {
      let resolved = try await EndpointResolver.resolve(endpoint: result.endpoint)
      let host = txtHost ?? resolved.host
      let device = DiscoveredDevice(
        serviceName: serviceName,
        displayName: txtName ?? serviceName,
        host: host,
        port: resolved.port,
        pin: txtPin,
        state: txtPin == nil ? .failed : .ready
      )
      upsert(device)

      if txtPin == nil {
        statusMessage = "\(device.displayName) found — scan QR for PIN"
      }
    } catch {
      upsert(
        DiscoveredDevice(
          serviceName: serviceName,
          displayName: txtName ?? serviceName,
          host: txtHost,
          port: nil,
          pin: txtPin,
          state: .failed
        )
      )
    }

    resolveTasks[serviceName] = nil
  }

  private func txtValue(_ key: String, in result: NWBrowser.Result) -> String? {
    guard case .bonjour(let record) = result.metadata else { return nil }
    return record[key]
  }

  private func upsert(_ device: DiscoveredDevice) {
    if let index = nearbyDevices.firstIndex(where: { $0.serviceName == device.serviceName }) {
      nearbyDevices[index] = device
    } else {
      nearbyDevices.append(device)
    }
    nearbyDevices.sort { $0.displayName.localizedCaseInsensitiveCompare($1.displayName) == .orderedAscending }
  }
}

private enum EndpointResolver {
  enum ResolveError: Error {
    case missingEndpoint
  }

  static func resolve(endpoint: NWEndpoint) async throws -> (host: String, port: Int) {
    try await withCheckedThrowingContinuation { continuation in
      let connection = NWConnection(to: endpoint, using: .tcp)
      var finished = false

      connection.stateUpdateHandler = { state in
        switch state {
        case .ready:
          guard !finished else { return }
          finished = true
          defer { connection.cancel() }

          guard let remote = connection.currentPath?.remoteEndpoint,
            case .hostPort(let host, let port) = remote
          else {
            continuation.resume(throwing: ResolveError.missingEndpoint)
            return
          }

          continuation.resume(returning: (cleanHost(host), Int(port.rawValue)))
        case .failed(let error):
          guard !finished else { return }
          finished = true
          connection.cancel()
          continuation.resume(throwing: error)
        default:
          break
        }
      }

      connection.start(queue: .global(qos: .userInitiated))
    }
  }

  private static func cleanHost(_ host: NWEndpoint.Host) -> String {
    let raw = "\(host)"
    if raw.hasPrefix("::ffff:") {
      return String(raw.dropFirst("::ffff:".count))
    }
    return raw
  }
}
