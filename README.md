# Proof Ledger

**Maintainer:** Garth Noel
**Organisation:** [Anans-AI](https://github.com/Anans-AI)

This repository contains sterile, offline-verifiable evidence bundles produced
by the Anans governance system. Each bundle is cryptographically sealed and
ships with a self-contained verifier — no internet access required.

## How to Verify

```
cd proofs/<proof-id>/<version>/EVIDENCE
pip install pynacl          # one-time dependency
python VERIFY.py --evidence_dir .
```

Expected output: `VERIFY PASS`

Any other output is a hard failure. See the per-proof `VERIFY.md` for the
full failure-mode table and tamper-resistance tests.

## How It Works

Each bundle contains:

- `manifest.json` — canonical SHA-256 index of every evidence file
- `manifest.sig` — Ed25519 signature over `manifest.json` bytes
- `enforcement.pub` — verifying public key (no private key in repo)
- `VERIFY.py` — self-contained verifier (stdlib + pynacl only)

The verifier is fail-closed: any signature or hash mismatch exits non-zero
with a `FAIL_CLOSED:` message. There is no partial-pass state.

## Repository Layout

```
proofs/
  <proof-id>/
    <version>/
      EVIDENCE/
        manifest.json
        manifest.sig
        enforcement.pub
        VERIFY.py
        <evidence files>
      VERIFY.md
```

## Available Proofs

| Proof | Version | Description |
|---|---|---|
| `nist-ma12` | `v0.1.0-audit` | NIST SP 800-53 MA-12 maintenance discipline evidence |

## Guarantee

This repository publishes evidence bundles and portable verifiers only.
No proprietary source code or private keys are included.

A signed manifest that does not match the committed files is treated as a
hard stop — equivalent to tampering — and will not be released.
