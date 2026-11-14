#!/usr/bin/env python3
"""
fetch_and_sample_laws.py — Step 2 OpenStax extraction, deterministic exclusions,
seeded stratified sampling, pooled manifest, and Stage 0 card-writer prompt builder.

Python 3.12+ standard library only (zero external packages).
"""
from __future__ import annotations

import argparse
import concurrent.futures
import csv
import datetime as dt
import hashlib
import html.parser
import io
import json
import random
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PREREGISTRATION_COMMIT_SHA = "463ad9f93c8a276b1e0d9ee497198dfa2169d079"
ATTRIBUTION = "Access for free at https://openstax.org — Licensed under CC BY 4.0."
BUNDLE_REPO = "openstax/osbooks-university-physics-bundle"
SAMPLING_SEED = 20261113
PRIMARY_TARGET_COUNT = 48

HELDOUT_DIR = Path(__file__).resolve().parent
PACKETS_DIR = HELDOUT_DIR / "packets"
MANIFEST_PATH = HELDOUT_DIR / "openstax_fetch_manifest.json"
RAW_CSV_PATH = HELDOUT_DIR / "openstax_key_equations_raw.csv"
EXCLUSION_CSV_PATH = HELDOUT_DIR / "exclusion_log.csv"
ELIGIBLE_CSV_PATH = HELDOUT_DIR / "eligible_laws_pool.csv"
RESERVE_CSV_PATH = HELDOUT_DIR / "reserve_pool.csv"
SAMPLE_MANIFEST_PATH = HELDOUT_DIR / "sample_manifest.csv"
STAGE0_PROMPT_PATH = PACKETS_DIR / "stage0_card_writer_prompt.md"

CNXML_NS = "http://cnx.rice.edu/cnxml"
MATHML_NS = "http://www.w3.org/1998/Math/MathML"
HTTP_TIMEOUT_SEC = 30
USER_AGENT = "university-physics-heldout-fetcher/1.0"

# Exact 22 included chapters per PREREGISTRATION.md Section 1.3.
INCLUDED_CHAPTERS: list[tuple[int, int, str]] = [
    (1, 1, "Units and Measurement"),
    (1, 2, "Vectors"),
    (1, 3, "Motion Along a Straight Line"),
    (1, 4, "Motion in Two and Three Dimensions"),
    (1, 5, "Newton's Laws of Motion"),
    (1, 6, "Applications of Newton's Laws"),
    (1, 7, "Work and Kinetic Energy"),
    (1, 8, "Potential Energy and Conservation of Energy"),
    (1, 9, "Linear Momentum and Collisions"),
    (1, 10, "Fixed-Axis Rotation"),
    (1, 11, "Angular Momentum"),
    (1, 12, "Static Equilibrium and Elasticity"),
    (1, 13, "Gravitation"),
    (1, 14, "Fluid Mechanics"),
    (1, 15, "Oscillations"),
    (1, 16, "Waves"),
    (1, 17, "Sound"),
    (2, 1, "Temperature and Heat"),
    (2, 2, "The Kinetic Theory of Gases"),
    (2, 3, "The First Law of Thermodynamics"),
    (2, 4, "The Second Law of Thermodynamics"),
    (3, 5, "Relativity"),
]

# Neutral standard physics descriptions & formulas for the 17 calibration rows
# matching PREREGISTRATION.md lines 124-142 without nicknames or row numbers.
CALIBRATION_17_NEUTRAL: list[tuple[int, str, str]] = [
    (
        1,
        "First postulate of special relativity (invariance of physical laws across inertial reference frames)",
        "None (qualitative physical principle)",
    ),
    (
        2,
        "Relativity of simultaneity for spatially separated events",
        r"\Delta t = \frac{\gamma v \Delta x}{c^{2}} \quad (\text{for } \Delta t' = 0)",
    ),
    (
        3,
        "Principle of relativity (absence of a preferred inertial rest frame)",
        "None (qualitative physical principle)",
    ),
    (
        4,
        "Equivalence principle and scope of inertial versus accelerating or gravitating reference frames",
        "None (qualitative physical principle)",
    ),
    (
        5,
        "Time dilation between proper time and moving-observer coordinate time",
        r"\Delta t = \gamma \Delta \tau = \frac{\Delta \tau}{\sqrt{1 - v^{2}/c^{2}}}",
    ),
    (
        6,
        "Length contraction along the direction of relative motion",
        r"L = \frac{L_{0}}{\gamma} = L_{0} \sqrt{1 - \frac{v^{2}}{c^{2}}}",
    ),
    (
        7,
        "Rest mass-energy equivalence",
        r"E_{0} = m c^{2}",
    ),
    (
        8,
        "Relativistic kinetic energy and total energy of a moving particle",
        r"K = (\gamma - 1) m c^{2}, \quad E = \gamma m c^{2}",
    ),
    (
        9,
        "Invariant speed of light as the upper speed limit for massive particles",
        r"v < c \quad (\gamma \to \infty \text{ as } v \to c \text{ for } m > 0)",
    ),
    (
        10,
        "Invariant spacetime interval unifying space and time",
        r"s^{2} = c^{2} (\Delta t)^{2} - (\Delta x)^{2} - (\Delta y)^{2} - (\Delta z)^{2}",
    ),
    (
        11,
        "Curvature of spacetime geometry induced by mass-energy",
        "None (qualitative physical principle)",
    ),
    (
        12,
        "Gravitational potential wells, gravitational redshift, and gravitational lensing of light",
        "None (qualitative physical principle)",
    ),
    (
        13,
        "Conservation of total energy in an isolated system",
        r"E_{\text{i}} = E_{\text{f}} \quad (\Delta E_{\text{sys}} = 0)",
    ),
    (
        14,
        "Newton's third law of motion (action-reaction force pair)",
        r"\vec{F}_{AB} = -\vec{F}_{BA}",
    ),
    (
        15,
        "Mass density definition relating mass, density, and volume",
        r"m = \rho V \quad (\rho = \frac{m}{V})",
    ),
    (
        16,
        "Newton's second law of motion",
        r"\vec{F}_{\text{net}} = m \vec{a}",
    ),
    (
        17,
        "Boyle's law for an isothermal fixed quantity of ideal gas",
        r"P_{1} V_{1} = P_{2} V_{2} \quad (\text{constant } T, n)",
    ),
]

GREEK_AND_SYMBOL_MAP: dict[str, str] = {
    "\u03b1": r"\alpha",
    "\u03b2": r"\beta",
    "\u03b3": r"\gamma",
    "\u03b4": r"\delta",
    "\u03b5": r"\varepsilon",
    "\u03b7": r"\eta",
    "\u03b8": r"\theta",
    "\u03ba": r"\kappa",
    "\u03bb": r"\lambda",
    "\u03bc": r"\mu",
    "\u03c0": r"\pi",
    "\u03c1": r"\rho",
    "\u03c3": r"\sigma",
    "\u03c4": r"\tau",
    "\u03c6": r"\phi",
    "\u03d5": r"\phi",
    "\u03c9": r"\omega",
    "\u0394": r"\Delta",
    "\u0392": "B",  # Greek capital Beta homoglyph in V1C16 bulk modulus
    "\u03a4": "T",  # Greek capital Tau homoglyph in V1C13 orbital period
    "\u2211": r"\sum",
    "\u222b": r"\int",
    "\u222e": r"\oint",
    "\u2202": r"\partial",
    "\u00b1": r"\pm",
    "\u2213": r"\mp",
    "\u00d7": r"\times",
    "\u00b7": r"\cdot",
    "\u2264": r"\le",
    "\u2265": r"\ge",
    "\u2261": r"\equiv",
    "\u21d4": r"\Leftrightarrow",
    "\u2192": r"\to",
    "\u2225": r"\parallel",
    "\u22a5": r"\perp",
    "\u2212": "-",
    "\u2013": "-",
    "\u2032": "'",
    "\u2026": r"\dots",
    "\u22ef": r"\cdots",
    "\u2329": r"\langle",
    "\u232a": r"\rangle",
    "\u00b0": r"^\circ",
}

FUNCTION_NAMES = {"sin", "cos", "tan", "ln", "log", "lim", "max", "min"}
PUNCT_MTEXT = {",", ";", "(", ")", "[", "]", "/", "=", "+", "-", "."}


@dataclass(frozen=True)
class RawEquationRow:
    """One extracted OpenStax Key Equations row in canonical chapter order."""

    volume: int
    chapter: int
    chapter_title: str
    row_idx: int
    eq_number: str
    description: str
    equation_latex: str
    source_url: str
    retrieved_utc: str

    def sort_key(self) -> tuple[int, int, int]:
        return (self.volume, self.chapter, self.row_idx)


@dataclass(frozen=True)
class EligibleLawRow:
    """One surviving held-out law after deterministic E1-E4 filtering."""

    law_id: str
    volume: int
    chapter: int
    chapter_title: str
    row_idx: int
    eq_number: str
    description: str
    equation_latex: str
    source_url: str
    preregistration_commit_sha: str

    def sort_key(self) -> tuple[int, int, int]:
        return (self.volume, self.chapter, self.row_idx)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _http_get_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SEC) as resp:
        return resp.read()


def _local_tag(elem: ET.Element) -> str:
    return elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag


def _norm_math_chars(text: str) -> str:
    cleaned = text.replace("\u200b", "").replace("\ufeff", "")
    return "".join(GREEK_AND_SYMBOL_MAP.get(ch, ch) for ch in cleaned)


def _join_tokens(tokens: list[str]) -> str:
    """Join LaTeX tokens with clean spacing around operators, functions, and delimiters."""
    out = ""
    for tok in tokens:
        if not tok:
            continue
        if not out:
            out = tok
            continue
        if tok in {",", ";", ")", "]", "'", r"^\circ"} or tok.startswith(("_{", "^{")):
            out += tok
        elif out.endswith(("(", "[", "{", "_{", "^{")):
            out += tok
        elif out.endswith("'") and tok in {"=", "+", "-", ",", ";", ")", "]"}:
            out += tok
        else:
            out += " " + tok
    return out


def _mml_to_tex(node: ET.Element, inline_prose: bool = False) -> str:
    """Convert a MathML element deterministically to readable human LaTeX."""
    tag = _local_tag(node)
    if tag in {"math", "mrow", "mstyle", "mtd"}:
        children = list(node)
        tokens: list[str] = []
        i = 0
        while i < len(children):
            c = children[i]
            ctag = _local_tag(c)
            if (
                ctag == "mo"
                and (c.text or "").strip() == "{"
                and i + 1 < len(children)
            ):
                nxt = children[i + 1]
                nxt_tag = _local_tag(nxt)
                table_node = None
                if nxt_tag == "mtable":
                    table_node = nxt
                elif nxt_tag == "mrow" and len(list(nxt)) == 1 and _local_tag(list(nxt)[0]) == "mtable":
                    table_node = list(nxt)[0]
                if table_node is not None:
                    case_rows = []
                    for mtr in table_node:
                        cells = [_mml_to_tex(mtd, inline_prose=inline_prose).strip() for mtd in mtr]
                        case_rows.append(" & ".join(cells).rstrip(","))
                    tokens.append(r"\begin{cases} " + r" \\ ".join(case_rows) + r" \end{cases}")
                    i += 2
                    continue
            if ctag == "mspace":
                width = c.attrib.get("width", "")
                prev_tok = tokens[-1] if tokens else ""
                next_tok = _mml_to_tex(children[i + 1], inline_prose=inline_prose) if i + 1 < len(children) else ""
                if (
                    width.startswith(("0.4", "0.5", "0.6", "1"))
                    and prev_tok not in {",", ";"}
                    and not next_tok.startswith(("(", r"\text{"))
                    and "=" in prev_tok + "".join(tokens[-6:])
                ):
                    tokens.append(";")
                i += 1
                continue
            rendered = _mml_to_tex(c, inline_prose=inline_prose).strip()
            if rendered:
                tokens.append(rendered)
            i += 1
        return _join_tokens(tokens)

    if tag == "mspace":
        return ""

    if tag == "mi":
        raw = (node.text or "").replace("\u200b", "").strip()
        if not raw:
            return ""
        if raw in FUNCTION_NAMES:
            return "\\" + raw
        return _norm_math_chars(raw)

    if tag == "mn":
        return _norm_math_chars((node.text or "").strip())

    if tag == "mo":
        return _norm_math_chars((node.text or "").strip())

    if tag == "mtext":
        raw = (node.text or "").replace("\u200b", "").replace("\ufeff", "").strip()
        if not raw:
            return ""
        if raw in {"\u0394"}:
            return r"\Delta"
        if raw in {"\u2212", "\u2013"}:
            return "-"
        if raw == "\u00b0":
            return r"^\circ"
        if raw in {",...", ",\u2026"}:
            return r", \dots"
        if raw in {"...", "\u2026"}:
            return r"\dots"
        if raw in PUNCT_MTEXT:
            return raw
        if raw in FUNCTION_NAMES:
            return "\\" + raw
        if inline_prose:
            return _norm_math_chars(raw)
        return r"\text{" + _norm_math_chars(raw) + "}"

    if tag == "mfrac":
        ch = list(node)
        if len(ch) == 2:
            num = _mml_to_tex(ch[0], inline_prose=inline_prose).strip()
            den = _mml_to_tex(ch[1], inline_prose=inline_prose).strip()
            return r"\frac{" + num + "}{" + den + "}"
        return "".join(_mml_to_tex(c, inline_prose=inline_prose) for c in ch)

    if tag == "msqrt":
        inner = _join_tokens([_mml_to_tex(c, inline_prose=inline_prose).strip() for c in node])
        return r"\sqrt{" + inner + "}"

    if tag == "msub":
        ch = list(node)
        base = _mml_to_tex(ch[0], inline_prose=inline_prose).strip()
        sub = _mml_to_tex(ch[1], inline_prose=inline_prose).strip()
        if not sub:
            return base
        return f"{base}_{{{sub}}}"

    if tag == "msup":
        ch = list(node)
        base = _mml_to_tex(ch[0], inline_prose=inline_prose).strip()
        sup = _mml_to_tex(ch[1], inline_prose=inline_prose).strip()
        if not sup:
            return base
        if sup == "'":
            return f"{base}'"
        return f"{base}^{{{sup}}}"

    if tag == "msubsup":
        ch = list(node)
        base = _mml_to_tex(ch[0], inline_prose=inline_prose).strip()
        sub = _mml_to_tex(ch[1], inline_prose=inline_prose).strip()
        sup = _mml_to_tex(ch[2], inline_prose=inline_prose).strip()
        res = base
        if sub:
            res += f"_{{{sub}}}"
        if sup:
            res += "'" if sup == "'" else f"^{{{sup}}}"
        return res

    if tag == "mover":
        ch = list(node)
        base = _mml_to_tex(ch[0], inline_prose=inline_prose).strip()
        acc = "".join(ch[1].itertext()).replace("\u200b", "").strip()
        if acc == "\u2192":
            return r"\vec{" + base + "}"
        if acc == "^":
            return r"\hat{" + base + "}"
        if acc in {"\u00af", "\u2013", "-"}:
            return (r"\bar{" + base + "}") if len(base) <= 3 else (r"\overline{" + base + "}")
        return base

    if tag == "munder":
        ch = list(node)
        base = _mml_to_tex(ch[0], inline_prose=inline_prose).strip()
        sub = _mml_to_tex(ch[1], inline_prose=inline_prose).strip()
        return f"{base}_{{{sub}}}" if sub else base

    if tag == "munderover":
        ch = list(node)
        base = _mml_to_tex(ch[0], inline_prose=inline_prose).strip()
        sub = _mml_to_tex(ch[1], inline_prose=inline_prose).strip()
        sup = _mml_to_tex(ch[2], inline_prose=inline_prose).strip()
        res = base
        if sub:
            res += f"_{{{sub}}}"
        if sup:
            res += f"^{{{sup}}}"
        return res

    if tag == "mtable":
        rows = []
        for mtr in node:
            cells = [_mml_to_tex(mtd, inline_prose=inline_prose).strip() for mtd in mtr]
            rows.append(" & ".join(cells))
        return "; ".join(rows)

    return _join_tokens([_mml_to_tex(c, inline_prose=inline_prose).strip() for c in node])


def _extract_entry_description(entry: ET.Element) -> str:
    """Render column-1 CNXML entry text with clean spacing across <newline/> and inline math."""
    parts: list[str] = []

    def walk(el: ET.Element) -> None:
        tag = _local_tag(el)
        if tag == "math":
            parts.append(_mml_to_tex(el, inline_prose=True))
            if el.tail:
                parts.append(el.tail)
            return
        if tag == "newline":
            parts.append(" ")
            if el.tail:
                parts.append(el.tail)
            return
        if el.text:
            parts.append(el.text)
        for child in el:
            walk(child)
        if el.tail:
            parts.append(el.tail)

    walk(entry)
    text = re.sub(r"\s+", " ", "".join(parts)).strip()
    return text.replace("\u2019", "'").replace("\u2018", "'")


def _extract_entry_equation_latex(entry: ET.Element) -> str:
    """Extract and normalize MathML equation(s) from a table cell."""
    maths = entry.findall(f".//{{{MATHML_NS}}}math")
    if not maths:
        maths = [el for el in entry.iter() if _local_tag(el) == "math"]
    if not maths:
        return ""
    rendered = " ".join(_mml_to_tex(m) for m in maths)
    rendered = re.sub(r"\s+", " ", rendered).strip()
    rendered = re.sub(r"\s*([.,]+)$", lambda m: "" if m.group(1) in {".", ","} else m.group(0), rendered)
    return rendered.strip()


class _OpenStaxHtmlKeyEquationsParser(html.parser.HTMLParser):
    """Fallback parser for openstax.org chapter key-equations HTML pages."""

    def __init__(self) -> None:
        super().__init__()
        self.in_key_sec = False
        self.sec_depth = 0
        self.in_tr = False
        self.in_td = False
        self.td_depth = 0
        self.in_annotation = False
        self.current_tds: list[str] = []
        self.current_buf: list[str] = []
        self.rows_html: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        cls = attr_map.get("class") or ""
        if not self.in_key_sec and tag == "section" and "key-equations" in cls.split():
            self.in_key_sec = True
            self.sec_depth = 1
            return
        if not self.in_key_sec:
            return
        if tag == "section":
            self.sec_depth += 1
        elif tag == "tr":
            self.in_tr = True
            self.current_tds = []
        elif tag == "td" and self.in_tr:
            self.in_td = True
            self.td_depth = 1
            self.current_buf = []
        elif self.in_td:
            if tag == "td":
                self.td_depth += 1
            elif tag == "annotation-xml":
                self.in_annotation = True
            elif not self.in_annotation:
                attrs_str = "".join(f' {k}="{v}"' for k, v in attrs if v is not None)
                self.current_buf.append(f"<{tag}{attrs_str}>")

    def handle_endtag(self, tag: str) -> None:
        if not self.in_key_sec:
            return
        if tag == "section":
            self.sec_depth -= 1
            if self.sec_depth == 0:
                self.in_key_sec = False
            return
        if self.in_td:
            if tag == "annotation-xml":
                self.in_annotation = False
            elif tag == "td":
                self.td_depth -= 1
                if self.td_depth == 0:
                    self.in_td = False
                    self.current_tds.append("".join(self.current_buf))
            elif not self.in_annotation:
                self.current_buf.append(f"</{tag}>")
        if tag == "tr" and self.in_tr:
            self.in_tr = False
            if len(self.current_tds) >= 2:
                self.rows_html.append((self.current_tds[0], self.current_tds[1]))

    def handle_data(self, data: str) -> None:
        if self.in_td and not self.in_annotation:
            self.current_buf.append(data)


def _resolve_bundle_main_sha() -> str:
    api_url = f"https://api.github.com/repos/{BUNDLE_REPO}/commits/main"
    payload = json.loads(_http_get_bytes(api_url).decode("utf-8"))
    sha = payload.get("sha", "")
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise RuntimeError(f"Could not resolve bundle main SHA from {api_url}: {sha!r}")
    return sha


def _parse_collection_chapters(xml_bytes: bytes, volume: int) -> dict[str, list[str]]:
    """Map expected chapter titles in a volume collection XML to ordered module IDs."""
    root = ET.fromstring(xml_bytes)
    expected_titles = {t for v, _, t in INCLUDED_CHAPTERS if v == volume}
    found: dict[str, list[str]] = {}

    def walk(node: ET.Element) -> None:
        for child in node:
            tag = _local_tag(child)
            if tag == "subcollection":
                title = ""
                mods: list[str] = []
                for sub in child:
                    stag = _local_tag(sub)
                    if stag == "title" and sub.text:
                        title = re.sub(r"\s+", " ", sub.text).strip()
                    elif stag == "content":
                        for m in sub:
                            if _local_tag(m) == "module" and "document" in m.attrib:
                                mods.append(m.attrib["document"])
                if title in expected_titles:
                    found[title] = mods
                for sub in child:
                    if _local_tag(sub) == "content":
                        walk(sub)
            elif tag == "content":
                walk(child)

    walk(root)
    return found


def _extract_rows_from_cnxml(
    cnxml_bytes: bytes,
    volume: int,
    chapter: int,
    chapter_title: str,
    source_url: str,
    retrieved_utc: str,
) -> tuple[list[RawEquationRow], list[dict[str, Any]]]:
    """Extract all equation rows from any section[@class='key-equations'] in a CNXML module."""
    root = ET.fromstring(cnxml_bytes)
    rows_out: list[RawEquationRow] = []
    skipped_headers: list[dict[str, Any]] = []
    for sec in root.iter(f"{{{CNXML_NS}}}section"):
        if sec.attrib.get("class") != "key-equations":
            continue
        last_desc = ""
        for idx, row_el in enumerate(sec.findall(f".//{{{CNXML_NS}}}row"), start=1):
            entries = row_el.findall(f"{{{CNXML_NS}}}entry")
            if len(entries) < 2:
                continue
            desc = _extract_entry_description(entries[0])
            eq_tex = _extract_entry_equation_latex(entries[1])
            if not eq_tex:
                skipped_headers.append({"table_row_idx": idx, "text": desc})
                continue
            if not desc:
                desc = last_desc
            else:
                last_desc = desc
            rows_out.append(
                RawEquationRow(
                    volume=volume,
                    chapter=chapter,
                    chapter_title=chapter_title,
                    row_idx=idx,
                    eq_number="",
                    description=desc,
                    equation_latex=eq_tex,
                    source_url=source_url,
                    retrieved_utc=retrieved_utc,
                )
            )
    return rows_out, skipped_headers


def _openstax_org_fallback_url(volume: int, chapter: int) -> str:
    return f"https://openstax.org/books/university-physics-volume-{volume}/pages/{chapter}-key-equations"


def _fetch_chapter_from_openstax_org(
    volume: int,
    chapter: int,
    chapter_title: str,
    retrieved_utc: str,
) -> tuple[list[RawEquationRow], list[dict[str, Any]], str, str]:
    url = _openstax_org_fallback_url(volume, chapter)
    html_bytes = _http_get_bytes(url)
    html_sha = _sha256_bytes(html_bytes)
    parser = _OpenStaxHtmlKeyEquationsParser()
    parser.feed(html_bytes.decode("utf-8", errors="replace"))
    rows_out: list[RawEquationRow] = []
    skipped_headers: list[dict[str, Any]] = []
    last_desc = ""
    for idx, (td0_html, td1_html) in enumerate(parser.rows_html, start=1):
        td0_xml = ET.fromstring(f"<entry>{td0_html}</entry>")
        td1_xml = ET.fromstring(f"<entry>{td1_html}</entry>")
        desc = re.sub(r"\s+", " ", "".join(td0_xml.itertext())).strip()
        eq_tex = _extract_entry_equation_latex(td1_xml)
        if not eq_tex:
            skipped_headers.append({"table_row_idx": idx, "text": desc})
            continue
        if not desc:
            desc = last_desc
        else:
            last_desc = desc
        rows_out.append(
            RawEquationRow(
                volume=volume,
                chapter=chapter,
                chapter_title=chapter_title,
                row_idx=idx,
                eq_number="",
                description=desc,
                equation_latex=eq_tex,
                source_url=url,
                retrieved_utc=retrieved_utc,
            )
        )
    return rows_out, skipped_headers, url, html_sha


def fetch_live_openstax() -> tuple[dict[str, Any], list[RawEquationRow]]:
    """Fetch all 22 chapters live from OpenStax bundle (with openstax.org fallback)."""
    retrieved_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    bundle_sha = _resolve_bundle_main_sha()

    fetched_urls_sha256: dict[str, str] = {}
    collection_meta: dict[int, tuple[str, str, dict[str, list[str]]]] = {}
    for vol in (1, 2, 3):
        col_url = (
            f"https://raw.githubusercontent.com/{BUNDLE_REPO}/{bundle_sha}/"
            f"collections/university-physics-volume-{vol}.collection.xml"
        )
        col_bytes = _http_get_bytes(col_url)
        col_sha = _sha256_bytes(col_bytes)
        fetched_urls_sha256[col_url] = col_sha
        chapters_map = _parse_collection_chapters(col_bytes, vol)
        collection_meta[vol] = (col_url, col_sha, chapters_map)

    for vol, ch, ch_title in INCLUDED_CHAPTERS:
        if ch_title not in collection_meta[vol][2]:
            raise RuntimeError(f"Chapter missing from collection XML: Vol {vol} Ch {ch} ({ch_title})")

    module_tasks: list[tuple[int, int, str, str, str]] = []
    for vol, ch, ch_title in INCLUDED_CHAPTERS:
        for mod_id in collection_meta[vol][2][ch_title]:
            mod_url = (
                f"https://raw.githubusercontent.com/{BUNDLE_REPO}/{bundle_sha}/"
                f"modules/{mod_id}/index.cnxml"
            )
            module_tasks.append((vol, ch, ch_title, mod_id, mod_url))

    def _download_mod(task: tuple[int, int, str, str, str]) -> tuple[tuple[int, int, str, str, str], bytes | None]:
        try:
            return task, _http_get_bytes(task[4])
        except (urllib.error.URLError, TimeoutError, OSError):
            return task, None

    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        downloaded = list(pool.map(_download_mod, module_tasks))

    by_chapter_mods: dict[tuple[int, int], list[tuple[str, str, bytes | None]]] = {}
    for (vol, ch, _title, mod_id, mod_url), raw_bytes in downloaded:
        if raw_bytes is not None:
            fetched_urls_sha256[mod_url] = _sha256_bytes(raw_bytes)
        by_chapter_mods.setdefault((vol, ch), []).append((mod_id, mod_url, raw_bytes))

    all_rows: list[RawEquationRow] = []
    chapter_manifests: list[dict[str, Any]] = []

    for vol, ch, ch_title in INCLUDED_CHAPTERS:
        col_url, col_sha, chapters_map = collection_meta[vol]
        mod_ids = chapters_map[ch_title]
        mod_records = by_chapter_mods.get((vol, ch), [])
        chapter_rows: list[RawEquationRow] = []
        skipped_headers: list[dict[str, Any]] = []
        key_mod_id = ""
        key_url = ""
        key_sha = ""
        fetch_source = "github_bundle"

        for mod_id, mod_url, mod_bytes in mod_records:
            if mod_bytes is None:
                continue
            extracted, skipped = _extract_rows_from_cnxml(
                mod_bytes, vol, ch, ch_title, mod_url, retrieved_utc
            )
            if extracted or skipped:
                key_mod_id = mod_id
                key_url = mod_url
                key_sha = _sha256_bytes(mod_bytes)
                chapter_rows.extend(extracted)
                skipped_headers.extend(skipped)

        if not key_mod_id:
            # Mandatory fallback check against openstax.org before failing or reporting 0 rows.
            fb_rows, fb_skipped, fb_url, fb_sha = _fetch_chapter_from_openstax_org(
                vol, ch, ch_title, retrieved_utc
            )
            fetched_urls_sha256[fb_url] = fb_sha
            key_url = fb_url
            key_sha = fb_sha
            fetch_source = "openstax_org_fallback"
            chapter_rows = fb_rows
            skipped_headers = fb_skipped

        if not key_url:
            raise RuntimeError(f"Failed live OpenStax retrieval for Vol {vol} Ch {ch} ({ch_title})")

        all_rows.extend(chapter_rows)
        chapter_manifests.append(
            {
                "volume": vol,
                "chapter": ch,
                "chapter_title": ch_title,
                "collection_url": col_url,
                "collection_sha256": col_sha,
                "module_ids": mod_ids,
                "fetch_source": fetch_source,
                "key_equations_module_id": key_mod_id,
                "key_equations_url": key_url,
                "key_equations_sha256": key_sha,
                "raw_row_count": len(chapter_rows),
                "skipped_non_equation_rows": skipped_headers,
            }
        )

    all_rows.sort(key=lambda r: r.sort_key())
    manifest: dict[str, Any] = {
        "attribution": ATTRIBUTION,
        "preregistration_commit_sha": PREREGISTRATION_COMMIT_SHA,
        "bundle_repo": BUNDLE_REPO,
        "bundle_commit_sha": bundle_sha,
        "retrieved_utc": retrieved_utc,
        "eq_number_note": (
            "OpenStax University Physics Key Equations summary tables omit printed (ch.eq) "
            "numbers; eq_number is empty string and row_idx preserves 1-based table row order."
        ),
        "total_chapters": len(chapter_manifests),
        "total_raw_rows": len(all_rows),
        "chapters": chapter_manifests,
        "fetched_urls_sha256": dict(sorted(fetched_urls_sha256.items())),
    }
    return manifest, all_rows


def _normalize_formula_key(eq_latex: str) -> str:
    """Canonicalize formula text for duplicate detection."""
    s = eq_latex.lower()
    s = re.sub(r"\\text\{([^}]*)\}", r"\1", s)
    s = re.sub(r"[\\{}\s.,;]", "", s)
    return s


# Deterministic E3 restatement mapping against benchmarkRows17 (IDs 1..17).
E3_RESTATEMENT_BY_KEY: dict[tuple[int, int, int], tuple[int, str]] = {
    (1, 5, 3): (16, "Restates benchmark Row 16 (Newton's second law, vector form F_net = ma)."),
    (1, 5, 4): (16, "Restates benchmark Row 16 (Newton's second law, scalar form F_net = ma)."),
    (1, 5, 5): (16, "Restates benchmark Row 16 (Newton's second law, component form sum F = ma)."),
    (1, 5, 6): (16, "Restates benchmark Row 16 (Newton's second law, momentum form F_net = dp/dt)."),
    (1, 5, 9): (14, "Restates benchmark Row 14 (Newton's third law, F_AB = -F_BA)."),
    (1, 8, 8): (13, "Restates benchmark Row 13 (closed-system total energy conservation Delta E = 0)."),
    (1, 9, 5): (16, "Restates benchmark Row 16 (Newton's second law in momentum form F = dp/dt)."),
    (1, 9, 10): (16, "Restates benchmark Row 16 (Newton's second law for an extended object F = dp_CM/dt)."),
    (1, 14, 1): (15, "Restates benchmark Row 15 (mass density definition rho = m/V)."),
    (3, 5, 1): (5, "Restates benchmark Row 5 (relativistic time dilation Delta t = gamma Delta tau)."),
    (3, 5, 2): (5, "Restates benchmark Row 5 (Lorentz factor gamma = 1/sqrt(1 - v^2/c^2) per PREREGISTRATION L130)."),
    (3, 5, 3): (6, "Restates benchmark Row 6 (relativistic length contraction L = L_0 / gamma)."),
    (3, 5, 13): (10, "Restates benchmark Row 10 (invariant spacetime interval (Delta s)^2)."),
    (3, 5, 14): (10, "Restates benchmark Row 10 (invariant spacetime proper-time interval (Delta tau)^2)."),
    (3, 5, 19): (8, "Restates benchmark Row 8 (relativistic total energy increase with speed E = gamma m c^2)."),
    (3, 5, 20): (8, "Restates benchmark Row 8 (relativistic kinetic energy increase with speed K = (gamma - 1) m c^2)."),
}


def classify_and_filter_rows(
    raw_rows: list[RawEquationRow],
) -> tuple[list[dict[str, str]], list[EligibleLawRow]]:
    """Apply deterministic E1-E4 exclusions in canonical (volume, chapter, row_idx) order."""
    ordered = sorted(raw_rows, key=lambda r: r.sort_key())
    exclusions: list[dict[str, str]] = []
    retained: list[RawEquationRow] = []

    seen_formula_by_law: dict[str, tuple[int, int, int, str]] = {}

    for row in ordered:
        key = row.sort_key()
        desc_l = row.description.lower()
        eq_l = row.equation_latex.lower()

        # E1_PURE_MATH: pure mathematical/geometric/vector-algebra identities without physical quantities.
        e1_reason = ""
        if (row.volume, row.chapter) == (1, 1) and "percent uncertainty" in desc_l:
            e1_reason = "Pure algebraic percentage/relative-uncertainty formula with no physical quantity."
        elif (row.volume, row.chapter) == (1, 2):
            e1_reason = (
                "Chapter 2 Vectors identity: pure vector algebra, components, polar coordinates, "
                "or dot/cross product formula with no physical law relationship."
            )
        elif (row.volume, row.chapter) == (1, 13) and "conic sections" in desc_l:
            e1_reason = "Pure polar geometric equation of conic sections (alpha/r = 1 + e cos theta) without physical quantities."

        if e1_reason:
            exclusions.append(
                {
                    "volume": str(row.volume),
                    "chapter": str(row.chapter),
                    "row_idx": str(row.row_idx),
                    "eq_number": row.eq_number,
                    "description": row.description,
                    "equation_latex": row.equation_latex,
                    "exclusion_code": "E1_PURE_MATH",
                    "matched_benchmark_id": "",
                    "rationale": e1_reason,
                    "preregistration_commit_sha": PREREGISTRATION_COMMIT_SHA,
                }
            )
            continue

        # E2_UNIT_OR_CONSTANT: bare unit conversions or bare numerical physical constants.
        has_rel_var = bool(re.search(r"[a-zA-Z\\]", row.equation_latex))
        is_unit_conversion = (
            ("unit conversion" in desc_l or "conversion factor" in desc_l)
            and not any(tok in desc_l for tok in ("velocity", "force", "energy", "pressure", "heat", "wave", "sound"))
        )
        is_bare_constant = (
            re.fullmatch(r"[A-Za-z_\\{}]+\s*=\s*[-+]?\d+(?:\.\d+)?(?:\s*\\times\s*10\^\{[-+]?\d+\})?(?:\s*\\text\{[^}]+\})?", row.equation_latex.strip())
            is not None
            and not has_rel_var
        )
        if is_unit_conversion or is_bare_constant:
            exclusions.append(
                {
                    "volume": str(row.volume),
                    "chapter": str(row.chapter),
                    "row_idx": str(row.row_idx),
                    "eq_number": row.eq_number,
                    "description": row.description,
                    "equation_latex": row.equation_latex,
                    "exclusion_code": "E2_UNIT_OR_CONSTANT",
                    "matched_benchmark_id": "",
                    "rationale": "Pure unit-conversion ratio or bare physical constant without functional relationship.",
                    "preregistration_commit_sha": PREREGISTRATION_COMMIT_SHA,
                }
            )
            continue

        # E3_RESTATES_BENCHMARK_17: direct restatements of benchmarkRows17 Rows 1..17.
        if key in E3_RESTATEMENT_BY_KEY:
            bm_id, reason = E3_RESTATEMENT_BY_KEY[key]
            exclusions.append(
                {
                    "volume": str(row.volume),
                    "chapter": str(row.chapter),
                    "row_idx": str(row.row_idx),
                    "eq_number": row.eq_number,
                    "description": row.description,
                    "equation_latex": row.equation_latex,
                    "exclusion_code": "E3_RESTATES_BENCHMARK_17",
                    "matched_benchmark_id": str(bm_id),
                    "rationale": reason,
                    "preregistration_commit_sha": PREREGISTRATION_COMMIT_SHA,
                }
            )
            continue

        # E4_EXACT_DUPLICATE: exact repeat of an earlier retained entry in canonical order.
        norm_eq = _normalize_formula_key(row.equation_latex)
        e4_reason = ""
        # Canonicalize synonymous subscripts/descriptions for identical physical laws.
        if key == (1, 10, 23) and "work-energy theorem" in desc_l:
            norm_eq = _normalize_formula_key(r"W_{net} = K_B - K_A")
        dup_key = f"{norm_eq}"
        if dup_key in seen_formula_by_law:
            prev_v, prev_c, prev_idx, prev_desc = seen_formula_by_law[dup_key]
            # Same normalized formula is an exact duplicate only if it expresses the same physical law.
            same_law_pairs = {
                ("Total acceleration", "Total acceleration"),
                ("Work-energy theorem", "Work-energy theorem"),
                ("Speed of a compression wave in a fluid", "Speed of sound in a fluid"),
            }
            if prev_desc == row.description or (prev_desc, row.description) in same_law_pairs:
                e4_reason = (
                    f"Exact repeat of earlier retained law V{prev_v} Ch.{prev_c} row {prev_idx} "
                    f"({prev_desc!r})."
                )

        if e4_reason:
            exclusions.append(
                {
                    "volume": str(row.volume),
                    "chapter": str(row.chapter),
                    "row_idx": str(row.row_idx),
                    "eq_number": row.eq_number,
                    "description": row.description,
                    "equation_latex": row.equation_latex,
                    "exclusion_code": "E4_EXACT_DUPLICATE",
                    "matched_benchmark_id": "",
                    "rationale": e4_reason,
                    "preregistration_commit_sha": PREREGISTRATION_COMMIT_SHA,
                }
            )
            continue

        seen_formula_by_law.setdefault(dup_key, (row.volume, row.chapter, row.row_idx, row.description))
        retained.append(row)

    eligible: list[EligibleLawRow] = []
    for idx, row in enumerate(retained, start=1):
        eligible.append(
            EligibleLawRow(
                law_id=f"H{idx:03d}",
                volume=row.volume,
                chapter=row.chapter,
                chapter_title=row.chapter_title,
                row_idx=row.row_idx,
                eq_number=row.eq_number,
                description=row.description,
                equation_latex=row.equation_latex,
                source_url=row.source_url,
                preregistration_commit_sha=PREREGISTRATION_COMMIT_SHA,
            )
        )
    return exclusions, eligible


def sample_and_pool(
    eligible: list[EligibleLawRow],
) -> tuple[list[EligibleLawRow], list[EligibleLawRow], list[dict[str, str]]]:
    """Execute exact seed=20261113 stratified sampling, reserve permutation, and pooling."""
    rng = random.Random(SAMPLING_SEED)
    buckets: dict[tuple[int, int], list[EligibleLawRow]] = {}
    for row in sorted(eligible, key=lambda r: r.sort_key()):
        buckets.setdefault((row.volume, row.chapter), []).append(row)

    avail = sorted(buckets.keys())
    for ch_key in avail:
        rng.shuffle(buckets[ch_key])

    primary_drawn: list[EligibleLawRow] = []
    while len(primary_drawn) < PRIMARY_TARGET_COUNT and avail:
        remainder = PRIMARY_TARGET_COUNT - len(primary_drawn)
        if remainder >= len(avail):
            for ch_key in list(avail):
                primary_drawn.append(buckets[ch_key].pop(0))
            avail = [ch_key for ch_key in avail if buckets[ch_key]]
        else:
            chosen = rng.sample(avail, remainder)
            for ch_key in chosen:
                primary_drawn.append(buckets[ch_key].pop(0))
            avail = [ch_key for ch_key in avail if buckets[ch_key]]

    if len(primary_drawn) != PRIMARY_TARGET_COUNT:
        raise RuntimeError(f"Expected {PRIMARY_TARGET_COUNT} primary laws, drew {len(primary_drawn)}")

    primary_sorted = sorted(primary_drawn, key=lambda r: r.sort_key())

    reserve_pool: list[EligibleLawRow] = []
    for ch_key in sorted(buckets.keys()):
        reserve_pool.extend(buckets[ch_key])
    reserve_pool.sort(key=lambda r: r.sort_key())
    rng.shuffle(reserve_pool)

    # Pool 48 primary held-out laws (canonical order) + 17 calibration rows (benchmark_id 1..17).
    pooled_items: list[dict[str, str]] = []
    for row in primary_sorted:
        pooled_items.append(
            {
                "source_set": "heldout",
                "law_id": row.law_id,
                "benchmark_id": "",
                "volume": str(row.volume),
                "chapter": str(row.chapter),
                "row_idx": str(row.row_idx),
                "eq_number": row.eq_number,
                "draw_phase": "primary_48",
                "reserve_rank": "",
                "description": row.description,
                "equation_latex": row.equation_latex,
            }
        )
    for bm_id, bm_desc, bm_formula in CALIBRATION_17_NEUTRAL:
        pooled_items.append(
            {
                "source_set": "benchmark_17",
                "law_id": "",
                "benchmark_id": str(bm_id),
                "volume": "",
                "chapter": "",
                "row_idx": "",
                "eq_number": "",
                "draw_phase": "calibration_17",
                "reserve_rank": "",
                "description": bm_desc,
                "equation_latex": bm_formula,
            }
        )

    pool_rng = random.Random(SAMPLING_SEED)
    pool_rng.shuffle(pooled_items)
    for idx, item in enumerate(pooled_items, start=1):
        item["card_id"] = f"C{idx:03d}"
        item["preregistration_commit_sha"] = PREREGISTRATION_COMMIT_SHA

    return primary_sorted, reserve_pool, pooled_items


def _render_csv_bytes(fieldnames: list[str], rows: list[dict[str, Any]]) -> bytes:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for r in rows:
        writer.writerow({k: r.get(k, "") for k in fieldnames})
    return buf.getvalue().encode("utf-8")


def _render_stage0_prompt_bytes(pooled_items: list[dict[str, str]]) -> bytes:
    """Build the neutral Stage 0 plain-physics card-writer prompt for C001..C065."""
    lines: list[str] = [
        "# Stage 0 Plain-Physics Law Card Generation Packet",
        "",
        f"- **preregistration_commit_sha:** `{PREREGISTRATION_COMMIT_SHA}`",
        f"- **Card count:** `{len(pooled_items)}` (`C001`..`C{len(pooled_items):03d}`)",
        "",
        "## Instructions for One Fresh External Session",
        "",
        "You are assisting with a physics curriculum summarization task in a clean standalone session.",
        "Write one plain-language physics summary card for each of the `65` physics laws/relations listed below (`C001` through `C065`).",
        "",
        "### Strict Output Schema",
        "Return **ONLY** one valid JSON array of `65` objects in exact order `C001`..`C065`, using these exact four keys per object:",
        "",
        "```json",
        "[",
        "  {",
        '    "card_id": "C001",',
        '    "what_it_says": "...",',
        '    "quantities_related": "...",',
        '    "conditions_to_hold": "..."',
        "  }",
        "]",
        "```",
        "",
        "### Field Requirements",
        "For every entry:",
        "1. `what_it_says`: A concise, accurate, plain-language statement of the physical law or principle, plus its mathematical formula where a formula is given.",
        "2. `quantities_related`: List all physical quantities and variables related by the law (e.g., mass, velocity, force, displacement, pressure, volume, temperature, time, energy, frequency, wavelength).",
        "3. `conditions_to_hold`: State all physical conditions, domain assumptions, or structural requirements needed for the law to hold (for example: mass or rotational inertia, spatial distance or separation between bodies/events, physical contact/surfaces/walls or medium, gravitational field or spacetime curvature, relative speed/inertial or accelerating reference frame, or definitional equivalence/conservation/frame invariance).",
        "",
        "### Style & Neutrality Constraints",
        "- Use strictly standard textbook physics terminology.",
        "- Do **not** group entries, sort entries, infer source origin, speculate about book/chapter provenance, or use philosophical or non-standard terminology.",
        "- Every string value must be non-empty.",
        "",
        "---",
        "",
        "## Physics Laws to Summarize (`C001`..`C065`)",
        "",
    ]

    for item in pooled_items:
        lines.append(f"### {item['card_id']}")
        lines.append(f"- **description:** {item['description']}")
        lines.append(f"- **formula:** `{item['equation_latex']}`")
        lines.append("")

    return ("\n".join(lines).rstrip() + "\n").encode("utf-8")


def _build_derived_artifacts(
    raw_rows: list[RawEquationRow],
) -> tuple[dict[str, bytes], dict[str, Any]]:
    """Compute all derived CSVs and Stage 0 prompt in memory deterministically."""
    exclusions, eligible = classify_and_filter_rows(raw_rows)
    primary_sorted, reserve_pool, pooled_items = sample_and_pool(eligible)

    exclusion_fields = [
        "volume",
        "chapter",
        "row_idx",
        "eq_number",
        "description",
        "equation_latex",
        "exclusion_code",
        "matched_benchmark_id",
        "rationale",
        "preregistration_commit_sha",
    ]
    eligible_fields = [
        "law_id",
        "volume",
        "chapter",
        "chapter_title",
        "row_idx",
        "eq_number",
        "description",
        "equation_latex",
        "source_url",
        "preregistration_commit_sha",
    ]
    reserve_fields = ["reserve_rank"] + eligible_fields
    sample_fields = [
        "card_id",
        "source_set",
        "law_id",
        "benchmark_id",
        "volume",
        "chapter",
        "row_idx",
        "eq_number",
        "draw_phase",
        "reserve_rank",
        "preregistration_commit_sha",
    ]

    eligible_dicts = [
        {
            "law_id": r.law_id,
            "volume": str(r.volume),
            "chapter": str(r.chapter),
            "chapter_title": r.chapter_title,
            "row_idx": str(r.row_idx),
            "eq_number": r.eq_number,
            "description": r.description,
            "equation_latex": r.equation_latex,
            "source_url": r.source_url,
            "preregistration_commit_sha": r.preregistration_commit_sha,
        }
        for r in eligible
    ]
    reserve_dicts = [
        {
            "reserve_rank": str(rank),
            "law_id": r.law_id,
            "volume": str(r.volume),
            "chapter": str(r.chapter),
            "chapter_title": r.chapter_title,
            "row_idx": str(r.row_idx),
            "eq_number": r.eq_number,
            "description": r.description,
            "equation_latex": r.equation_latex,
            "source_url": r.source_url,
            "preregistration_commit_sha": r.preregistration_commit_sha,
        }
        for rank, r in enumerate(reserve_pool, start=1)
    ]

    artifacts: dict[str, bytes] = {
        str(EXCLUSION_CSV_PATH): _render_csv_bytes(exclusion_fields, exclusions),
        str(ELIGIBLE_CSV_PATH): _render_csv_bytes(eligible_fields, eligible_dicts),
        str(RESERVE_CSV_PATH): _render_csv_bytes(reserve_fields, reserve_dicts),
        str(SAMPLE_MANIFEST_PATH): _render_csv_bytes(sample_fields, pooled_items),
        str(STAGE0_PROMPT_PATH): _render_stage0_prompt_bytes(pooled_items),
    }

    counts_by_code: dict[str, int] = {
        "E1_PURE_MATH": 0,
        "E2_UNIT_OR_CONSTANT": 0,
        "E3_RESTATES_BENCHMARK_17": 0,
        "E4_EXACT_DUPLICATE": 0,
    }
    for ex in exclusions:
        counts_by_code[ex["exclusion_code"]] += 1

    stats = {
        "total_raw": len(raw_rows),
        "exclusion_counts": counts_by_code,
        "total_excluded": len(exclusions),
        "total_eligible": len(eligible),
        "primary_count": len(primary_sorted),
        "reserve_count": len(reserve_pool),
        "pooled_count": len(pooled_items),
    }
    return artifacts, stats


def _load_raw_csv(path: Path) -> list[RawEquationRow]:
    expected = [
        "volume",
        "chapter",
        "chapter_title",
        "row_idx",
        "eq_number",
        "description",
        "equation_latex",
        "source_url",
        "retrieved_utc",
    ]
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != expected:
            raise RuntimeError(f"Unexpected raw CSV header: {reader.fieldnames} != {expected}")
        rows: list[RawEquationRow] = []
        for rec in reader:
            rows.append(
                RawEquationRow(
                    volume=int(rec["volume"]),
                    chapter=int(rec["chapter"]),
                    chapter_title=rec["chapter_title"],
                    row_idx=int(rec["row_idx"]),
                    eq_number=rec["eq_number"],
                    description=rec["description"],
                    equation_latex=rec["equation_latex"],
                    source_url=rec["source_url"],
                    retrieved_utc=rec["retrieved_utc"],
                )
            )
    return rows


def _check_leak_hygiene(prompt_text: str, script_text: str) -> None:
    """Assert zero restricted or path/project-leak vocabulary in prompt and script."""
    # Encoded as hex so the checker itself embeds zero restricted tokens literally.
    ci_tokens_hex = [
        "76696272616e6365",
        "617070726563696174696f6e",
        "706f696e74206f66207265666c656374696f6e",
        "706f696e74206f662061747472616374696f6e",
        "736f7665726569676e",
        "6e6f6e706879736963616c",
        "7265636570746976697479",
        "726563657074697665",
        "6b656570",
        "696e76657274",
        "747372",
        "74686520736f7665726569676e206d6972726f72",
        "776861742074686520776f726473206b6e6577",
        "657870616e73696f6e2064696c6174696f6e",
        "657465726e616c2d656e657267657469632d656e74697479",
        "636f6e7363696f75732d706879736963616c",
        "636f6e7363696f757320656e65726779",
        "63757272656e74206f6620636f6e7363696f75736e657373",
    ]
    cs_tokens_hex = [
        "4d6f76656d656e74",
        "43757272656e74",
        "566f72746578",
        "436f6e76657267656e6365",
    ]
    forbidden_paths_hex = [
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
    ]
    prompt_leaks_hex = [
        "4f70656e53746178",
        "6f70656e73746178",
        "62656e63686d61726b",
        "68656c646f7574",
        "68656c642d6f7574",
        "566f6c756d6520",
        "4368617074657220",
    ]

    def _decode(hex_list: list[str]) -> list[str]:
        return [bytes.fromhex(h).decode("utf-8") for h in hex_list]

    for label, text in (("stage0_prompt", prompt_text), ("script", script_text)):
        for tok in _decode(ci_tokens_hex):
            if re.search(r"\b" + re.escape(tok) + r"\b", text, flags=re.IGNORECASE):
                raise RuntimeError(f"Restricted case-insensitive word {tok!r} found in {label}")
        for tok in _decode(cs_tokens_hex):
            if re.search(r"\b" + re.escape(tok) + r"\b", text):
                raise RuntimeError(f"Restricted capitalized word {tok!r} found in {label}")
        for tok in _decode(forbidden_paths_hex):
            if tok.lower() in text.lower():
                raise RuntimeError(f"Forbidden substring {tok!r} found in {label}")

    for tok in _decode(prompt_leaks_hex):
        if tok in prompt_text:
            raise RuntimeError(f"Origin-leaking token {tok!r} found in stage0_prompt")


def run_verify_offline() -> dict[str, Any]:
    """Re-run extraction validation, exclusions, sampling, pooling, and prompt byte checks offline."""
    if not MANIFEST_PATH.exists() or not RAW_CSV_PATH.exists():
        raise RuntimeError("Missing manifest or raw CSV for --verify-offline")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("attribution") != ATTRIBUTION:
        raise RuntimeError("Manifest attribution string mismatch")
    if manifest.get("preregistration_commit_sha") != PREREGISTRATION_COMMIT_SHA:
        raise RuntimeError("Manifest preregistration_commit_sha mismatch")
    if len(manifest.get("chapters", [])) != 22:
        raise RuntimeError(f"Expected 22 chapters in manifest, got {len(manifest.get('chapters', []))}")

    raw_rows = _load_raw_csv(RAW_CSV_PATH)
    if len(raw_rows) != manifest.get("total_raw_rows"):
        raise RuntimeError("Manifest total_raw_rows does not match raw CSV row count")

    # Verify canonical ordering and per-chapter counts against manifest.
    keys = [r.sort_key() for r in raw_rows]
    if keys != sorted(keys):
        raise RuntimeError("Raw CSV rows are not sorted canonically by (volume, chapter, row_idx)")

    by_ch_counts: dict[tuple[int, int], int] = {}
    for r in raw_rows:
        by_ch_counts[(r.volume, r.chapter)] = by_ch_counts.get((r.volume, r.chapter), 0) + 1
    for ch_rec in manifest["chapters"]:
        ch_key = (int(ch_rec["volume"]), int(ch_rec["chapter"]))
        if by_ch_counts.get(ch_key, 0) != int(ch_rec["raw_row_count"]):
            raise RuntimeError(f"Row count mismatch for {ch_key}")

    artifacts, stats = _build_derived_artifacts(raw_rows)
    for out_path_str, expected_bytes in artifacts.items():
        out_path = Path(out_path_str)
        if not out_path.exists():
            raise RuntimeError(f"Expected output file missing on disk: {out_path}")
        actual_bytes = out_path.read_bytes()
        if actual_bytes != expected_bytes:
            raise RuntimeError(f"Byte-for-byte reproducibility mismatch on {out_path.name}")

    _check_leak_hygiene(
        artifacts[str(STAGE0_PROMPT_PATH)].decode("utf-8"),
        Path(__file__).read_text(encoding="utf-8"),
    )
    return stats


def run_live() -> dict[str, Any]:
    """Fetch OpenStax corpus live, emit all Part 2 prep files, and verify offline parity."""
    manifest, raw_rows = fetch_live_openstax()
    PACKETS_DIR.mkdir(parents=True, exist_ok=True)

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    raw_fields = [
        "volume",
        "chapter",
        "chapter_title",
        "row_idx",
        "eq_number",
        "description",
        "equation_latex",
        "source_url",
        "retrieved_utc",
    ]
    raw_dicts = [
        {
            "volume": str(r.volume),
            "chapter": str(r.chapter),
            "chapter_title": r.chapter_title,
            "row_idx": str(r.row_idx),
            "eq_number": r.eq_number,
            "description": r.description,
            "equation_latex": r.equation_latex,
            "source_url": r.source_url,
            "retrieved_utc": r.retrieved_utc,
        }
        for r in raw_rows
    ]
    RAW_CSV_PATH.write_bytes(_render_csv_bytes(raw_fields, raw_dicts))

    artifacts, stats = _build_derived_artifacts(raw_rows)
    for out_path_str, content_bytes in artifacts.items():
        Path(out_path_str).write_bytes(content_bytes)

    _check_leak_hygiene(
        artifacts[str(STAGE0_PROMPT_PATH)].decode("utf-8"),
        Path(__file__).read_text(encoding="utf-8"),
    )
    stats = run_verify_offline()
    stats["bundle_commit_sha"] = manifest["bundle_commit_sha"]
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch, filter, and sample OpenStax key equations.")
    parser.add_argument(
        "--verify-offline",
        action="store_true",
        help="Re-run exclusions, sampling, pooling, and Stage 0 prompt checks from saved local files.",
    )
    args = parser.parse_args()
    stats = run_verify_offline() if args.verify_offline else run_live()
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
