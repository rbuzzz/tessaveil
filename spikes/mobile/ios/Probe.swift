import Foundation

// Import tessaveil_probe.h through the host target's bridging header.
// Source contract only; no Xcode target, linked archive or executed Swift build.
struct ProbeSummary {
    let status: UInt32
    let durationUs: UInt64
    let memoryBytes: UInt64

    var display: String {
        let memory = memoryBytes == UInt64.max ? "unmeasured" : String(memoryBytes)
        return "status=\(status); duration_us=\(durationUs); memory_bytes=\(memory)"
    }
}

enum SyntheticProbe {
    // Caller supplies Array(transientText.utf8), without applying normalization,
    // and immediately clears the secure UI. No password is a stored property.
    // This synchronous call belongs on a worker queue, never the main UI thread.
    static func open(fixture: Data, passwordUtf8: inout [UInt8]) -> ProbeSummary {
        defer {
            passwordUtf8.withUnsafeMutableBytes { buffer in
                buffer.initializeMemory(as: UInt8.self, repeating: 0)
            }
            passwordUtf8.removeAll(keepingCapacity: false)
        }
        guard fixture.count <= 4096, passwordUtf8.count <= 1024 else {
            return ProbeSummary(status: 13, durationUs: 0, memoryBytes: UInt64.max)
        }
        let vaultCount = fixture.count
        let passwordCount = passwordUtf8.count
        let result = fixture.withUnsafeBytes { image in
            passwordUtf8.withUnsafeBytes { input in
                tv_probe_open_vault(image.bindMemory(to: UInt8.self).baseAddress, vaultCount,
                                    input.bindMemory(to: UInt8.self).baseAddress, passwordCount)
            }
        }
        return ProbeSummary(status: result.status, durationUs: result.duration_us,
                            memoryBytes: result.memory_bytes)
    }
}
