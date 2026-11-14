#!/usr/bin/env python3
"""
run_mutation_suite.py — Part 4 Break-It Mutation Suite (M01-M15).

Executes all 15 pre-registered single-point mutations from
proof/heldout/PREREGISTRATION.md Section 3.2 in fresh isolated temporary copies
without ever mutating the live repository.

Supports:
  - Default mode: runs M01..M15 and writes proof/heldout/mutation_results.json
  - --verify-offline: validates hygiene, all 15 verbatim snippets in live files,
    source SHA-256 manifest parity, and proof/heldout/mutation_results.json invariants.

Python 3.12+ standard library only (zero external packages).
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any

PREREGISTRATION_COMMIT_SHA = "463ad9f93c8a276b1e0d9ee497198dfa2169d079"

HELDOUT_DIR = Path(__file__).resolve().parent
REPO_ROOT = HELDOUT_DIR.parents[1]
RESULTS_PATH = HELDOUT_DIR / "mutation_results.json"
CERT_PATH = REPO_ROOT / "proof" / "verification_certificate.json"

# Hex-encoded hygiene patterns (matching Part 2 scripts plus local user paths).
_FORBIDDEN_SUBSTRINGS_HEX = [
    "2f55736572732f",
    "2f55736572732f6e6a66",
    "66696c653a2f2f2f",
    "7473725f3031",
    "2e706466",
    "726973657265",
    "763535",
    "70726f6f66203236",
    "4e5f626c696e64",
    "6e5f626c696e645f7061697273",
    "2e67656d696e69",
    "626c696e64",
    "73616d706c655f6d616e6966657374",
]


@dataclass(frozen=True)
class MutationSpec:
    id: str
    file_path: str
    symbol: str
    expected_check: str
    kind: str  # "lean" or "full_suite"
    original_snippet: str
    mutated_snippet: str


MUTATION_SPECS: tuple[MutationSpec, ...] = (
    MutationSpec(
        id="M01",
        file_path="proof/lean/TSR/Condition.lean",
        symbol="barrier (Lean definition)",
        expected_check="lake build fails at condition_triad_equivalence / destructive_null_requires_spatial_separation",
        kind="lean",
        original_snippet="def barrier (M : Medium F) (x y : M.Locus) : F := M.rho * M.dist x y",
        mutated_snippet="def barrier (M : Medium F) (_x _y : M.Locus) : F := zero",
    ),
    MutationSpec(
        id="M02",
        file_path="proof/lean/TSR/Condition.lean",
        symbol="condition_triad_equivalence (Lean theorem assumption)",
        expected_check="lake build fails at condition_triad_equivalence (missing partition assumption hPart)",
        kind="lean",
        original_snippet="theorem condition_triad_equivalence (M : Medium F) (hPart : IsPartitionedMedium M) :",
        mutated_snippet="theorem condition_triad_equivalence (M : Medium F) :",
    ),
    MutationSpec(
        id="M03",
        file_path="proof/lean/TSR/Condition.lean",
        symbol="damped_ripple_strict_decay (Lean theorem assumption)",
        expected_check="lake build fails at damped_ripple_strict_decay (M.alpha_bounds_of_pos hRes type mismatch)",
        kind="lean",
        original_snippet=(
            "theorem damped_ripple_strict_decay (M : PerturbationMedium F)\n"
            "    (hRes : zero < M.rho) (B0 : F) (hB0 : zero < B0)"
        ),
        mutated_snippet=(
            "theorem damped_ripple_strict_decay (M : PerturbationMedium F)\n"
            "    (hRes : zero ≤ M.rho) (B0 : F) (hB0 : zero < B0)"
        ),
    ),
    MutationSpec(
        id="M04",
        file_path="proof/lean/TSR/MirrorFunctor.lean",
        symbol="mirrorAtom (Lean definition)",
        expected_check="lake build fails at mirrorAtom_involutive / R_form_involutive",
        kind="lean",
        original_snippet="  | .lightSpeed => .current",
        mutated_snippet="  | .lightSpeed => .attraction",
    ),
    MutationSpec(
        id="M05",
        file_path="proof/lean/TSR/MirrorFunctor.lean",
        symbol="regionResistant (Lean definition)",
        expected_check="lake build fails at two_level_reading_theorem (decide) and gravity_open_joint_two_vs_three_regions",
        kind="lean",
        original_snippet=(
            "def regionResistant : MirrorRegion → Bool\n"
            "  | .physical      => true\n"
            "  | .nonphysical   => false\n"
            "  | .sharedOverlap => false"
        ),
        mutated_snippet=(
            "def regionResistant : MirrorRegion → Bool\n"
            "  | .physical      => true\n"
            "  | .nonphysical   => false\n"
            "  | .sharedOverlap => true"
        ),
    ),
    MutationSpec(
        id="M06",
        file_path="proof/lean/TSR/MirrorFunctor.lean",
        symbol="benchmarkRows17 Row 2 (Lean benchmark row)",
        expected_check="lake build fails at two_level_reading_theorem and v57_rule_wordings_benchmark (decide)",
        kind="lean",
        original_snippet='  ⟨2,  "2 no shared now (distance)",      .Invert, false, .SpatialSeparationDependence⟩,',
        mutated_snippet='  ⟨2,  "2 no shared now (distance)",      .Keep, false, .SpatialSeparationDependence⟩,',
    ),
    MutationSpec(
        id="M07",
        file_path="proof/lean/TSR/MirrorFunctor.lean",
        symbol="benchmarkRows17 Row 7 (Lean benchmark row)",
        expected_check="lake build fails at two_level_reading_theorem and v57_rule_wordings_benchmark (decide)",
        kind="lean",
        original_snippet='  ⟨7,  "7 E = mc^2",                      .Keep,   true,  .IdentityOrEquiv⟩,',
        mutated_snippet='  ⟨7,  "7 E = mc^2",                      .Invert,   true,  .IdentityOrEquiv⟩,',
    ),
    MutationSpec(
        id="M08",
        file_path="proof/lean/TSR/MirrorFunctor.lean",
        symbol="isSharedEnergyWork (Lean definition)",
        expected_check="lake build fails at v57_rule_wordings_benchmark (decide: R_read_v57_ch16 match count drops from 16 to 14)",
        kind="lean",
        original_snippet=(
            "def isSharedEnergyWork : LawAST → Bool\n"
            "  | .SharedCenterCurvature => true\n"
            "  | _                      => false"
        ),
        mutated_snippet=(
            "def isSharedEnergyWork : LawAST → Bool\n"
            "  | .SharedCenterCurvature => false\n"
            "  | _                      => false"
        ),
    ),
    MutationSpec(
        id="M09",
        file_path="proof/lean/TSR/Crossing.lean",
        symbol="canStep (Lean definition)",
        expected_check="lake build fails at step_from_intuition_false and unique_weak_diagonal_escape",
        kind="lean",
        original_snippet="  | (.NP, .In),  (.P,  .Out) => tuned  -- Weak Diagonal: Intuition shifts Belief iff tuned",
        mutated_snippet="  | (.NP, .In),  (.P,  .Out) => true",
    ),
    MutationSpec(
        id="M10",
        file_path="proof/lean/TSR/EntityAndMeta.lean",
        symbol="sovereignEntityDyn (Lean definition)",
        expected_check="lake build fails at four_way_entity_separation",
        kind="lean",
        original_snippet="  stepOuterObjective := fun st x => st.outerObjective + predErrorSq st x",
        mutated_snippet="  stepOuterObjective := fun st _ => st.outerObjective",
    ),
    MutationSpec(
        id="M11",
        file_path="proof/z3/structural_rigidity.py",
        symbol="_build_stage_relations (Z3 Stage 2 relation graph)",
        expected_check="run_structural_rigidity() raises AssertionError: Expected 2 at Stage 2, got 4",
        kind="full_suite",
        original_snippet='        rels["gate_cocreates_center2"] = (2, {(IDX["Tune"], IDX["Attraction"])})',
        mutated_snippet="        # disabled gate_cocreates_center2",
    ),
    MutationSpec(
        id="M12",
        file_path="proof/z3/structural_rigidity.py",
        symbol="_build_stage_relations (Z3 Stage 3 relation graph)",
        expected_check="run_structural_rigidity() raises AssertionError: Expected 1 at Stage 3, got 2",
        kind="full_suite",
        original_snippet="    if stage >= 3:",
        mutated_snippet="    if stage >= 99:",
    ),
    MutationSpec(
        id="M13",
        file_path="proof/z3/lexical_rigidity.py",
        symbol='SLOT_REQUIREMENTS["Expansion"] (Z3 lexical slot)',
        expected_check="verify_tsr_sat_and_uniqueness() raises AssertionError: Canonical TSR assignment must be globally unique!",
        kind="full_suite",
        original_snippet='        ("continuum_unfolding_sense", "Expansion_names_unbounded_continuum_unfolding_rather_than_organismal_lifecycle"),',
        mutated_snippet="        # removed continuum_unfolding_sense",
    ),
    MutationSpec(
        id="M14",
        file_path="proof/etymology/combinatorial_proofs.py",
        symbol="shares_4char_substring (Python combinatorics)",
        expected_check="verify_part3_invariants() fails N_orth_unrelated == 3152 (becomes 3153) and run_self_tests() fails",
        kind="full_suite",
        original_snippet=(
            '    if fam_a == "ment" and fam_b == "ment" and a[:2] == b[:2]:\n'
            "        return True"
        ),
        mutated_snippet=(
            '    if fam_a == "ment" and fam_b == "ment" and a[:2] == b[:2]:\n'
            "        return False"
        ),
    ),
    MutationSpec(
        id="M15",
        file_path="proof/etymology/combinatorial_proofs.py",
        symbol="exact_hypergeometric_upper_tail (Python fractions primary test)",
        expected_check="verify_part3_invariants() fails 0.287 < exact_hypergeometric_p_float < 0.289 (p drops to 0.0429)",
        kind="full_suite",
        original_snippet="    for k in range(obs_k, max_k + 1):",
        mutated_snippet="    for k in range(obs_k + 1, max_k + 1):",
    ),
)


def _decode_hex_list(hex_items: list[str]) -> list[str]:
    return [bytes.fromhex(item).decode("utf-8") for item in hex_items]


def _check_hygiene(named_texts: list[tuple[str, str]]) -> None:
    forbidden = _decode_hex_list(_FORBIDDEN_SUBSTRINGS_HEX)
    for label, text in named_texts:
        lowered = text.lower()
        for tok in forbidden:
            if tok.lower() in lowered:
                raise RuntimeError(f"Forbidden hygiene token {tok!r} found in {label}")


def _snapshot_repo_hashes() -> dict[str, str]:
    """Hash all source/data files in live repo directories used by verification."""
    hashes: dict[str, str] = {}
    for sub in ("proof", "arms", "vocab", "rule", "tests"):
        root = REPO_ROOT / sub
        if not root.exists():
            continue
        for f in sorted(root.rglob("*")):
            if (
                f.is_file()
                and ".lake" not in f.parts
                and "__pycache__" not in f.parts
                and not f.name.startswith(".")
                and not f.name.endswith((".pyc", ".pyo"))
                and f != RESULTS_PATH
            ):
                rel = f.relative_to(REPO_ROOT).as_posix()
                hashes[rel] = hashlib.sha256(f.read_bytes()).hexdigest()
    return hashes


def _build_env() -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    elan_bin = Path.home() / ".elan" / "bin"
    if elan_bin.exists():
        env["PATH"] = f"{elan_bin}:{env.get('PATH', '')}"
    return env


def _copy_seed_tree(seed_dir: Path, env: dict[str, str]) -> None:
    """Populate a clean isolated seed workspace without touching the live repo."""
    for sub in ("proof", "arms", "vocab", "rule", "tests"):
        src = REPO_ROOT / sub
        if not src.exists():
            continue

        def _ignore(directory: str, names: list[str]) -> set[str]:
            ignored: set[str] = set()
            rel_dir = Path(directory).resolve().relative_to(REPO_ROOT.resolve())
            for name in names:
                if name in {"__pycache__", ".DS_Store"} or name.endswith((".pyc", ".pyo", ".mp3")):
                    ignored.add(name)
                elif rel_dir == Path("proof/heldout") and name == "packets":
                    ignored.add(name)
            return ignored

        shutil.copytree(
            src,
            seed_dir / sub,
            ignore=_ignore,
            copy_function=shutil.copy2,
        )

    lean_dir = seed_dir / "proof" / "lean"
    if not (lean_dir / ".lake").exists():
        build_proc = subprocess.run(
            ["lake", "build"],
            cwd=lean_dir,
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=300,
        )
        if build_proc.returncode != 0:
            raise RuntimeError(
                f"Baseline lake build in temp seed failed (exit {build_proc.returncode}):\n"
                f"{build_proc.stdout}\n{build_proc.stderr}"
            )


def _sanitize_excerpt(raw_output: str, temp_case: Path, temp_seed: Path) -> str:
    """Strip any temp/repo directory paths and keep a concise failure excerpt."""
    text = raw_output
    path_candidates = {
        str(temp_case.resolve()),
        str(temp_case),
        str(temp_seed.resolve()),
        str(temp_seed),
        str(REPO_ROOT.resolve()),
        str(REPO_ROOT),
    }
    for prefix in sorted(path_candidates, key=len, reverse=True):
        if prefix:
            text = text.replace(prefix + "/", "")
            text = text.replace(prefix, "<workspace>")

    tmp_root = str(Path(tempfile.gettempdir()).resolve())
    text = re.sub(rf"{re.escape(tmp_root)}/tsr_mut_[^/\s:]+/?", "", text)
    text = re.sub(r"/tmp/tsr_mut_[^/\s:]+/?", "", text)
    text = re.sub(r"/private/var/folders/[^\s:]+/tsr_mut_[^/\s:]+/?", "", text)

    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    tb_idx = -1
    for i, line in enumerate(lines):
        if line.startswith("Traceback (most recent call last):"):
            tb_idx = i
    if tb_idx != -1:
        selected = lines[tb_idx:]
    else:
        err_indices = [i for i, line in enumerate(lines) if "error:" in line]
        if err_indices:
            start = max(0, err_indices[0] - 2)
            selected = lines[start:]
        else:
            selected = lines[-12:]

    excerpt = "\n".join(selected[-14:])
    if len(excerpt) > 900:
        excerpt = excerpt[-900:]
    return excerpt


def _run_single_mutation(
    spec: MutationSpec,
    seed_dir: Path,
    env: dict[str, str],
) -> dict[str, Any]:
    """Execute one mutation inside its own fresh isolated temporary copy."""
    with tempfile.TemporaryDirectory(prefix=f"tsr_mut_{spec.id}_") as tmp_dir:
        temp_case = Path(tmp_dir) / "workspace"
        shutil.copytree(seed_dir, temp_case, copy_function=shutil.copy2)

        target = temp_case / spec.file_path
        target_text = target.read_text(encoding="utf-8")
        occurrences = target_text.count(spec.original_snippet)
        assert occurrences == 1, (
            f"{spec.id}: expected 1 occurrence of original snippet in {spec.file_path}, found {occurrences}"
        )
        mutated_text = target_text.replace(spec.original_snippet, spec.mutated_snippet, 1)
        assert mutated_text != target_text, f"{spec.id}: mutation produced no change"
        target.write_text(mutated_text, encoding="utf-8")

        if spec.kind == "lean":
            cmd = ["lake", "build"]
            cwd = temp_case / "proof" / "lean"
            cmd_label = "lake build"
        elif spec.kind == "full_suite":
            cmd = [sys.executable, "-B", "proof/run_all_proofs.py"]
            cwd = temp_case
            cmd_label = "python3 -B proof/run_all_proofs.py"
        else:
            raise ValueError(f"Unknown mutation kind: {spec.kind}")

        t0 = time.perf_counter()
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=180,
        )
        elapsed = round(time.perf_counter() - t0, 3)

        combined = (proc.stderr or "") + "\n" + (proc.stdout or "")
        excerpt = _sanitize_excerpt(combined, temp_case, seed_dir)
        caught = proc.returncode != 0

        return {
            "id": spec.id,
            "file_path": spec.file_path,
            "symbol": spec.symbol,
            "expected_check": spec.expected_check,
            "verifier_command": cmd_label,
            "exit_code": proc.returncode,
            "caught": caught,
            "runtime_seconds": elapsed,
            "failure_excerpt": excerpt,
        }


def _verify_mutation_specs_in_live_repo() -> None:
    """Read-only verification that all 15 original snippets match uniquely in live files."""
    seen_ids: list[str] = []
    for spec in MUTATION_SPECS:
        seen_ids.append(spec.id)
        target = REPO_ROOT / spec.file_path
        if not target.exists():
            raise RuntimeError(f"{spec.id}: missing target file {spec.file_path}")
        text = target.read_text(encoding="utf-8")
        count = text.count(spec.original_snippet)
        if count != 1:
            raise RuntimeError(
                f"{spec.id}: expected exact count 1 in {spec.file_path}, got {count}"
            )
        if spec.original_snippet == spec.mutated_snippet:
            raise RuntimeError(f"{spec.id}: original and mutated snippets are identical")
    expected_ids = [f"M{i:02d}" for i in range(1, 16)]
    if seen_ids != expected_ids:
        raise RuntimeError(f"Unexpected mutation ID sequence: {seen_ids}")


def _verify_certificate_manifest_parity() -> None:
    """Verify live Lean/Z3/etymology files match proof/verification_certificate.json hashes."""
    if not CERT_PATH.exists():
        raise RuntimeError(f"Missing certificate file: {CERT_PATH}")
    cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
    if cert.get("preregistration_commit_sha") != PREREGISTRATION_COMMIT_SHA:
        raise RuntimeError("Certificate preregistration_commit_sha mismatch")
    manifest = cert.get("source_sha256_manifest", {})
    if not manifest:
        raise RuntimeError("Certificate source_sha256_manifest is empty")
    for rel, expected_sha in manifest.items():
        path = REPO_ROOT / rel
        if not path.exists():
            raise RuntimeError(f"Missing manifest file: {rel}")
        actual_sha = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_sha != expected_sha:
            raise RuntimeError(f"SHA-256 mismatch on {rel}: {actual_sha} != {expected_sha}")


def _verify_offline_results() -> dict[str, Any]:
    """Validate committed mutation_results.json, live snippets, manifest, and hygiene."""
    _verify_mutation_specs_in_live_repo()
    _verify_certificate_manifest_parity()

    if not RESULTS_PATH.exists():
        raise RuntimeError(f"Missing mutation results file: {RESULTS_PATH}")
    results_text = RESULTS_PATH.read_text(encoding="utf-8")
    script_text = Path(__file__).read_text(encoding="utf-8")
    _check_hygiene(
        [
            (Path(__file__).name, script_text),
            (RESULTS_PATH.name, results_text),
        ]
    )

    payload = json.loads(results_text)
    if payload.get("preregistration_commit_sha") != PREREGISTRATION_COMMIT_SHA:
        raise RuntimeError("preregistration_commit_sha mismatch in mutation_results.json")

    env_info = payload.get("execution_environment", {})
    for key in ("os", "arch", "python_version"):
        if not env_info.get(key):
            raise RuntimeError(f"Missing execution_environment.{key}")

    if payload.get("total_mutations") != 15:
        raise RuntimeError(f"Expected total_mutations == 15, got {payload.get('total_mutations')}")
    if payload.get("caught_count") != 15:
        raise RuntimeError(f"Expected caught_count == 15, got {payload.get('caught_count')}")
    if payload.get("surviving_count") != 0:
        raise RuntimeError(f"Expected surviving_count == 0, got {payload.get('surviving_count')}")
    if payload.get("surviving_mutations") != []:
        raise RuntimeError(f"Expected empty surviving_mutations, got {payload.get('surviving_mutations')}")
    if payload.get("all_caught") is not True:
        raise RuntimeError("Expected all_caught == true")

    records = payload.get("mutations", [])
    if len(records) != 15:
        raise RuntimeError(f"Expected 15 mutation records, got {len(records)}")

    for spec, rec in zip(MUTATION_SPECS, records):
        expected_cmd = "lake build" if spec.kind == "lean" else "python3 -B proof/run_all_proofs.py"
        if rec.get("id") != spec.id:
            raise RuntimeError(f"Mutation ID mismatch: {rec.get('id')} != {spec.id}")
        if rec.get("file_path") != spec.file_path:
            raise RuntimeError(f"{spec.id}: file_path mismatch")
        if rec.get("symbol") != spec.symbol:
            raise RuntimeError(f"{spec.id}: symbol mismatch")
        if rec.get("expected_check") != spec.expected_check:
            raise RuntimeError(f"{spec.id}: expected_check mismatch")
        if rec.get("verifier_command") != expected_cmd:
            raise RuntimeError(f"{spec.id}: verifier_command mismatch")
        if rec.get("exit_code") == 0 or rec.get("caught") is not True:
            raise RuntimeError(f"{spec.id}: mutation survived!")
        if not isinstance(rec.get("runtime_seconds"), (int, float)) or rec["runtime_seconds"] < 0:
            raise RuntimeError(f"{spec.id}: invalid runtime_seconds")
        if not str(rec.get("failure_excerpt", "")).strip():
            raise RuntimeError(f"{spec.id}: empty failure_excerpt")
        if "tsr_mut_" in rec["failure_excerpt"]:
            raise RuntimeError(f"{spec.id}: temp directory name leaked in failure_excerpt")

    return {
        "mode": "verify-offline",
        "hygiene_passed": True,
        "snippets_verified": 15,
        "certificate_manifest_verified": True,
        "total_mutations": 15,
        "caught_count": 15,
        "surviving_count": 0,
        "all_caught": True,
        "execution_environment": env_info,
    }


def run_suite() -> dict[str, Any]:
    """Execute all 15 mutations in isolated temp copies and write mutation_results.json."""
    _verify_mutation_specs_in_live_repo()
    baseline_hashes = _snapshot_repo_hashes()
    env = _build_env()

    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="tsr_mut_seed_") as seed_tmp:
        seed_dir = Path(seed_tmp) / "seed"
        _copy_seed_tree(seed_dir, env)

        for spec in MUTATION_SPECS:
            entry = _run_single_mutation(spec, seed_dir, env)
            after_hashes = _snapshot_repo_hashes()
            assert after_hashes == baseline_hashes, (
                f"Live repository files changed during {spec.id}!"
            )
            results.append(entry)
            status = "CAUGHT" if entry["caught"] else "SURVIVED"
            print(
                f"[{spec.id}] {status} (exit={entry['exit_code']}, {entry['runtime_seconds']:.2f}s) "
                f"— {spec.file_path}"
            )

    surviving = [r["id"] for r in results if not r["caught"]]
    caught_count = sum(1 for r in results if r["caught"])

    payload = {
        "preregistration_commit_sha": PREREGISTRATION_COMMIT_SHA,
        "execution_environment": {
            "os": platform.system(),
            "arch": platform.machine(),
            "python_version": platform.python_version(),
        },
        "total_mutations": len(results),
        "caught_count": caught_count,
        "surviving_count": len(surviving),
        "surviving_mutations": surviving,
        "all_caught": caught_count == len(MUTATION_SPECS),
        "mutations": results,
    }

    payload_text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    script_text = Path(__file__).read_text(encoding="utf-8")
    _check_hygiene(
        [
            (Path(__file__).name, script_text),
            (RESULTS_PATH.name, payload_text),
        ]
    )

    RESULTS_PATH.write_text(payload_text, encoding="utf-8")

    return {
        "mode": "run",
        "hygiene_passed": True,
        "total_mutations": len(results),
        "caught_count": caught_count,
        "surviving_count": len(surviving),
        "surviving_mutations": surviving,
        "all_caught": caught_count == len(MUTATION_SPECS),
        "results_path": RESULTS_PATH.relative_to(REPO_ROOT).as_posix(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run or offline-verify the Part 4 15-mutation Break-It suite (M01-M15)."
    )
    parser.add_argument(
        "--verify-offline",
        action="store_true",
        help="Verify hygiene, all 15 verbatim snippets, manifest hashes, and mutation_results.json without mutating.",
    )
    args = parser.parse_args()
    summary = _verify_offline_results() if args.verify_offline else run_suite()
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_caught"] else 1


if __name__ == "__main__":
    sys.exit(main())
