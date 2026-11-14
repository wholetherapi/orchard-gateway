"""Upstream pool selection for orchard-gateway."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Pool:
    name: str
    endpoint: str
    weight: int


POOLS = (
    Pool("orchard-pool-a", "https://orchard-pool-a.internal", 3),
    Pool("orchard-pool-b", "https://orchard-pool-b.internal", 1),
)


def choose_pool(partner: str, path: str) -> Pool:
    """Deterministic weighted selection keyed by partner and path."""
    digest = sum(ord(ch) for ch in f"{partner}:{path}")
    total = sum(pool.weight for pool in POOLS)
    slot = digest % total
    for pool in POOLS:
        if slot < pool.weight:
            return pool
        slot -= pool.weight
    return POOLS[0]
