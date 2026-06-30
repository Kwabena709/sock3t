import Foundation
import Network

@MainActor
final class DiscoveryService: ObservableObject {
  @Published var devices: [RemoteDevice] = []

  private var browser: NWBrowser?
  private var discoveredEndpoints: [String: NWEndpoint] = [:]

  func start() {
    stop()

    let parameters = NWParameters.tcp
    parameters.includePeerToPeer = true

    let descriptor = NWBrowser.Descriptor.bonjour(type: "_crosssend._tcp", domain: nil)
    let browser = NWBrowser(for: descriptor, using: parameters)

    browser.stateUpdateHandler = { state in
      if case .failed(let error) = state {
        print("Discovery failed: \(error)")
      }
    }

    browser.browseResultsChangedHandler = { [weak self] results, _ in
      Task { @MainActor in
        self?.handleResults(results)
      }
    }

    browser.start(queue: .main)
    self.browser = browser
  }

  func stop() {
    browser?.cancel()
    browser = nil
    discoveredEndpoints.removeAll()
    devices.removeAll()
  }

  private func handleResults(_ results: Set<NWBrowser.Result>) {
  }

  func addManualDevice(_ device: RemoteDevice) {
    if !devices.contains(where: { $0.id == device.id }) {
      devices.append(device)
    }
  }
}
