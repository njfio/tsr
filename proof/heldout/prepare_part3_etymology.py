#!/usr/bin/env python3
"""Prepare Part 3 etymology coding packet from frozen OpenStax University Physics Key Terms.

Default mode fetches all 22 chapters' modules from the frozen OpenStax GitHub bundle
referenced in ``proof/heldout/openstax_fetch_manifest.json``, extracts ``<glossary><definition><term>``
headwords (never ``<meaning>`` prose), applies deterministic exclusions C1-C3 per
``proof/heldout/PREREGISTRATION.md``, draws 40 control words with ``seed = 20261113``,
pools them with ``targets_10`` and ``ledger_physics_35``, and writes:

- ``proof/heldout/openstax_key_terms_raw.csv``
- ``proof/heldout/control_exclusion_log.csv``
- ``proof/heldout/word_coding_key.csv``
- ``proof/heldout/word_coding_packet.csv``
- ``proof/heldout/etymology_coding_prompt.md``

With ``--verify-offline``, makes zero network calls, replays exclusions/sampling/pooling
from ``openstax_key_terms_raw.csv``, and asserts byte-for-byte parity plus hygiene checks.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import random
import re
import sys
from typing import Iterable
import urllib.request
import xml.etree.ElementTree as ET


HELDOUT_DIR = Path(__file__).resolve().parent
PROOF_DIR = HELDOUT_DIR.parent
REPO_ROOT = PROOF_DIR.parent

MANIFEST_PATH = HELDOUT_DIR / "openstax_fetch_manifest.json"
LEDGER_PATH = PROOF_DIR / "etymology" / "ledger_80.json"

RAW_TERMS_CSV = HELDOUT_DIR / "openstax_key_terms_raw.csv"
EXCLUSION_LOG_CSV = HELDOUT_DIR / "control_exclusion_log.csv"
WORD_KEY_CSV = HELDOUT_DIR / "word_coding_key.csv"
WORD_PACKET_CSV = HELDOUT_DIR / "word_coding_packet.csv"
CODING_PROMPT_MD = HELDOUT_DIR / "etymology_coding_prompt.md"

PREREGISTRATION_COMMIT_SHA = "463ad9f93c8a276b1e0d9ee497198dfa2169d079"
OPENSTAX_ATTRIBUTION = "Access for free at https://openstax.org — Licensed under CC BY 4.0."
SAMPLE_SEED = 20261113
CONTROL_SAMPLE_SIZE = 40

TARGETS_10: tuple[str, ...] = (
    "acceleration",
    "density",
    "energy",
    "force",
    "mass",
    "space",
    "speed",
    "time",
    "velocity",
    "volume",
)

# Hex-encoded repo hygiene substrings (kept hex-encoded so source files remain clean).
_FORBIDDEN_SUBSTRINGS_HEX: tuple[str, ...] = (
    "2f55736572732f6e6a66",       # local home path prefix
    "66696c653a2f2f2f",           # file URI scheme
    "7473725f3031",               # local repo folder name
    "2e706466",                   # document extension
    "726973657265",               # OCR artifact
    "763535",                     # superseded draft edition
    "70726f6f66203236",           # private working label
    "4e5f626c696e64",             # forbidden count identifier
    "6e5f626c696e645f7061697273", # forbidden pair identifier
    "2e67656d696e69",             # agent config directory
    "626c696e64",                 # forbidden term anywhere under proof/heldout/
)

# Hex-encoded group/book/source-leak substrings forbidden in prompt & coding packet.
_PACKET_LEAK_SUBSTRINGS_HEX: tuple[str, ...] = (
    "746172676574",                               # group label 1
    "636f6e74726f6c",                             # group label 2
    "636f72655f6c6177",                           # stratum label 1
    "7365636f6e646172795f70687973696373",         # stratum label 2
    "6e6f745f706879736963735f7465726d",           # stratum label 3
    "6c6564676572",                               # source file label
    "6f70656e73746178",                           # corpus publisher
    "756e69766572736974792070687973696373",       # textbook title
    "74686520736f7665726569676e206d6972726f72",   # manuscript title
    "776861742074686520776f726473206b6e6577",     # etymology chapter/essay title
    "747372",                                     # manuscript acronym
    "696e77617264206669727374",                   # prior kind label 1
    "6f757477617264206669727374",                 # prior kind label 2
    "686f757365686f6c64",                         # prior kind label 3
    "66616d696c79",                               # prior kind label 4
)

# Irregular/Latinate morphological pairs listed in PREREGISTRATION.md L388 and standard derivatives.
_LATINATE_PAIRS: tuple[tuple[str, str], ...] = (
    ("accelerate", "acceleration"),
    ("radiate", "radiation"),
    ("expand", "expansion"),
    ("vibrate", "vibration"),
    ("resist", "resistance"),
    ("reflect", "reflection"),
    ("resonate", "resonance"),
    ("converge", "convergence"),
    ("culminate", "culmination"),
    ("appreciate", "appreciation"),
    ("collect", "collection"),
    ("create", "creation"),
    ("direct", "direction"),
    ("distort", "distortion"),
    ("dense", "density"),
    ("gravitate", "gravity"),
    ("press", "pressure"),
    ("real", "realize"),
    ("sense", "sensation"),
    ("move", "movement"),
    ("space", "spatial"),
    ("time", "temporal"),
    ("energy", "energetic"),
    ("inertia", "inertial"),
    ("friction", "frictional"),
    ("electric", "electrical"),
    ("mass", "massive"),
)

_NEGATING_RE_PREFIXES: tuple[str, ...] = ("non", "un", "in", "im", "re")

# Ordered longest-first; only strip when stem >= 4 characters (and silent-e guardrails apply).
_STANDARD_SUFFIXES: tuple[str, ...] = (
    "ational",
    "ation",
    "ition",
    "ness",
    "ment",
    "ance",
    "ence",
    "ical",
    "tion",
    "ion",
    "ing",
    "est",
    "ity",
    "ive",
    "al",
    "ic",
    "or",
    "er",
    "ed",
    "es",
    "ly",
    "d",
    "s",
    "y",
)


@dataclass(frozen=True)
class RawKeyTermRow:
    volume: int
    chapter: int
    chapter_title: str
    module_id: str
    term_idx: int
    raw_term: str
    is_lowercase_single_word: bool
    source_url: str
    retrieved_utc: str
    preregistration_commit_sha: str


def _decode_hex_list(hex_items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(bytes.fromhex(h).decode("utf-8") for h in hex_items)


def _local_name(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def _collapse_ws(text: str) -> str:
    return " ".join(text.split())


def _load_manifest() -> dict:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("preregistration_commit_sha") != PREREGISTRATION_COMMIT_SHA:
        raise RuntimeError(
            f"Manifest preregistration_commit_sha mismatch: {manifest.get('preregistration_commit_sha')}"
        )
    if manifest.get("attribution") != OPENSTAX_ATTRIBUTION:
        raise RuntimeError(f"Unexpected attribution in manifest: {manifest.get('attribution')!r}")
    if len(manifest.get("chapters", [])) != 22:
        raise RuntimeError(f"Expected 22 chapters in manifest, got {len(manifest.get('chapters', []))}")
    return manifest


def _load_ledger() -> tuple[list[str], dict[str, dict], list[str]]:
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    rows = ledger.get("words")
    if not isinstance(rows, list) or len(rows) != 80:
        raise RuntimeError(f"Expected 80 words in ledger_80.json, got {len(rows) if isinstance(rows, list) else type(rows)}")
    by_word: dict[str, dict] = {}
    all_words: list[str] = []
    physics_35: list[str] = []
    for row in rows:
        w = row["word"].strip()
        if not re.fullmatch(r"[a-z]+", w):
            raise RuntimeError(f"Unexpected non-lowercase word in ledger_80.json: {w!r}")
        if w in by_word:
            raise RuntimeError(f"Duplicate word in ledger_80.json: {w!r}")
        by_word[w] = row
        all_words.append(w)
        if row["physics_stratum"] in ("core_law", "secondary_physics"):
            physics_35.append(w)
    if len(physics_35) != 35:
        raise RuntimeError(f"Expected 35 physics-eligible ledger words, got {len(physics_35)}")
    return all_words, by_word, physics_35


def _fetch_module_cnxml(url: str, expected_sha256: str | None) -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "tsr-heldout-part3-prep/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        status = getattr(resp, "status", 200)
        if status != 200:
            raise RuntimeError(f"HTTP {status} fetching {url}")
        raw_bytes = resp.read()
    digest = hashlib.sha256(raw_bytes).hexdigest()
    if expected_sha256 is not None and digest != expected_sha256:
        raise RuntimeError(f"SHA-256 mismatch for {url}: got {digest}, expected {expected_sha256}")
    retrieved_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return raw_bytes, retrieved_utc


def _extract_glossary_terms(xml_bytes: bytes, url: str) -> list[str]:
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as exc:
        raise RuntimeError(f"XML parse error in {url}: {exc}") from exc

    terms: list[str] = []
    for elem in root.iter():
        if _local_name(elem.tag) != "glossary":
            continue
        for child in elem.iter():
            if _local_name(child.tag) == "term":
                term_text = _collapse_ws("".join(child.itertext()))
                if not term_text:
                    raise RuntimeError(f"Empty <term> element inside <glossary> in {url}")
                terms.append(term_text)
    return terms


def fetch_raw_key_terms(manifest: dict) -> list[RawKeyTermRow]:
    bundle_repo = manifest["bundle_repo"]
    bundle_sha = manifest["bundle_commit_sha"]
    sha_map: dict[str, str] = manifest.get("fetched_urls_sha256", {})

    jobs: list[tuple[int, int, str, str, str, str | None]] = []
    for ch in manifest["chapters"]:
        vol = int(ch["volume"])
        chap_num = int(ch["chapter"])
        chap_title = str(ch["chapter_title"])
        for mod_id in ch["module_ids"]:
            url = (
                f"https://raw.githubusercontent.com/{bundle_repo}/{bundle_sha}"
                f"/modules/{mod_id}/index.cnxml"
            )
            jobs.append((vol, chap_num, chap_title, str(mod_id), url, sha_map.get(url)))

    def _run_job(job: tuple[int, int, str, str, str, str | None]) -> list[RawKeyTermRow]:
        vol, chap_num, chap_title, mod_id, url, expected_sha = job
        raw_bytes, retrieved_utc = _fetch_module_cnxml(url, expected_sha)
        terms = _extract_glossary_terms(raw_bytes, url)
        rows: list[RawKeyTermRow] = []
        for idx, raw_term in enumerate(terms, start=1):
            is_lower = bool(re.fullmatch(r"[a-z]+", raw_term))
            rows.append(
                RawKeyTermRow(
                    volume=vol,
                    chapter=chap_num,
                    chapter_title=chap_title,
                    module_id=mod_id,
                    term_idx=idx,
                    raw_term=raw_term,
                    is_lowercase_single_word=is_lower,
                    source_url=url,
                    retrieved_utc=retrieved_utc,
                    preregistration_commit_sha=PREREGISTRATION_COMMIT_SHA,
                )
            )
        return rows

    all_rows: list[RawKeyTermRow] = []
    with ThreadPoolExecutor(max_workers=12) as pool:
        for mod_rows in pool.map(_run_job, jobs):
            all_rows.extend(mod_rows)

    if not all_rows:
        raise RuntimeError("Fetched zero OpenStax glossary key terms across all 22 chapters")
    return all_rows


def load_raw_key_terms_csv(path: Path) -> list[RawKeyTermRow]:
    rows: list[RawKeyTermRow] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for rec in reader:
            flag = rec["is_lowercase_single_word"].strip()
            if flag not in ("true", "false"):
                raise RuntimeError(f"Invalid boolean flag in {path}: {flag!r}")
            rows.append(
                RawKeyTermRow(
                    volume=int(rec["volume"]),
                    chapter=int(rec["chapter"]),
                    chapter_title=rec["chapter_title"],
                    module_id=rec["module_id"],
                    term_idx=int(rec["term_idx"]),
                    raw_term=rec["raw_term"],
                    is_lowercase_single_word=(flag == "true"),
                    source_url=rec["source_url"],
                    retrieved_utc=rec["retrieved_utc"],
                    preregistration_commit_sha=rec["preregistration_commit_sha"],
                )
            )
    return rows


def render_raw_terms_csv(rows: list[RawKeyTermRow]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(
        [
            "volume",
            "chapter",
            "chapter_title",
            "module_id",
            "term_idx",
            "raw_term",
            "is_lowercase_single_word",
            "source_url",
            "retrieved_utc",
            "preregistration_commit_sha",
        ]
    )
    for r in rows:
        writer.writerow(
            [
                r.volume,
                r.chapter,
                r.chapter_title,
                r.module_id,
                r.term_idx,
                r.raw_term,
                "true" if r.is_lowercase_single_word else "false",
                r.source_url,
                r.retrieved_utc,
                r.preregistration_commit_sha,
            ]
        )
    return buf.getvalue()


def _build_pair_map() -> dict[str, set[str]]:
    adj: dict[str, set[str]] = {}
    for a, b in _LATINATE_PAIRS:
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    return adj


_PAIR_MAP = _build_pair_map()


def _strip_suffix_once(w: str) -> set[str]:
    out: set[str] = set()
    for suf in _STANDARD_SUFFIXES:
        if not w.endswith(suf):
            continue
        # Never strip single 's' from double-s or Greek/Latin -us/-is/-os endings.
        if suf == "s" and w.endswith(("ss", "us", "is", "os")):
            continue
        if suf == "d" and w.endswith(("ed", "nd", "ld", "rd")):
            if not w.endswith(("ated", "ized", "ured", "ved", "sed", "ced", "ted")):
                continue
        base = w[: -len(suf)]
        if len(base) < 4:
            continue
        if suf == "y" and base.endswith(("e", "a", "o", "u")):
            continue
        out.add(base)
        # Silent-e restoration after consonants (e.g. gravitat+ion -> gravitate, resistiv+e -> resistive)
        if suf in ("ation", "ition", "tion", "ion", "ing", "ed", "er", "or", "ive", "ity", "al", "ic", "d", "y"):
            if base[-1] not in "aeiou":
                out.add(base + "e")
        # Consonant deduping (e.g. running -> runn -> run, stopped -> stopp -> stop)
        if suf in ("ing", "ed", "er", "est", "y") and len(base) >= 5 and base[-1] == base[-2]:
            out.add(base[:-1])
        # -ies / -ied / -ier -> -y (e.g. densities -> density, energies -> energy)
        if suf in ("es", "ed", "er", "est") and base.endswith("i") and len(base) >= 4:
            out.add(base[:-1] + "y")
    return out


def _morphological_stems(word: str) -> set[str]:
    """Generate controlled morphological stems per PREREGISTRATION.md L388 without over-stemming."""
    frontier: set[str] = {word}
    if word in _PAIR_MAP:
        frontier.update(_PAIR_MAP[word])

    # Strip at most one negating / re- prefix when remainder >= 4.
    for w in list(frontier):
        for pref in _NEGATING_RE_PREFIXES:
            if w.startswith(pref):
                rem = w[len(pref) :]
                if len(rem) >= 4:
                    frontier.add(rem)
                    if rem in _PAIR_MAP:
                        frontier.update(_PAIR_MAP[rem])

    # Bounded 2-pass suffix stripping (handles compound derivations like resistivity -> resistive -> resist
    # and gravitational -> gravitation -> gravitate -> gravity without collapsing short roots).
    stems: set[str] = set(frontier)
    pass1: set[str] = set()
    for w in frontier:
        pass1.update(_strip_suffix_once(w))
    stems.update(pass1)
    for w in pass1:
        if w in _PAIR_MAP:
            stems.update(_PAIR_MAP[w])
        for s2 in _strip_suffix_once(w):
            stems.add(s2)
            if s2 in _PAIR_MAP:
                stems.update(_PAIR_MAP[s2])
    return stems


def build_reference_stem_index(ref_words: Iterable[str]) -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for ref in sorted(set(ref_words)):
        for st in _morphological_stems(ref):
            index.setdefault(st, []).append(ref)
    return index


def classify_candidate_word(
    word: str,
    ledger_set: set[str],
    targets_set: set[str],
    ref_stem_index: dict[str, list[str]],
) -> tuple[str | None, str, str]:
    """Apply C1 -> C2 -> C3 in exact preregistered order.

    Returns ``(exclusion_code_or_None, matched_reference_word, rationale)``.
    """
    if word in ledger_set:
        return (
            "C1_IN_LEDGER_80",
            word,
            "Exact match in 80-word etymological ledger (ledger_80.json).",
        )
    if word in targets_set:
        return (
            "C2_CONFIRMED_TARGET",
            word,
            "Exact match in confirmed 10 physical quantity targets.",
        )

    cand_stems = _morphological_stems(word)
    matched_refs: list[str] = []
    matched_stems: list[str] = []
    for st in sorted(cand_stems):
        if st in ref_stem_index:
            for ref in ref_stem_index[st]:
                if ref not in matched_refs:
                    matched_refs.append(ref)
                if st not in matched_stems:
                    matched_stems.append(st)

    if matched_refs:
        # Prefer direct pair match or longest shared stem for deterministic reporting.
        matched_refs.sort()
        primary_ref = matched_refs[0]
        return (
            "C3_MORPHOLOGICAL_VARIANT",
            primary_ref,
            f"Shared morphological/Latinate root ({', '.join(sorted(matched_stems)[:3])}) with reference word '{primary_ref}'.",
        )
    return None, "", ""


def run_c3_self_tests(ledger_set: set[str], targets_set: set[str], ref_stem_index: dict[str, list[str]]) -> None:
    """Assert expected C3 inclusion/non-overmatching behavior on synthetic audit edge cases."""
    must_exclude = {
        "radiation": {"radiate", "radiation"},
        "resistor": {"resist", "resistance"},
        "resistivity": {"resist", "resistance"},
        "reflective": {"reflect", "reflection"},
        "spatial": {"space"},
        "temporal": {"time"},
        "energetic": {"energy"},
        "inertial": {"inertia"},
        "frictional": {"friction"},
        "gravitational": {"gravitate", "gravity"},
        "massive": {"mass"},
    }
    for word, allowed_refs in must_exclude.items():
        code, ref, _ = classify_candidate_word(word, ledger_set, targets_set, ref_stem_index)
        if code != "C3_MORPHOLOGICAL_VARIANT" or ref not in allowed_refs:
            raise AssertionError(
                f"C3 self-test failed for {word!r}: got ({code}, {ref!r}), expected C3 matching one of {sorted(allowed_refs)}"
            )

    must_keep = (
        "wavelength",
        "refraction",
        "ideal",
        "moment",
        "period",
        "compressibility",
        "displacement",
        "equilibrium",
    )
    for word in must_keep:
        code, ref, _ = classify_candidate_word(word, ledger_set, targets_set, ref_stem_index)
        if code is not None:
            raise AssertionError(f"C3 over-match for {word!r}: matched ({code}, {ref!r})")


def render_exclusion_log_csv(exclusions: list[tuple[str, str, str, str]]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(["word", "exclusion_code", "matched_reference_word", "rationale", "preregistration_commit_sha"])
    for word, code, ref, rationale in exclusions:
        writer.writerow([word, code, ref, rationale, PREREGISTRATION_COMMIT_SHA])
    return buf.getvalue()


def render_word_key_csv(
    shuffled_pool: list[str],
    targets_set: set[str],
    controls_set: set[str],
    ledger_physics_set: set[str],
    ledger_by_word: dict[str, dict],
    word_chapters: dict[str, list[tuple[int, int]]],
) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(
        [
            "item_id",
            "word",
            "in_targets_10",
            "in_controls_40",
            "in_ledger_physics_35",
            "ledger_stratum",
            "ledger_kind",
            "control_openstax_chapters",
            "preregistration_commit_sha",
        ]
    )
    for idx, word in enumerate(shuffled_pool, start=1):
        item_id = f"W{idx:03d}"
        in_targets = word in targets_set
        in_controls = word in controls_set
        in_l35 = word in ledger_physics_set
        l_row = ledger_by_word.get(word)
        stratum = str(l_row["physics_stratum"]) if l_row is not None else ""
        kind = str(l_row["kind"]) if l_row is not None else ""
        chap_str = ""
        if in_controls:
            chaps = sorted(set(word_chapters.get(word, [])))
            chap_str = ";".join(f"V{v}C{c}" for v, c in chaps)
        writer.writerow(
            [
                item_id,
                word,
                "true" if in_targets else "false",
                "true" if in_controls else "false",
                "true" if in_l35 else "false",
                stratum,
                kind,
                chap_str,
                PREREGISTRATION_COMMIT_SHA,
            ]
        )
    return buf.getvalue()


def render_word_packet_csv(shuffled_pool: list[str]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(["item_id", "word"])
    for idx, word in enumerate(shuffled_pool, start=1):
        writer.writerow([f"W{idx:03d}", word])
    return buf.getvalue()


def render_coding_prompt_md(shuffled_pool: list[str]) -> str:
    lines: list[str] = [
        "# Historical Etymology Coding Packet (Part 3)",
        "",
        f"- **preregistration_commit_sha:** `{PREREGISTRATION_COMMIT_SHA}`",
        "- **source_coverage:** `single-source` (`https://www.etymonline.com` only)",
        f"- **item_count:** `{len(shuffled_pool)}` (`W001`..`W{len(shuffled_pool):03d}`)",
        "",
        "## Instructions",
        "",
        "1. Work in a fresh standalone session without reading repository files or external project notes.",
        f"2. Code all `{len(shuffled_pool)}` English words (`W001`..`W{len(shuffled_pool):03d}`) in the exact order listed below. Do not sort, skip, regroup, or infer categories across items.",
        "3. Consult **only** `https://www.etymonline.com/word/<word>` for each item (`source_coverage = \"single-source\"`). Use the entry's documented English attestation history (earliest attested century/date and semantic evolution).",
        "4. Classify each word's historical semantic direction into exact category `direction_class` using these four definitions:",
        "   - `\"person_first\"`: The word's earliest attested sense in English refers to a human or personal state, action, feeling, intention, character, or interpersonal capacity, and any technical physical or scientific quantity/phenomenon sense appears strictly later.",
        "   - `\"physics_first\"`: The word's earliest attested sense in English refers to an external material, spatial, mechanical, astronomical, or physical-world object, phenomenon, or measure, and any personal or psychological sense appears strictly later.",
        "   - `\"both_from_start\"`: Both human/personal senses and external material/spatial/physical senses appear contemporaneously from the word's earliest attestation in English (neither strictly precedes the other).",
        "   - `\"no_person_sense\"`: Attested as a material, spatial, technical, or mathematical term without an established personal or psychological state sense in `etymonline.com`.",
        "5. **Strict Copyright & Attribution Rule:** **NEVER** quote, copy verbatim, or closely paraphrase prose definitions or full sentences from `etymonline.com`. Record **only**:",
        "   - the exact URL (`https://www.etymonline.com/word/<word>`),",
        "   - the ISO UTC date checked (`YYYY-MM-DD`),",
        "   - a brief earliest-attestation date + 2-4 word non-quoted category tag for `earliest_person_sense` (or `\"none\"` when absent),",
        "   - a brief earliest-attestation date + 2-4 word non-quoted category tag for `earliest_physics_sense`, and",
        "   - `direction_class`.",
        f"6. Return **ONLY** a valid JSON array of `{len(shuffled_pool)}` objects in exact order `W001`..`W{len(shuffled_pool):03d}` with exact keys:",
        "",
        "```json",
        "[",
        "  {",
        "    \"item_id\": \"W001\",",
        "    \"word\": \"<word>\",",
        "    \"etymonline_url\": \"https://www.etymonline.com/word/<word>\",",
        "    \"etymonline_retrieved_utc\": \"<YYYY-MM-DD>\",",
        "    \"earliest_person_sense\": \"<date + 2-4 word non-quoted tag | none>\",",
        "    \"earliest_physics_sense\": \"<date + 2-4 word non-quoted tag>\",",
        "    \"direction_class\": \"<person_first | physics_first | both_from_start | no_person_sense>\"",
        "  }",
        "]",
        "```",
        "",
        "## Items (W001..W078)",
        "",
        "| item_id | word | etymonline_url |",
        "| :--- | :--- | :--- |",
    ]
    for idx, word in enumerate(shuffled_pool, start=1):
        lines.append(f"| `W{idx:03d}` | `{word}` | `https://www.etymonline.com/word/{word}` |")
    lines.append("")
    return "\n".join(lines)


def check_hygiene(texts_by_name: dict[str, str], packet_texts_by_name: dict[str, str]) -> None:
    forbidden = _decode_hex_list(_FORBIDDEN_SUBSTRINGS_HEX)
    for name, text in texts_by_name.items():
        lowered = text.lower()
        for sub in forbidden:
            if sub.lower() in lowered:
                raise RuntimeError(f"Hygiene failure in {name}: forbidden substring found (hex {sub.encode('utf-8').hex()})")

    # Also verify no file under proof/heldout/ contains the hex-guarded forbidden substring.
    guarded_token = bytes.fromhex("626c696e64").decode("utf-8")
    for p in sorted(HELDOUT_DIR.rglob("*")):
        if not p.is_file():
            continue
        if p.suffix.lower() in (".pyc", ".png", ".jpg", ".gz"):
            continue
        try:
            content = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if guarded_token in content.lower():
            raise RuntimeError(f"Hygiene failure in {p.relative_to(REPO_ROOT)}: forbidden token found")

    packet_forbidden = _decode_hex_list(_PACKET_LEAK_SUBSTRINGS_HEX)
    for name, text in packet_texts_by_name.items():
        lowered = text.lower()
        for sub in packet_forbidden:
            if sub.lower() in lowered:
                raise RuntimeError(
                    f"Packet/prompt leak check failed in {name}: forbidden term (hex {sub.encode('utf-8').hex()})"
                )


def process_pipeline(raw_rows: list[RawKeyTermRow], verbose: bool = True) -> dict[str, object]:
    ledger_80_list, ledger_by_word, ledger_physics_list = _load_ledger()
    ledger_80_set = set(ledger_80_list)
    targets_set = set(TARGETS_10)
    ledger_physics_set = set(ledger_physics_list)

    ref_words = ledger_80_set | targets_set
    ref_stem_index = build_reference_stem_index(ref_words)
    run_c3_self_tests(ledger_80_set, targets_set, ref_stem_index)

    # Deduplicate raw terms strictly matching ^[a-z]+$ verbatim, tracking OpenStax chapters.
    word_chapters: dict[str, list[tuple[int, int]]] = {}
    for row in raw_rows:
        expected_flag = bool(re.fullmatch(r"[a-z]+", row.raw_term))
        if expected_flag != row.is_lowercase_single_word:
            raise RuntimeError(
                f"Inconsistent is_lowercase_single_word for {row.raw_term!r}: {row.is_lowercase_single_word}"
            )
        if expected_flag:
            word_chapters.setdefault(row.raw_term, []).append((row.volume, row.chapter))

    candidates_sorted = sorted(word_chapters.keys())
    if verbose:
        print(f"Total raw OpenStax glossary terms extracted: {len(raw_rows)}")
        print(f"Unique lowercase single-word candidates (^[a-z]+$ verbatim): {len(candidates_sorted)}")
        print("All candidates before exclusion:")
        print("  " + ", ".join(candidates_sorted))

    exclusions: list[tuple[str, str, str, str]] = []
    eligible_controls: list[str] = []
    for word in candidates_sorted:
        code, ref, rationale = classify_candidate_word(word, ledger_80_set, targets_set, ref_stem_index)
        if code is not None:
            exclusions.append((word, code, ref, rationale))
        else:
            eligible_controls.append(word)

    if verbose:
        print(f"\nExcluded candidates ({len(exclusions)}):")
        for word, code, ref, rationale in exclusions:
            print(f"  - {word}: {code} -> {ref} | {rationale}")
        print(f"\nSurviving eligible controls ({len(eligible_controls)}):")
        print("  " + ", ".join(eligible_controls))

    if len(eligible_controls) < CONTROL_SAMPLE_SIZE:
        raise RuntimeError(
            f"Only {len(eligible_controls)} eligible controls survived; need at least {CONTROL_SAMPLE_SIZE}"
        )

    controls_40 = random.Random(SAMPLE_SEED).sample(eligible_controls, CONTROL_SAMPLE_SIZE)
    controls_set = set(controls_40)

    if controls_set & ledger_80_set:
        raise RuntimeError(f"Control sample overlaps ledger_80: {sorted(controls_set & ledger_80_set)}")
    if controls_set & targets_set:
        raise RuntimeError(f"Control sample overlaps targets_10: {sorted(controls_set & targets_set)}")

    pool_sorted = sorted(targets_set | controls_set | ledger_physics_set)
    overlap_targets_ledger35 = sorted(targets_set & ledger_physics_set)
    expected_pool_size = len(ledger_physics_set) + len(targets_set - ledger_physics_set) + CONTROL_SAMPLE_SIZE
    if len(pool_sorted) != expected_pool_size or len(pool_sorted) != 78:
        raise RuntimeError(
            f"Expected pooled coding set size 78 (35 + 3 + 40), got {len(pool_sorted)} "
            f"(overlap={overlap_targets_ledger35})"
        )

    shuffled_pool = list(pool_sorted)
    random.Random(SAMPLE_SEED).shuffle(shuffled_pool)

    if verbose:
        print(f"\nSampled controls_40 (seed={SAMPLE_SEED}):")
        print("  " + ", ".join(controls_40))
        print(
            f"\nUnified pool size: {len(shuffled_pool)} "
            f"(ledger_physics_35={len(ledger_physics_set)}, targets_10={len(targets_set)}, "
            f"overlap={len(overlap_targets_ledger35)} {overlap_targets_ledger35}, controls_40={len(controls_40)})"
        )

    exclusion_csv = render_exclusion_log_csv(exclusions)
    word_key_csv = render_word_key_csv(
        shuffled_pool=shuffled_pool,
        targets_set=targets_set,
        controls_set=controls_set,
        ledger_physics_set=ledger_physics_set,
        ledger_by_word=ledger_by_word,
        word_chapters=word_chapters,
    )
    word_packet_csv = render_word_packet_csv(shuffled_pool)
    coding_prompt_md = render_coding_prompt_md(shuffled_pool)

    return {
        "candidates_sorted": candidates_sorted,
        "exclusions": exclusions,
        "eligible_controls": eligible_controls,
        "controls_40": controls_40,
        "shuffled_pool": shuffled_pool,
        "overlap_targets_ledger35": overlap_targets_ledger35,
        "exclusion_csv": exclusion_csv,
        "word_key_csv": word_key_csv,
        "word_packet_csv": word_packet_csv,
        "coding_prompt_md": coding_prompt_md,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verify-offline",
        action="store_true",
        help="Replay pipeline offline from openstax_key_terms_raw.csv and verify byte-for-byte parity & hygiene.",
    )
    args = parser.parse_args(argv)

    manifest = _load_manifest()

    if args.verify_offline:
        for req_path in (RAW_TERMS_CSV, EXCLUSION_LOG_CSV, WORD_KEY_CSV, WORD_PACKET_CSV, CODING_PROMPT_MD):
            if not req_path.is_file():
                raise RuntimeError(f"Missing required artifact for --verify-offline: {req_path}")
        raw_rows = load_raw_key_terms_csv(RAW_TERMS_CSV)
        out = process_pipeline(raw_rows, verbose=False)

        expected_files = {
            EXCLUSION_LOG_CSV: str(out["exclusion_csv"]),
            WORD_KEY_CSV: str(out["word_key_csv"]),
            WORD_PACKET_CSV: str(out["word_packet_csv"]),
            CODING_PROMPT_MD: str(out["coding_prompt_md"]),
        }
        for path, generated_text in expected_files.items():
            on_disk = path.read_text(encoding="utf-8")
            if on_disk != generated_text:
                raise RuntimeError(f"Offline verification mismatch (not byte-for-byte identical): {path}")

        raw_csv_text = RAW_TERMS_CSV.read_text(encoding="utf-8")
        check_hygiene(
            texts_by_name={
                RAW_TERMS_CSV.name: raw_csv_text,
                EXCLUSION_LOG_CSV.name: str(out["exclusion_csv"]),
                WORD_KEY_CSV.name: str(out["word_key_csv"]),
                WORD_PACKET_CSV.name: str(out["word_packet_csv"]),
                CODING_PROMPT_MD.name: str(out["coding_prompt_md"]),
                Path(__file__).name: Path(__file__).read_text(encoding="utf-8"),
            },
            packet_texts_by_name={
                WORD_PACKET_CSV.name: str(out["word_packet_csv"]),
                CODING_PROMPT_MD.name: str(out["coding_prompt_md"]),
            },
        )
        print(
            "OFFLINE_VERIFY_OK: "
            f"raw_terms={len(raw_rows)}, candidates={len(out['candidates_sorted'])}, "
            f"excluded={len(out['exclusions'])}, eligible={len(out['eligible_controls'])}, "
            f"controls={len(out['controls_40'])}, pool={len(out['shuffled_pool'])}, "
            f"bytes_prompt={len(CODING_PROMPT_MD.read_bytes())}"
        )
        return 0

    raw_rows = fetch_raw_key_terms(manifest)
    raw_csv_text = render_raw_terms_csv(raw_rows)
    out = process_pipeline(raw_rows, verbose=True)

    check_hygiene(
        texts_by_name={
            RAW_TERMS_CSV.name: raw_csv_text,
            EXCLUSION_LOG_CSV.name: str(out["exclusion_csv"]),
            WORD_KEY_CSV.name: str(out["word_key_csv"]),
            WORD_PACKET_CSV.name: str(out["word_packet_csv"]),
            CODING_PROMPT_MD.name: str(out["coding_prompt_md"]),
            Path(__file__).name: Path(__file__).read_text(encoding="utf-8"),
        },
        packet_texts_by_name={
            WORD_PACKET_CSV.name: str(out["word_packet_csv"]),
            CODING_PROMPT_MD.name: str(out["coding_prompt_md"]),
        },
    )

    RAW_TERMS_CSV.write_text(raw_csv_text, encoding="utf-8")
    EXCLUSION_LOG_CSV.write_text(str(out["exclusion_csv"]), encoding="utf-8")
    WORD_KEY_CSV.write_text(str(out["word_key_csv"]), encoding="utf-8")
    WORD_PACKET_CSV.write_text(str(out["word_packet_csv"]), encoding="utf-8")
    CODING_PROMPT_MD.write_text(str(out["coding_prompt_md"]), encoding="utf-8")

    # Re-run full file-scan hygiene check after writing artifacts to disk.
    check_hygiene(
        texts_by_name={},
        packet_texts_by_name={
            WORD_PACKET_CSV.name: WORD_PACKET_CSV.read_text(encoding="utf-8"),
            CODING_PROMPT_MD.name: CODING_PROMPT_MD.read_text(encoding="utf-8"),
        },
    )
    print("\nWrote all Part 3 preparation artifacts cleanly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
