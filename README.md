# orchard-gateway

Payment edge gateway for the orchard payment fabric.

**Status:** Released - v3.4.1 (generally available on the internal registry).

`orchard-gateway` terminates partner traffic at the payment edge, validates
request signatures, applies per-partner rate limits, and forwards each request
to the appropriate orchard payment pool. The service is deployed as a
stateless Deployment and is configured exclusively through environment
variables (`APP_MODE`, `UPSTREAM_POOL`).

## Layout

- `src/gateway.py` - signature validation and request routing
- `src/pools.py` - upstream pool selection and health scoring
- `pyproject.toml` - build metadata

## Running locally

```
python -m orchard_gateway.gateway --listen :8080
```
