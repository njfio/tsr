"""Phase 0 / Phase 1 acceptance: rulings reproduced from records alone; no hand-coded ruling in the decision path."""
import re
from pathlib import Path

import pytest

from tsr_runner.schema import load_corpus, validate
from tsr_runner.rule import calibrate, decide, load_criteria
from tsr_runner.vocab import Vocab, load_lexicon, ROOT
from tsr_runner import formal

LEX = load_lexicon()
CRIT = load_criteria()
RECS = load_corpus(ROOT / "corpus")


def test_corpus_validates():
    errs = []
    for r in RECS:
        errs += validate(r, LEX["quantities"], set(CRIT["identity_forms"]))
    assert errs == []


def test_all_published_rulings_reproduced():
    cal = calibrate(RECS, LEX, CRIT)
    misses = [r for r in cal["rows"] if not r["match"]]
    assert cal["total"] >= 22
    assert misses == [], misses


def test_pending_rulings_are_only_the_unpublished_two():
    cal = calibrate(RECS, LEX, CRIT)
    assert set(cal["pending_author"]) == {"mech.escape_velocity", "mech.centripetal_force"}


def test_no_hand_coded_rulings_in_decision_path():
    src = (ROOT / "tsr_runner" / "rule.py").read_text()
    for forbidden in ["ruling.shape", "book_status", '"keep"', "'invert'"]:
        assert forbidden not in src.split("def calibrate")[0], forbidden


def test_open_joints_are_not_forced():
    by_id = {r.id: r for r in RECS}
    for rid in ["rel.row11_mass_energy_warps_spacetime", "rel.row12_wells_and_lensing", "mech.newtons_second_law"]:
        assert decide(by_id[rid], LEX, CRIT).forced is False


def test_undetermined_quantity_gives_judgment():
    from tsr_runner.schema import Relation, Variable, Cost
    r = Relation(id="t", domain="thermodynamics", title="t", statement="s", form="equation",
                 variables=[Variable("heat capacity C", "heat capacity")],
                 costs=[Cost("warming", ["heat capacity"])])
    d = decide(r, LEX, CRIT)
    assert d.shape == "JUDGMENT" and d.forced is False and "C3" in d.rule_trace


def test_resistance_criterion_is_domain_independent():
    """Every lexicon verdict cites a clause of R1 or 'none'; no entry mentions a domain as its reason."""
    for q, e in LEX["quantities"].items():
        assert e["verdict"] in (True, False, "undetermined"), q
        assert not re.search(r"reflects (better|well)", e.get("reason", "")), q


def test_mirror_twice_baseline_matches_tsr_formal():
    v = Vocab()
    clashes = v.many_to_one()
    assert set(clashes) >= {"Current", "Desire"}
    assert v.typed_clashes() == {}


def test_composition_of_book_formulas():
    v = Vocab()
    cases = [("F = m × a", {"F": "force", "m": "mass m", "a": "acceleration"}, "Frequency = Movement M × Appreciation"),
             ("m = ρ × V", {"m": "mass m", "ρ": "density", "V": "volume"}, "Movement M = Desire × Vibrance"),
             ("E = m × c²", {"E": "physical energy", "m": "mass m", "c": "speed of light c"}, "C² × M = E")]
    for p, n, r in cases:
        assert formal.composition_check(p, n, r, v)["ok"] is True, (p, r)


def test_rewritten_formula_is_a_composition_failure():
    v = Vocab()
    res = formal.composition_check("F = k × x", {"F": "force", "k": "spring constant", "x": "space"},
                                   "Frequency = Vibration ÷ Movement M", v)
    assert res["ok"] is False


def test_units_do_not_cross():
    v = Vocab()
    assert v.lint_formula("(kinetic energy) = ½ × Movement M × rise per Expansion") != []
    assert v.lint_formula("C² × M = E") == []
    assert v.new_words("Frequency = Desire-field × Appreciation") == ["Desire-field"]


def test_parity_formula_level():
    fails = formal.parity_check({"a": "keeps", "b": "keeps", "c": "keeps"}, {"c": ["a", "b"]}, "formula")
    assert fails == []
    fails = formal.parity_check({"a": "keeps", "b": "turns around", "c": "keeps"}, {"c": ["a", "b"]}, "formula")
    assert fails and fails[0]["collision"] is True


def test_sign_graph_detects_opposite_edges():
    res = formal.sign_graph_check([{"rises": "Frequency", "with": "alignment", "sign": 1},
                                   {"rises": "Frequency", "with": "alignment", "sign": -1}])
    assert res["ok"] is False
