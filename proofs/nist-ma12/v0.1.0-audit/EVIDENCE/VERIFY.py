from __future__ import annotations
import argparse
import base64
import hashlib
import json
from pathlib import Path

def fail(msg: str) -> None:
    raise SystemExit(f"FAIL_CLOSED: {msg}")

def read_utf8(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except Exception as exc:
        fail(f"read/decode failed: {p}: {exc}")
    raise AssertionError("unreachable")

def load_json(p: Path):
    try:
        return json.loads(read_utf8(p))
    except Exception as exc:
        fail(f"json parse failed: {p}: {exc}")
    raise AssertionError("unreachable")

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def verify_signature_if_present(evidence_dir: Path, manifest_bytes: bytes) -> None:
    sig_p = evidence_dir / "manifest.sig"
    pub_p = evidence_dir / "enforcement.pub"
    if not sig_p.exists() and not pub_p.exists():
        return
    if not sig_p.exists() or not pub_p.exists():
        fail("signature artifacts incomplete")
    try:
        from nacl.signing import VerifyKey  # type: ignore
    except Exception as exc:
        fail(f"signature present but pynacl unavailable: {exc}")
    sig = base64.b64decode(read_utf8(sig_p).strip())
    pub = base64.b64decode(read_utf8(pub_p).strip())
    try:
        VerifyKey(pub).verify(manifest_bytes, sig)
    except Exception as exc:
        fail(f"manifest signature verification failed: {exc}")

def canon_sha(obj: dict) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--evidence_dir", required=True)
    args = ap.parse_args()
    e = Path(args.evidence_dir).resolve()
    if not e.exists():
        fail(f"missing evidence dir: {e}")

    manifest_p = e / "manifest.json"
    if not manifest_p.exists():
        fail("missing manifest.json")
    manifest_bytes = manifest_p.read_bytes()
    verify_signature_if_present(e, manifest_bytes)
    manifest = load_json(manifest_p)

    files = manifest.get("files", [])
    if not isinstance(files, list) or not files:
        fail("manifest files missing/invalid")
    for item in files:
        rel = item.get("path")
        expected = item.get("sha256")
        if not isinstance(rel, str) or not isinstance(expected, str):
            fail("manifest entry invalid")
        p = e / rel
        if not p.exists():
            fail(f"missing file: {rel}")
        if sha256_file(p) != expected:
            fail(f"hash mismatch: {rel}")

    required = [
        "MA12_NIST_DISC.json",
        "NIST_MAPPING.json",
        "robustness.json",
        "forbidden_action_attempt.json",
        "receipt.json",
        "openclaw/final_report.json",
        "openclaw/verify_result.json",
        "openclaw/shared_manifest.json",
    ]
    for rp in required:
        if not (e / rp).exists():
            fail(f"missing required evidence file: {rp}")

    disc = load_json(e / "MA12_NIST_DISC.json")
    mapping = load_json(e / "NIST_MAPPING.json")
    robustness = load_json(e / "robustness.json")
    attempt = load_json(e / "forbidden_action_attempt.json")
    receipt = load_json(e / "receipt.json")
    oc_report = load_json(e / "openclaw/final_report.json")
    oc_verify = load_json(e / "openclaw/verify_result.json")

    if disc.get("status") != "VERIFIED":
        fail("disc status not VERIFIED")
    if disc.get("merkle_root") != canon_sha(disc.get("evidence", {})):
        fail("disc merkle_root mismatch")

    selected_id = mapping.get("selected_constraint_id")
    selected_desc = mapping.get("selected_constraint_description")
    if not selected_id or not selected_desc:
        fail("mapping missing selected constraint binding")
    if not isinstance(mapping.get("executed_test_ids", []), list) or not mapping.get("executed_test_ids"):
        fail("mapping missing executed_test_ids")

    if robustness.get("status") != "PASS":
        fail("robustness status not PASS")
    if attempt.get("pass") is not True:
        fail("forbidden action attempt not marked pass")
    dec = attempt.get("decision", {})
    res = attempt.get("result", {})
    if dec.get("status") != "DENY":
        fail("forbidden action decision not DENY")
    if res.get("executed") is not False:
        fail("forbidden action executed unexpectedly")

    if oc_report.get("status") != "PASS":
        fail("openclaw final_report status not PASS")
    if oc_verify.get("status") != "PASS":
        fail("openclaw verify_result status not PASS")

    if not isinstance(receipt.get("artifact_hashes", {}), dict):
        fail("receipt artifact_hashes missing/invalid")

    print("VERIFY PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
