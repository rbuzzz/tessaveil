#include <jni.h>
#include "../include/tessaveil_probe.h"

static void clear_bytes(uint8_t *bytes, size_t length) {
    volatile uint8_t *p = bytes;
    while (length--) *p++ = 0;
}

JNIEXPORT jlongArray JNICALL Java_org_tessaveil_spike_Probe_openNative(
        JNIEnv *env, jobject self, jbyteArray vault, jint vault_len,
        jbyteArray password, jint password_len) {
    (void)self;
    TvProbeResult result = {13, 0, 0, UINT64_MAX};
    uint8_t image[4096];
    uint8_t input[1024];
    /* GetByteArrayRegion preserves standard UTF-8 and embedded NUL; never use
       GetStringUTFChars (JNI modified UTF-8) or strlen. */
    if (vault && password && vault_len >= 0 && vault_len <= 4096 &&
        password_len >= 0 && password_len <= 1024 &&
        (*env)->GetArrayLength(env, vault) == vault_len &&
        (*env)->GetArrayLength(env, password) == password_len) {
        (*env)->GetByteArrayRegion(env, vault, 0, vault_len, (jbyte *)image);
        if (!(*env)->ExceptionCheck(env)) {
            (*env)->GetByteArrayRegion(env, password, 0, password_len, (jbyte *)input);
            if (!(*env)->ExceptionCheck(env)) {
                result = tv_probe_open_vault(image, (size_t)vault_len, input, (size_t)password_len);
            }
        }
    }
    clear_bytes(input, sizeof input);
    clear_bytes(image, sizeof image);
    if ((*env)->ExceptionCheck(env)) return NULL;
    jlong values[3] = {(jlong)result.status, (jlong)result.duration_us,
                      result.memory_bytes == UINT64_MAX ? -1 : (jlong)result.memory_bytes};
    jlongArray output = (*env)->NewLongArray(env, 3);
    if (output) (*env)->SetLongArrayRegion(env, output, 0, 3, values);
    return output;
}
