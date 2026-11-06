"""The pipeline produces every artifact on a mock roster, and labels them MOCK."""
import json
import shutil
from pathlib import Path

from tsr_runner.cli import main
from tsr_runner.vocab import ROOT


def test_mock_run_end_to_end():
    run_id = "pytest-MOCK"
    shutil.rmtree(ROOT / "results" / run_id, ignore_errors=True)
    rc = main(["run", "--domain", "calibration", "--include-ruled", "--mock", "--run-id", run_id])
    assert rc == 0
    rd = ROOT / "results" / run_id
    for f in ["config.json", "rows.json", "collisions.json", "breaks.json", "decoys.json", "canary.json", "report.md", "calls.jsonl"]:
        assert (rd / f).exists(), f
    rows = json.loads((rd / "rows.json").read_text())
    assert all(r["mock"] for r in rows)
    assert "MOCK" in (rd / "report.md").read_text()
    # hidden calibration: damping lands as turns around
    damp = next(r for r in rows if r["record_id"] == "mech.damping")
    assert damp["consensus"]["shape"] == "turns around" and damp["candidate_forced"]
    shutil.rmtree(rd)


def test_dissenting_mock_fails_agreement_gate():
    from tsr_runner.providers import ModelSpec, CallLog, LoggedModel
    from tsr_runner.schema import load_corpus
    from tsr_runner.rule import load_criteria
    from tsr_runner.vocab import Vocab, load_lexicon
    from tsr_runner import generate
    recs = {r.id: r for r in load_corpus(ROOT / "corpus")}
    log = CallLog(ROOT / "results" / "pytest-dissent-MOCK")
    gens = [LoggedModel(ModelSpec(f"m-{i}", "mock:dissent", "v"), log) for i in range(1, 6)]
    # two of five dissent -> 3/5 < 4
    gens[1].spec.name = "a-2"; gens[2].spec.name = "b-2"
    rr = generate.run_row(recs["mech.friction"], gens, None, Vocab(), load_lexicon(), load_criteria(), wording_pass=False)
    assert rr.candidate_forced is False and any("agree" in g for g in rr.gate)
    shutil.rmtree(ROOT / "results" / "pytest-dissent-MOCK")
