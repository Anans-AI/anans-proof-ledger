# ANANS Proof Ledger

This repository contains **sterile, offline-verifiable evidence bundles**.

Each bundle is cryptographically sealed: a manifest records the SHA-256 hash
of every evidence file, and the manifest itself is signed with an Ed25519 key
whose public half ships as `enforcement.pub` inside the bundle.

## How to Verify a Bundle

```
cd proofs/<proof-id>/<version>/EVIDENCE
pip install pynacl          # one-time dependency
python VERIFY.py --evidence_dir .
```

Expected output: `VERIFY PASS`

Any other output is a hard failure. See the per-proof `VERIFY.md` for the
full failure-mode table and tamper-resistance tests.

## Repository Layout

```
proofs/
  <proof-id>/
    <version>/
      EVIDENCE/
        manifest.json       # canonical file-hash index + metadata
        manifest.sig        # Ed25519 signature over manifest.json bytes
        enforcement.pub     # verifying public key (no private key in repo)
        VERIFY.py           # self-contained verifier (no internet required)
        <evidence files>
      VERIFY.md             # human-readable verification guide
```

## Available Proofs

| Proof | Version | Description |
|---|---|---|
| `nist-ma12` | `v0.1.0-audit` | NIST SP 800-53 MA-12 maintenance discipline evidence |

## Guarantee

This repo publishes evidence bundles and portable verifiers only.
No proprietary source code or private keys are included.

A signed manifest that does not match the committed files is treated as a
hard stop — equivalent to tampering — and must not be released.
