#ifndef TESSAVEIL_PROBE_H
#define TESSAVEIL_PROBE_H
#include <stddef.h>
#include <stdint.h>

/* Source ABI contract; no generated bindings or platform compilation verified. */
typedef struct {
    uint32_t status;
    uint32_t reserved;
    uint64_t duration_us;
    uint64_t memory_bytes; /* UINT64_MAX means unmeasured, never zero peak memory. */
} TvProbeResult;

/* Read-only buffers, explicit byte lengths; no C-string scanning or normalization.
 * Buffers must remain readable and unchanged for the synchronous call. */
TvProbeResult tv_probe_open_vault(const uint8_t *vault, size_t vault_len,
                                const uint8_t *password_utf8, size_t password_len);
#endif
