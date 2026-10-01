"""Generate the public TSVALPHA schema-2 fixture with independent Python crypto.

This script is deliberately not part of normal CI. Install the exact wheels in
requirements.lock into an isolated directory, add that directory to PYTHONPATH,
and redirect stdout to inspect the generated JSON before updating the fixture.
"""

import hashlib
import json
import unicodedata

from argon2.low_level import Type, hash_secret_raw
from nacl.bindings import crypto_aead_xchacha20poly1305_ietf_encrypt


PASSWORD_DECOMPOSED = "TSVALPHA public e\u0301 🦀 password"
SALT = bytes.fromhex("00112233445566778899aabbccddeeff")
WRAP_NONCE = bytes.fromhex("000102030405060708090a0b0c0d0e0f1011121314151617")
PAYLOAD_NONCE = bytes.fromhex("18191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f")
DEK = bytes.fromhex("a0a1a2a3a4a5a6a7a8a9aaabacadaeafb0b1b2b3b4b5b6b7b8b9babbbcbdbebf")


def cbor_text(value: str) -> bytes:
    encoded = value.encode("utf-8")
    if len(encoded) < 24:
        return bytes([0x60 | len(encoded)]) + encoded
    if len(encoded) <= 255:
        return bytes([0x78, len(encoded)]) + encoded
    raise ValueError("fixture text unexpectedly long")


def generate() -> bytes:
    payload = b"\x84\x02" + cbor_text("public-tsvalpha-fixture") + cbor_text("en") + b"\x80"
    password = unicodedata.normalize("NFC", PASSWORD_DECOMPOSED).encode("utf-8")
    kek = hash_secret_raw(
        secret=password,
        salt=SALT,
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        type=Type.ID,
        version=19,
    )
    header = bytearray(140)
    header[0:8] = b"TSVALPHA"
    header[8:10] = (2).to_bytes(2, "little")
    header[10:12] = bytes([1, 1])
    header[12:16] = (65536).to_bytes(4, "little")
    header[16:20] = (3).to_bytes(4, "little")
    header[20:24] = (4).to_bytes(4, "little")
    header[24:40] = SALT
    header[40:64] = WRAP_NONCE
    header[64:88] = PAYLOAD_NONCE
    header[88:92] = (len(payload) + 16).to_bytes(4, "little")
    wrapped = crypto_aead_xchacha20poly1305_ietf_encrypt(
        DEK, bytes(header[:92]), WRAP_NONCE, kek
    )
    header[92:124] = wrapped[:32]
    header[124:140] = wrapped[32:]
    body = crypto_aead_xchacha20poly1305_ietf_encrypt(
        payload, bytes(header), PAYLOAD_NONCE, DEK
    )
    return bytes(header) + body


if __name__ == "__main__":
    image = generate()
    print(
        json.dumps(
            {
                "bytes": len(image),
                "sha256": hashlib.sha256(image).hexdigest(),
                "hex": image.hex(),
            },
            indent=2,
            sort_keys=True,
        )
    )
