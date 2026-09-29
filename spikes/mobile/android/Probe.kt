package org.tessaveil.spike

import java.nio.CharBuffer
import java.nio.charset.CodingErrorAction

/** Source contract, not an Android app or a verified build. Caller owns secure UI. */
object Probe {
    init { System.loadLibrary("tessaveil_probe_jni") }

    private external fun openNative(vault: ByteArray, vaultLength: Int,
                                    password: ByteArray, passwordLength: Int): LongArray

    data class Summary(val status: Long, val durationUs: Long, val memoryBytes: Long) {
        fun display(): String = "status=$status; duration_us=$durationUs; memory_bytes=" +
            if (memoryBytes < 0) "unmeasured" else memoryBytes.toString()
    }

    /** Consumes and clears caller's transient characters, including on failure.
     * Run off the UI thread. Never persist, log or attach the argument to UI state.
     * Charset encoding only: Rust performs NFC and rejects NUL with its full length.
     */
    fun openSyntheticFixture(fixture: ByteArray, password: CharArray): Summary {
        var encoded: java.nio.ByteBuffer? = null
        var bytes = ByteArray(0)
        try {
            if (fixture.size > 4096 || password.size > 1024) return Summary(13, 0, -1)
            encoded = Charsets.UTF_8.newEncoder()
                .onMalformedInput(CodingErrorAction.REPORT)
                .onUnmappableCharacter(CodingErrorAction.REPORT)
                .encode(CharBuffer.wrap(password))
            bytes = ByteArray(encoded.remaining())
            encoded.get(bytes)
            val result = openNative(fixture, fixture.size, bytes, bytes.size)
            return Summary(result[0], result[1], result[2])
        } catch (_: java.nio.charset.CharacterCodingException) {
            return Summary(6, 0, -1)
        } finally {
            bytes.fill(0)
            if (encoded?.hasArray() == true) encoded.array().fill(0)
            password.fill('\u0000')
        }
    }
}
