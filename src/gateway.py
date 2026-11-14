"""orchard-gateway: payment edge request handling."""

from __future__ import annotations

import hashlib
import hmac

from .pools import choose_pool

SIGNATURE_HEADER = "x-orchard-signature"
MAX_BODY_BYTES = 1_048_576


class RequestRejected(Exception):
    """Raised when partner traffic fails validation."""


def verify_signature(body: bytes, signature: str, secret: str) -> None:
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature or ""):
        raise RequestRejected("invalid request signature")


def handle(partner: str, path: str, body: bytes, signature: str, secret: str) -> dict:
    if len(body) > MAX_BODY_BYTES:
        raise RequestRejected("request body too large")
    verify_signature(body, signature, secret)
    pool = choose_pool(partner, path)
    return {"partner": partner, "path": path, "pool": pool.name, "bytes": len(body)}
