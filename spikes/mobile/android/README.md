# Android source contract — BLOCKED

`Probe.kt` and `probe_jni.c` define the disposable adapter. They are not a Gradle
project, APK, running UI or verified JNI linkage. Android SDK/NDK, Java/Gradle,
Rust and both physical target classes are unavailable in the inspected environment.

When provisioned, create a disposable arm64 Android host with a masked transient
input; compile the C shim against the NDK and statically link Rust's
`aarch64-linux-android` archive into `libtessaveil_probe_jni.so`. Record and pin
JDK/Gradle/AGP/NDK/SDK/compiler versions and lock dependencies before building.
Package the independently verified `../vectors/synthetic-vault-v0.bin` unchanged
as an asset, with its exact hash. Run the synchronous probe on a worker thread,
clear the input UI immediately, and show only `Summary.display()`.

The input is a consumed `CharArray`, strictly encoded to standard UTF-8 and passed
with its exact byte length. Invalid UTF-16 is rejected by the encoder. Embedded
NUL reaches Rust intact and is rejected there. No native NFC, preferences, saved
instance state, log, clipboard, secret return value or password storage is allowed.
JNI deliberately uses byte arrays rather than JNI modified-UTF-8 string APIs.
Mutable buffers are cleared best-effort; managed/IME/OS copies cannot be guaranteed
erased. The adapter itself does not implement a secure UI or lifecycle protections.

Replay every shared normalization case through the completed adapter in an
instrumentation test against the Rust boundary. No normalization bytes should be
shown or logged in the UI. Capture process peak-memory with Android profiling,
wall-time, OOM/failure, OS/model/architecture/RAM and thermal observations on each
required physical class. `memoryBytes == -1` explicitly means unmeasured; neither
Argon2's requested 64 MiB nor heap deltas are peak-memory evidence. No emulator or
CI runner can clear the physical gate.
