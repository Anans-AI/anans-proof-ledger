# Verification Guide — NIST MA-12 Audit Bundle v0.1.0-audit

## Prerequisites

- Python 3.8 or later
- `pynacl` library: `pip install pynacl`

No other dependencies. The verifier is self-contained.

## How to Verify

From the repository root:

```
cd proofs/nist-ma12/v0.1.0-audit/EVIDENCE
python VERIFY.py --evidence_dir .
```

Expected output on a valid bundle:

```
VERIFY PASS
```

## What the Verifier Checks

1. **Signature** — Loads `enforcement.pub` and verifies the Ed25519 signature in
   `manifest.sig` over the canonical bytes of `manifest.json`. A tampered manifest
   or wrong public key produces `FAIL_CLOSED: signature invalid`.

2. **File hashes** — For every file listed in `manifest.json`, recomputes its
   SHA-256 and compares it against the recorded value. Any file modified after
   signing produces `FAIL_CLOSED: hash mismatch: <filename>`.

The verifier is intentionally fail-closed: any error exits with a non-zero code
and a `FAIL_CLOSED:` message. There is no partial-pass state.

## Failure Modes and Meaning

| Output | Meaning |
|---|---|
| `VERIFY PASS` | Bundle is intact and signature is valid |
| `FAIL_CLOSED: signature invalid` | `manifest.json` was altered after signing, or wrong public key |
| `FAIL_CLOSED: hash mismatch: <file>` | Named file was altered after the manifest was signed |
| `FAIL_CLOSED: missing file: <file>` | A file listed in the manifest is absent |

A signed manifest that does not match the committed files is **worse than
unsigned** — it signals either a staging mistake (wrong file set committed)
or a post-sign overwrite. Do not treat such a bundle as authoritative.

## Negative Tests (Tamper Resistance)

To confirm the verifier catches tampering:

```bash
# 1. Tamper with a file — must fail
echo "x" >> MA12_NIST_DISC.json
python VERIFY.py --evidence_dir .
# Expected: FAIL_CLOSED: hash mismatch: MA12_NIST_DISC.json

# Restore
git checkout -- MA12_NIST_DISC.json

# 2. Tamper with the manifest — must fail
echo "x" >> manifest.json
python VERIFY.py --evidence_dir .
# Expected: FAIL_CLOSED: signature invalid

# Restore
git checkout -- manifest.json

# 3. Clean restore — must pass
python VERIFY.py --evidence_dir .
# Expected: VERIFY PASS
```

## Key Provenance

The `enforcement.pub` public key was generated and held by the bundle author.
No private key material is included in this repository.

## Bundle Metadata

| Field | Value |
|---|---|
| Proof ID | `nist_ma12_disc` |
| Compiler | `evidence_compiler_v2` |
| Build timestamp | `2026-02-24T17:48:02Z` |
| Signing algorithm | Ed25519 (pynacl) |
