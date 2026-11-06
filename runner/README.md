# TSR Rule Runner

A procedure, not a reader. It runs the one rule of *The Sovereign Mirror* through physics the book has not reflected, with the judgment calls written down first, and checks whether any two rows the rule forces contradict each other.

It can produce two results and is built to be equally able to produce either: a break report (two forced rows that collide, with both derivation chains), or a report that nothing collided across the corpus, with the decoy margin showing the rows were run and not curated.

Spec: the "TSR Rule Runner: software specification" (November 2026). Builds on `../tests/tsr_formal.py`, the extension-test and round-2 protocols, `../deep-read.md` and tsr.wtf/holds.

## Layout

```
corpus/          one YAML record per physics relation (112: 24 calibration + 88 unreflected)
vocab/           frozen.yaml (the word map, typed by Map row), resistance_lexicon.yaml (criterion R1)
rule/            criteria.yaml: the closed joints, the open joints, the pending rulings
tsr_runner/      schema, vocab, rule (feature extractor + decision), formal (Layer A), providers,
                 generate (roles + agreement gate), collide (Layers A/B/C + break report), decoy, ledger, cli
prompts/         generator, opponent, judge, rater, canary
tests/           Phase 0/1 acceptance + mock pipeline
results/         one directory per run (gitignored): calls.jsonl, rows, collisions, breaks, decoys, report
ledger/          <domain>.md in the holds format (written by real runs only)
patches/         tsr_formal_rows.py (new ROWS entries, written by real runs only)
```

## Run

```
pip install pyyaml pytest
python -m pytest -q tests                      # Phase 0/1 acceptance
python -m tsr_runner.cli validate               # schema + review status
python -m tsr_runner.cli calibrate              # rulings reproduced from records alone
python -m tsr_runner.cli preview                # what the procedure alone decides, every record
python -m tsr_runner.cli run --domain mechanics --models models.yaml --hidden-calibration mech.damping
python -m tsr_runner.cli run --domain thermodynamics --models models.yaml --book /path/to/book.txt
python -m tsr_runner.cli collide --runs results/<id1> results/<id2> ... --models models.yaml --book /path/to/book.txt
python -m tsr_runner.cli ledger --run results/<id>
```

`--mock` runs the whole pipeline with no model (plumbing only; every artifact is stamped MOCK). Copy `models.example.yaml` to `models.yaml` and set the API-key environment variables for a real run. The roster must have at least five generators from at least three vendors, one of them open-weights; the opponent must come from a vendor other than the generators' majority.

## How a row is decided

Every decision is traceable to a record field, a lexicon entry and a criterion id. Nothing in `rule.py` reads a book ruling.

1. If any quantity the cost rises (or falls) with is `undetermined` in the lexicon: **JUDGMENT**, not forced (C3).
2. If the record's form is a definition, identity, conservation law or symmetry: **keeps** (C1).
3. Otherwise count the cost claims that are resistance-caused (rise with a quantity that carries resistance under R1) or made by a separation; odd: **turns around**, else **keeps** (C0).
4. If the record names an open joint (`depends_on`), or any alternate standard form decides differently (C6): not forced.
5. The formula is never rewritten (October 2026 ruling): a turned row's reflected formula is the word-map image of the physical formula, and only its reading turns. A2 catches rewrites.

A relation that is both a definition and a cost claim (kinetic energy, Ohm, latent heat, heat capacity) is two records, linked by `derived_from`; both hold, at different levels.

## What a forced row is

A row goes to collision testing only if: the procedure decided it without a JUDGMENT flag and without an open joint; at least four of five generators agree on the shape; the words used are in the frozen vocabulary (no NEW words; units don't cross); the opponent could not produce a rule-compliant reading the other way; and the domain's decoy margin passed. Everything else is logged under Open with its disagreement pattern.

## Collisions

- A1 mirror-twice: the word map stays one-to-one when typed by Map row after new rows.
- A2 composition: `w(q) = op(w(inputs))` for every reflected formula.
- A3 sign graph: monotone claims as signed edges; opposite-sign edges or an unbalanced cycle.
- A4 parity along derivation chains, at the formula level. At the reading level the check is reported as informational only: the book's own row 8 is built from kept rows and turns, so reading parity is not compositional by the book's precedent.
- B: two blind judges on every pair of forced rows, and every forced row against the book's rulings: "taking both as true in TSR's meanings, is there a situation they describe differently?"
- C: every candidate collision against the book's text (a local plain-text copy of the paperback; not in the repo). If the book states the resolution: documentation gap, not a break.

A break is a surviving collision whose upstream judgment-call list is empty. The report names the minimal change to the rule that would dissolve it.

## State of the joints (criteria v1, lexicon R1)

Closed, and reproducing every published ruling (22/22):

- C1 identity vs cost: classified by what the statement asserts, not by what the formula contains; both-level relations are two records.
- C3 which quantities carry resistance: R1, stated once. Charge no, temperature no, entropy no; mass, friction, viscosity, damping, stiffness, electrical and thermal resistance, impedance, inductance yes; moment of inertia and density yes by geometry.
- C4 frozen vocabulary; C5 units don't cross; C6 every standard form is run.

Open (rows on them cannot be forced; see `rule/criteria.yaml`):

- `gravity_call` (the book's): what curves counts as energy or as resistance. Affects rows 11, 12, Newtonian gravitation, gravitational time dilation.
- `form_call`: F = ma, torque, centripetal force as definition or law.
- `separation_call`: whether a dependence on separation with no named difficulty (inverse-square laws, an aperture, a coupling that grows with distance) is "a separation made by distance".
- `reverse_cost`: a difficulty that falls with a resistance-carrying quantity (terminal velocity, Reynolds number, bound-state spacing, Yukawa range). The rule speaks only of costs that rise.
- R1 undetermined: heat capacity, refractive index (and index contrast), potential barrier height, Higgs coupling, QCD string tension.

Pending author rulings (the spec cites them; they are not published): escape velocity, centripetal force. Enter them in the records' `ruling.shape`.

## What the procedure alone says about the 88 new relations

Before any model is consulted (`preview`): 73 forced by the procedure, 9 JUDGMENT, 6 open. Of the 73, the ones that turn around are: Hooke's law, gravitational potential energy (cost reading), resonance width, latent heat (cost reading), Fourier conduction, Joule heating, Lenz / self-inductance, Ohm (cost reading), standing waves, decoherence. Everything else keeps, including the second law, the third law, the Carnot limit, both uncertainty relations and Landauer's principle, because under R1 none of them contains a resistance-carrying quantity. That is the honest output of the closed rule; whether the author wants temperature or entropy to carry resistance is a change to R1, made once, that reruns everything.

## Second-pass physics review

Every record outside `corpus/calibration` is marked `review: pending`. Physics errors in the corpus are the most likely false source of collisions; a reviewer sets `review: reviewed:<name>` after checking the statement, formula, form and cost block against the cited source.
