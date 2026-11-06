"""The frozen vocabulary: word map typed by Map row, lint for units, NEW-word check."""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
VOCAB_PATH = ROOT / "vocab" / "frozen.yaml"
LEXICON_PATH = ROOT / "vocab" / "resistance_lexicon.yaml"

OPERATORS = {"×", "x", "*", "÷", "/", "=", "+", "−", "-", "(", ")", "^", "²", "²"}


class Vocab:
    def __init__(self, path: Path = VOCAB_PATH):
        with open(path) as f:
            self.raw = yaml.safe_load(f)
        self.version = self.raw.get("version")
        self.mirror = [(m["physical"], m["nonphysical"], m["role"], m) for m in self.raw["mirror"]]
        self.diagonal = self.raw.get("diagonal", [])
        self.extra = {e["word"]: e for e in self.raw.get("nonphysical_extra", [])}
        self.forbidden = {w.lower() for w in self.raw.get("forbidden_nonphysical", [])}
        self.unit_words = {w.lower() for w in self.raw.get("unit_words", [])}
        self.magnitude_words = {w.lower() for w in self.raw.get("magnitude_words", [])}

    # ---- the word map ---------------------------------------------------
    def word_map(self) -> dict[str, str]:
        """physical -> nonphysical, first (straight-mirror) partner, as tsr_formal.word_map."""
        m: dict[str, str] = {}
        for phys, non, role, _ in self.mirror:
            m.setdefault(phys, non)
        return m

    def nonphysical_words(self) -> set[str]:
        words = {non for _, non, _, _ in self.mirror}
        words |= set(self.extra)
        words |= {"M", "C", "E", "C²", "C^2"}
        return words

    def physical_words(self) -> set[str]:
        return {phys for phys, _, _, _ in self.mirror}

    def typed_clashes(self, extra_rows: list[tuple[str, str, str]] = ()) -> dict:
        """Mirror-twice: typed by Map row, the map must be one-to-one.

        Returns {(nonphysical, role): [physical, ...]} for every clash.
        """
        typed = defaultdict(set)
        for phys, non, role, _ in self.mirror:
            typed[(non, role)].add(phys)
        for phys, non, role in extra_rows:
            typed[(non, role)].add(phys)
        return {k: sorted(v) for k, v in typed.items() if len(v) > 1}

    def many_to_one(self, extra_rows: list[tuple[str, str, str]] = ()) -> dict:
        back = defaultdict(set)
        for phys, non, role, _ in self.mirror:
            back[non].add((phys, role))
        for phys, non, role in extra_rows:
            back[non].add((phys, role))
        return {n: sorted(p) for n, p in back.items() if len(p) > 1}

    # ---- lint (C5) and NEW-word check (C4) ------------------------------
    _num = re.compile(r"(?<![A-Za-z])(\d+([.,]\d+)?|½|¼|¾|√)")

    def lint_formula(self, formula: str) -> list[str]:
        """Units don't cross. Numerals (except C² / C^2), unit words, magnitude words are errors."""
        errs = []
        f = formula.replace("C²", "C").replace("C^2", "C").replace("c²", "c")
        if self._num.search(f):
            errs.append(f"numeral in reflected formula: {formula!r}")
        low = formula.lower()
        for w in self.unit_words:
            if re.search(rf"\b{re.escape(w)}\b", low):
                errs.append(f"unit word {w!r} in reflected formula")
        for w in self.magnitude_words:
            if w in low:
                errs.append(f"magnitude word {w!r} in reflected formula")
        return errs

    _STOP = {"of", "per", "over", "the", "a", "an", "in", "through", "and", "by", "for", "to", "with", "is", "as", "its",
             "no", "partner", "unmapped", "definition", "frozen", "product", "constant", "sum", "ratio", "none", "or", "not"}
    _ALIASES = {"Movement", "Current", "M", "C", "E", "Attraction", "Vortex", "Convergence", "Culmination", "Idle", "Reflected"}

    def new_words(self, formula: str, known_physical: set[str] = frozenset()) -> list[str]:
        """Capitalized tokens of a reflected formula that are not frozen vocabulary, not a physical term the
        generator marked as unmapped, and not a symbol. This is the check for an invented TSR word
        ('Desire-field'); physical symbols and bracketed unmapped markers are not NEW words.
        """
        s = re.sub(r"\[[^\]]*\]", " ", formula)         # [angular momentum: unmapped]
        s = re.sub(r"\([^)]*\)", " ", s)                # (work)
        out = []
        known = self.nonphysical_words() | self._ALIASES
        for h in re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)+", s):   # hyphenated compounds are one word
            if h not in known and re.match(r"[A-Z]", h):
                out.append(h)
            s = s.replace(h, " ")
        for w in sorted(self.nonphysical_words() | self._ALIASES, key=len, reverse=True):
            s = re.sub(rf"(?<![A-Za-z]){re.escape(w)}(?![A-Za-z])", " ", s)
        s = re.sub(r"[×x*÷/=+−\-^²()?:;,'\"]", " ", s)
        phys = {t.lower() for name in known_physical for t in re.findall(r"[A-Za-z]+", name)}
        for t in s.split():
            if t.lower() in self._STOP or t.lower() in phys:
                continue
            if not re.match(r"[A-Z][a-z]", t):           # TSR words are capitalized words; symbols and lowercase physics are not NEW
                continue
            if t in {"Boltzmann", "Planck", "Shannon", "Yukawa", "Poynting", "Reynolds", "Fourier", "Carnot", "Gibbs"}:
                continue
            out.append(t)
        return out

    def sense_violations(self, sentence: str, formula: str = "") -> list[str]:
        """C4: senses the frozen vocabulary fixes. 'the gap' is resistance's only appearance on the nonphysical
        side; 'receptivity' is the flipped condition. Equating them, or using receptivity as a formula variable
        standing for a resistance quantity, is a new sense."""
        out = []
        low = sentence.lower()
        if re.search(r"gap\s*\(or\s+receptivity\)|receptivity\s*\(or\s+(the\s+)?gap\)|gap,?\s+or\s+receptivity|receptivity,?\s+or\s+the\s+gap", low):
            out.append("equates the gap with receptivity (they run opposite: the gap is resistance's appearance, receptivity its flip)")
        if re.search(r"(^|[=÷×/]\s*)receptivity(\s*[=÷×/]|$)", formula.strip()):
            out.append("uses receptivity as a formula variable")
        if re.search(r"receptivity\s+(is|stays)\s+(defined\s+as\s+)?the\s+ratio", low):
            out.append("defines receptivity as a ratio of quantities (a condition, not a quantity)")
        return out

    def forbidden_in(self, sentence: str) -> list[str]:
        """Deep-read traps: physical words that slipped onto the nonphysical side."""
        low = sentence.lower()
        hits = []
        for w in sorted(self.forbidden):
            if re.search(rf"\b{re.escape(w)}\b", low):
                hits.append(w)
        return hits


def load_lexicon(path: Path = LEXICON_PATH) -> dict:
    with open(path) as f:
        raw = yaml.safe_load(f)
    return {"version": raw.get("version"), "criterion_id": raw.get("criterion_id"),
            "quantities": raw["quantities"]}
