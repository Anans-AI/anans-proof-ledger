# Offline Verification Governance Bundles

Maintainer: **Garth Noel**

This repository publishes **sterile, offline-verifiable evidence bundles** and
portable verifiers only. It is a standalone proof container for **fail-closed**
verification of signed manifests and evidence hashes.

## What this repository is

- Verified evidence artifacts from bounded runs (JSON payloads + portable verifier).
- Designed for offline falsification: you can validate integrity without trusting
  claims or infrastructure.

## What this repository is not

- Not a blockchain ledger or transparency log.
- Not OS-level containment.
- Not blanket regulatory compliance.
- Not a live governance platform or runtime agent framework.

## How to verify (cold)

1. Download a proof bundle (zip asset or proof folder).
2. Unzip into an empty directory.
3. From inside the extracted directory, run:

```
python VERIFY.py --evidence_dir .
```

Expected output: `VERIFY PASS`

## Falsifiability

- Flip a single byte in any evidence file and rerun VERIFY. It must **FAIL_CLOSED**.
- Flip a single byte in `manifest.json` and rerun VERIFY. Signature verification
  must **FAIL_CLOSED**.

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
