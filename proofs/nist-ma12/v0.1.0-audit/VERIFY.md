# Verification Guide — NIST MA12 Proof Bundle (v0.1.0-audit)

## Scope

This proof bundle is an **offline-verifiable evidence container** demonstrating
deterministic, fail-closed denial of a forbidden action attempt under a mapped
NIST-derived constraint.

## What this is not

- Not a blockchain ledger or transparency log.
- Not OS-level containment.
- Not blanket regulatory compliance.
- Not a live agent runtime.

## Cold verification (recommended)

1. Download the zip asset for this proof bundle.
2. Unzip into an empty directory.
3. From inside the extracted directory, run:

```
python VERIFY.py --evidence_dir .
```

Expected: `VERIFY PASS`

## Falsifiability / negative tests

1. Evidence tamper:
   - Flip one byte in any evidence JSON (e.g., `robustness.json`)
   - Rerun VERIFY → must `FAIL_CLOSED: hash mismatch`

2. Manifest tamper:
   - Flip one byte in `manifest.json`
   - Rerun VERIFY → must `FAIL_CLOSED: manifest signature verification failed`

## Failure Modes

| Output | Meaning |
|---|---|
| `VERIFY PASS` | Bundle is intact and signature is valid |
| `FAIL_CLOSED: signature invalid` | `manifest.json` was altered after signing, or wrong public key |
| `FAIL_CLOSED: hash mismatch: <file>` | Named file was altered after the manifest was signed |
| `FAIL_CLOSED: missing file: <file>` | A file listed in the manifest is absent |

## Dependencies

- Python 3.x
- PyNaCl required for v1 signature verification (Ed25519). If PyNaCl is missing,
  signature checks cannot run.

## Bundle Metadata

| Field | Value |
|---|---|
| Proof ID | `nist_ma12_disc` |
| Compiler | `evidence_compiler_v2` |
| Build timestamp | `2026-02-24T17:48:02Z` |
| Signing algorithm | Ed25519 (pynacl) |
