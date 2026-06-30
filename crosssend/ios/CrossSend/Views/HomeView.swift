import PhotosUI
import SwiftUI
import UniformTypeIdentifiers

struct HomeView: View {
  @StateObject private var discovery = DiscoveryService()
  @StateObject private var transferClient = TransferClient()

  @State private var selectedDevice: RemoteDevice?
  @State private var selectedFiles: [FileToSend] = []
  @State private var showScanner = false
  @State private var showFilePicker = false
  @State private var showPhotoPicker = false
  @State private var photoPickerItems: [PhotosPickerItem] = []

  var body: some View {
    NavigationStack {
      List {
        Section {
          if let device = selectedDevice {
            VStack(alignment: .leading, spacing: 6) {
              Text(device.name)
                .font(.headline)
              Text("\(device.host):\(device.port)")
                .font(.subheadline.monospaced())
                .foregroundStyle(.secondary)
              Text("PIN \(device.pin)")
                .font(.subheadline.monospaced())
            }
          } else {
            Text("Select a nearby Android device or scan its QR code.")
              .foregroundStyle(.secondary)
          }

          if selectedDevice != nil {
            Button("Clear device", role: .destructive) {
              selectedDevice = nil
              selectedFiles = []
              transferClient.reset()
            }
          }
        } header: {
          Text("Android device")
        }

        Section {
          if discovery.isScanning && discovery.nearbyDevices.isEmpty {
            HStack(spacing: 12) {
              ProgressView()
              Text(discovery.statusMessage)
                .foregroundStyle(.secondary)
            }
          } else if discovery.nearbyDevices.isEmpty {
            Text(discovery.statusMessage)
              .foregroundStyle(.secondary)
          } else {
            ForEach(discovery.nearbyDevices) { device in
              NearbyDeviceRow(
                device: device,
                isSelected: selectedDevice?.id == device.remoteDevice?.id
              ) {
                selectNearbyDevice(device)
              }
            }
          }

          Button("Scan QR code") {
            showScanner = true
          }
        } header: {
          Text("Nearby devices")
        } footer: {
          Text("Both phones must be on the same Wi‑Fi. Start receive mode on Android first.")
        }

        Section("Files") {
          if selectedFiles.isEmpty {
            Text("No files selected")
              .foregroundStyle(.secondary)
          } else {
            ForEach(selectedFiles) { file in
              HStack {
                Text(file.name)
                Spacer()
                Text(byteCount(file.size))
                  .foregroundStyle(.secondary)
              }
            }
          }

          Button("Choose photos") {
            showPhotoPicker = true
          }
          .disabled(selectedDevice == nil)

          Button("Choose files") {
            showFilePicker = true
          }
          .disabled(selectedDevice == nil)
        }

        Section {
          Button {
            Task {
              guard let device = selectedDevice else { return }
              await transferClient.send(files: selectedFiles, to: device)
            }
          } label: {
            Label("Send to Android", systemImage: "arrow.up.circle.fill")
              .font(.headline)
          }
          .disabled(selectedDevice == nil || selectedFiles.isEmpty || isTransferring)
        }

        if case .failed(let message) = transferClient.progress.phase {
          Section("Error") {
            Text(message)
              .foregroundStyle(.red)
          }
        }

        if case .completed(let count) = transferClient.progress.phase {
          Section("Success") {
            Text("\(count) file(s) sent successfully.")
              .foregroundStyle(.green)
          }
        }
      }
      .navigationTitle("CrossSend")
      .onAppear {
        discovery.start()
      }
      .onDisappear {
        discovery.stop()
      }
      .sheet(isPresented: $showScanner) {
        QRScannerView { url in
          if let device = RemoteDevice.from(pairingURL: url) {
            selectedDevice = device
            discovery.addManualDevice(device)
          }
          showScanner = false
        }
      }
      .sheet(isPresented: $showFilePicker) {
        DocumentPicker { urls in
          Task {
            await loadDocuments(urls)
          }
        }
      }
      .photosPicker(
        isPresented: $showPhotoPicker,
        selection: $photoPickerItems,
        maxSelectionCount: 20,
        matching: .any(of: [.images, .videos])
      )
      .onChange(of: photoPickerItems) { _, items in
        Task {
          await loadPhotos(items)
        }
      }
      .overlay {
        if isTransferring {
          TransferOverlay(progress: transferClient.progress)
        }
      }
    }
  }

  private var isTransferring: Bool {
    switch transferClient.progress.phase {
    case .idle, .completed, .failed:
      return false
    default:
      return true
    }
  }

  private func selectNearbyDevice(_ device: DiscoveredDevice) {
    guard let remote = device.remoteDevice else { return }
    selectedDevice = remote
    transferClient.reset()
  }

  private func byteCount(_ value: Int64) -> String {
    ByteCountFormatter.string(fromByteCount: value, countStyle: .file)
  }

  private func loadPhotos(_ items: [PhotosPickerItem]) async {
    var loaded: [FileToSend] = []
    for item in items {
      if let data = try? await item.loadTransferable(type: Data.self) {
        let name = item.itemIdentifier ?? "photo-\(loaded.count + 1).jpg"
        let mime = item.supportedContentTypes.first?.preferredMIMEType ?? "image/jpeg"
        loaded.append(
          FileToSend(
            name: name,
            mimeType: mime,
            size: Int64(data.count),
            data: data
          )
        )
      }
    }
    selectedFiles = loaded
  }

  private func loadDocuments(_ urls: [URL]) async {
    var loaded: [FileToSend] = []
    for url in urls {
      guard url.startAccessingSecurityScopedResource() else { continue }
      defer { url.stopAccessingSecurityScopedResource() }
      if let data = try? Data(contentsOf: url) {
        let mime = UTType(filenameExtension: url.pathExtension)?.preferredMIMEType
          ?? "application/octet-stream"
        loaded.append(
          FileToSend(
            name: url.lastPathComponent,
            mimeType: mime,
            size: Int64(data.count),
            data: data
          )
        )
      }
    }
    selectedFiles = loaded
  }
}

private struct NearbyDeviceRow: View {
  let device: DiscoveredDevice
  let isSelected: Bool
  let onSelect: () -> Void

  var body: some View {
    Button(action: onSelect) {
      HStack {
        VStack(alignment: .leading, spacing: 4) {
          Text(device.displayName)
            .font(.headline)
            .foregroundStyle(.primary)
          if let host = device.host, let port = device.port {
            Text("\(host):\(port)")
              .font(.caption.monospaced())
              .foregroundStyle(.secondary)
          }
          statusText
        }
        Spacer()
        if isSelected {
          Image(systemName: "checkmark.circle.fill")
            .foregroundStyle(.blue)
        } else if device.state == .ready {
          Image(systemName: "chevron.right")
            .font(.caption)
            .foregroundStyle(.secondary)
        }
      }
    }
    .disabled(device.state != .ready)
  }

  @ViewBuilder
  private var statusText: some View {
    switch device.state {
    case .resolving:
      Text("Connecting…")
        .font(.caption)
        .foregroundStyle(.secondary)
    case .ready:
      if let pin = device.pin {
        Text("PIN \(pin)")
          .font(.caption.monospaced())
          .foregroundStyle(.secondary)
      }
    case .failed:
      Text("Use QR scan for this device")
        .font(.caption)
        .foregroundStyle(.orange)
    }
  }
}

struct TransferOverlay: View {
  let progress: TransferProgress

  var body: some View {
    ZStack {
      Color.black.opacity(0.35).ignoresSafeArea()
      VStack(spacing: 16) {
        ProgressView()
          .controlSize(.large)
        Text(message)
          .multilineTextAlignment(.center)
          .foregroundStyle(.white)
          .padding(.horizontal)
      }
      .padding(24)
      .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 20))
      .padding()
    }
  }

  private var message: String {
    switch progress.phase {
    case .offering:
      return "Preparing transfer…"
    case .uploading(let current, let total, let fileName):
      return "Sending \(fileName)\n\(current) of \(total)"
    case .completing:
      return "Finishing up…"
    default:
      return "Transferring…"
    }
  }
}
