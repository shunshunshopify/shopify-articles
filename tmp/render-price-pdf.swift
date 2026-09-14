import Foundation
import AppKit
import PDFKit

let input = URL(fileURLWithPath: CommandLine.arguments[1])
let output = URL(fileURLWithPath: CommandLine.arguments[2], isDirectory: true)
try FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)
guard let document = PDFDocument(url: input) else { fatalError("PDF open failed") }
print("Pages: \(document.pageCount)")
for index in 0..<document.pageCount {
    guard let page = document.page(at: index) else { continue }
    let box = page.bounds(for: .mediaBox)
    let scale: CGFloat = 1.5
    let width = Int(box.width * scale)
    let height = Int(box.height * scale)
    guard let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: width, pixelsHigh: height, bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0), let context = NSGraphicsContext(bitmapImageRep: bitmap) else { fatalError("Bitmap failed") }
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = context
    context.cgContext.setFillColor(NSColor.white.cgColor)
    context.cgContext.fill(CGRect(x: 0, y: 0, width: width, height: height))
    context.cgContext.scaleBy(x: scale, y: scale)
    page.draw(with: .mediaBox, to: context.cgContext)
    NSGraphicsContext.restoreGraphicsState()
    if let png = bitmap.representation(using: .png, properties: [:]) {
        try png.write(to: output.appendingPathComponent("page-\(index + 1).png"))
    }
    try (page.string ?? "").write(to: output.appendingPathComponent("page-\(index + 1).txt"), atomically: true, encoding: .utf8)
}
