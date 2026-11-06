"""Curation control: round-2 style blind rating (spec section 8).

For each forced row: T = the consensus sentence, D = a decoy with the shape flipped,
W = a decoy with other frozen-vocabulary words swapped in (same shape).
Fresh sessions rate 1–7. Forced rows must beat both decoy classes by a margin set
from round 2's baseline (T 4.8, D 1.9, W 2.8 → margins 2.9 and 2.0; default
threshold is half of each, configurable).
"""
from __future__ import annotations

import json
import random
import re
from pathlib import Path

from .vocab import Vocab
from .generate import vocab_table, parse_json, _tmpl
from .providers import LoggedModel

ROUND2_BASELINE = {"T": 4.8, "D": 1.9, "W": 2.8}
DEFAULT_MARGIN_FRACTION = 0.5

# Opposites used to flip a sentence's direction mechanically when no model is available.
FLIPS = [("easier", "harder"), ("less", "more"), ("rises", "falls"), ("gathers", "scatters"),
         ("culminate", "cancel"), ("never ungathers", "always ungathers"), ("shares", "does not share"),
         ("already there", "out of reach"), ("build each other up", "wear each other down"),
         ("draws you toward", "pushes you away from"), ("receptive", "resistant"), ("freely", "hard")]

SWAPPABLE = ["Movement M", "Desire", "Vibrance", "Vibration", "Expansion", "Appreciation", "Frequency",
             "Current", "Attraction", "Vortex", "Culmination", "Intuition", "Tune", "imagination"]


def flip_sentence(s: str) -> str:
    out = s
    for a, b in FLIPS:
        if re.search(rf"\b{a}\b", out):
            return re.sub(rf"\b{a}\b", b, out, count=1)
        if re.search(rf"\b{b}\b", out):
            return re.sub(rf"\b{b}\b", a, out, count=1)
    return "It is not the case that " + s[0].lower() + s[1:]


def swap_words(s: str, rng: random.Random) -> str:
    present = [w for w in SWAPPABLE if w in s]
    if not present:
        return s
    target = rng.choice(present)
    repl = rng.choice([w for w in SWAPPABLE if w != target and w not in s] or [w for w in SWAPPABLE if w != target])
    return s.replace(target, repl, 1)


def build_list(forced: list[dict], seed: int = 0, flipper=None) -> tuple[list[dict], dict[str, dict]]:
    """Returns (statements shuffled with ids S01.., key {Sxx: {record_id, version}})."""
    rng = random.Random(seed)
    items = []
    for r in forced:
        t = r["consensus"]["reflected_sentence"]
        d = flipper(t) if flipper else flip_sentence(t)
        w = swap_words(t, rng)
        items += [(r["record_id"], "T", t), (r["record_id"], "D", d), (r["record_id"], "W", w)]
    rng.shuffle(items)
    statements, key = [], {}
    for i, (rid, ver, text) in enumerate(items, 1):
        sid = f"S{i:02d}"
        statements.append({"id": sid, "text": text})
        key[sid] = {"record_id": rid, "version": ver}
    return statements, key


def rate(statements: list[dict], raters: list[LoggedModel], v: Vocab) -> dict[str, dict[str, int]]:
    block = "\n".join(f"{s['id']}: {s['text']}" for s in statements)
    prompt = _tmpl("rater.md").format(vocab_table=vocab_table(v), statements=block)
    out = {}
    for r in raters:
        try:
            o = parse_json(r(prompt, role="rater", temperature=0.0)) or {}
        except RuntimeError as e:
            out[r.spec.name] = {"error": str(e)}
            continue
        out[r.spec.name] = {k: int(x) for k, x in (o.get("ratings") or {}).items() if str(x).isdigit()}
    return out


def score(ratings: dict[str, dict[str, int]], key: dict[str, dict], controls: set[str] = frozenset(),
          margin_fraction: float = DEFAULT_MARGIN_FRACTION) -> dict:
    """Per-rater discrimination on controls, then T vs D and T vs W margins over valid raters."""
    valid = {}
    for rater, rs in ratings.items():
        if "error" in rs:
            continue
        # a rater that gives nearly everything the same score is excluded (round 2 rule)
        if len(set(rs.values())) <= 1:
            continue
        if controls:
            ok = True
            for rid in controls:
                t = [rs[s] for s, k in key.items() if k["record_id"] == rid and k["version"] == "T" and s in rs]
                dw = [rs[s] for s, k in key.items() if k["record_id"] == rid and k["version"] != "T" and s in rs]
                if t and dw and not (t[0] > max(dw)):
                    ok = False
            if not ok:
                continue
        valid[rater] = rs
    sums = {"T": [], "D": [], "W": []}
    tops = 0
    n_sets = 0
    for rid in {k["record_id"] for k in key.values()}:
        for rater, rs in valid.items():
            vals = {k["version"]: rs[s] for s, k in key.items() if k["record_id"] == rid and s in rs}
            if {"T", "D", "W"} <= set(vals):
                n_sets += 1
                for ver in sums:
                    sums[ver].append(vals[ver])
                if vals["T"] > vals["D"] and vals["T"] > vals["W"]:
                    tops += 1
    mean = {k: (sum(x) / len(x) if x else None) for k, x in sums.items()}
    margin_d = (mean["T"] - mean["D"]) if mean["T"] is not None and mean["D"] is not None else None
    margin_w = (mean["T"] - mean["W"]) if mean["T"] is not None and mean["W"] is not None else None
    need_d = (ROUND2_BASELINE["T"] - ROUND2_BASELINE["D"]) * margin_fraction
    need_w = (ROUND2_BASELINE["T"] - ROUND2_BASELINE["W"]) * margin_fraction
    passed = margin_d is not None and margin_w is not None and margin_d >= need_d and margin_w >= need_w
    return {"valid_raters": sorted(valid), "mean": mean, "margin_vs_D": margin_d, "margin_vs_W": margin_w,
            "required_margins": {"D": need_d, "W": need_w}, "T_tops_set": f"{tops}/{n_sets}",
            "passed": passed, "curated": not passed}
