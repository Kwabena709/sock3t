import AVFoundation
import SwiftUI

struct QRScannerView: UIViewControllerRepresentable {
  let onScan: (URL) -> Void

  func makeUIViewController(context: Context) -> ScannerViewController {
    let controller = ScannerViewController()
    controller.onScan = onScan
    return controller
  }

  func updateUIViewController(_ uiViewController: ScannerViewController, context: Context) {}
}

final class ScannerViewController: UIViewController, AVCaptureMetadataOutputObjectsDelegate {
  var onScan: ((URL) -> Void)?

  private let session = AVCaptureSession()

  override func viewDidLoad() {
    super.viewDidLoad()
    view.backgroundColor = .black
    configureCamera()
  }

  override func viewDidLayoutSubviews() {
    super.viewDidLayoutSubviews()
    view.layer.sublayers?
      .compactMap { $0 as? AVCaptureVideoPreviewLayer }
      .forEach { $0.frame = view.bounds }
  }

  private func configureCamera() {
    guard let device = AVCaptureDevice.default(for: .video),
      let input = try? AVCaptureDeviceInput(device: device)
    else {
      return
    }

    if session.canAddInput(input) {
      session.addInput(input)
    }

    let output = AVCaptureMetadataOutput()
    if session.canAddOutput(output) {
      session.addOutput(output)
      output.setMetadataObjectsDelegate(self, queue: .main)
      output.metadataObjectTypes = [.qr]
    }

    let preview = AVCaptureVideoPreviewLayer(session: session)
    preview.videoGravity = .resizeAspectFill
    view.layer.addSublayer(preview)

    DispatchQueue.global(qos: .userInitiated).async {
      self.session.startRunning()
    }
  }

  func metadataOutput(
    _ output: AVCaptureMetadataOutput,
    didOutput metadataObjects: [AVMetadataObject],
    from connection: AVCaptureConnection
  ) {
    guard let object = metadataObjects.first as? AVMetadataMachineReadableCodeObject,
      let value = object.stringValue,
      let url = URL(string: value)
    else {
      return
    }

    session.stopRunning()
    onScan?(url)
  }
}
