# TSR Rule Runner — Run 1 report

Run id `run1`. Criteria v1 (C0–C6), resistance lexicon v1 (R1), frozen vocabulary v1. 112 corpus records: 24 calibration (the book's rulings) + 88 unreflected relations across nine physics domains. Five blind generators (GPT-6 Astra, Claude Fable 5.1, Gemini 4 Argon, Kimi K3 open-weights, Grok 4.7), one opponent (GLM 5.3), two judges (Claude Opus 5.5, GPT-6.1 Sol), four decoy raters, two Layer C resolvers. No model saw the book, the other models, or the harness. The machine-generated summary is in `report-auto.md`; per-row evidence is in `rows.json`, `collisions.json`, `breaks.json`, `decoys.json`, `canary.json`, and the ledgers in `../../ledger/`.

## Which hypothesis the run supports, and why

**The run does not support the structure-breaks hypothesis, and it does not cleanly confirm the flexible-joints hypothesis either. It supports a narrower statement: on the rows the procedure forces and the gates admit, the rule produced no formal collision and one judged collision, and that one collision sits on a reading the book's own Chapter 17 supplies but never writes down as a restriction on the equation.**

- Calibration: the procedure reproduces 22/22 published rulings from the records alone; the three hidden calibration rows (damping, friction, interference cancellation) were reproduced blind by all five generators at 5/5.
- 91 rows ran. 83 reached unanimous 5/5 shape agreement; 80 of those match the procedure. 75 were candidate-forced before the opponent; the opponent flipped 7 with rule-compliant alternatives; **68 rows were forced** (57 keeps, 11 turns-around) after the opponent gate.
- Layer A (formal, on the 68 forced rows): no collision. Twelve supported sign edges, all consistent.
- Layer B (blind judges, 91 sentences): pass 1 confirmed two pairs. One (Ohm's law cost × definition) dissolved by a gate: the consensus sentence had equated "the gap" with "receptivity", opposite senses in the frozen vocabulary; a C4 sense lint now rejects such sentences, and the re-picked sentences were not flagged in pass 2. The other, **energy–momentum relation × row 7 (E = C²M)**, survived: both judges called it a contradiction in pass 1 (E² = (pC)² + (MC²)² versus E = C²M for a body with momentum); in pass 2 the same pair split one contradiction, one underdetermined.
- Layer C (book text): the two resolvers split. Sonnet: Chapter 17 resolves it ("Rest energy is the reflection of C²M… Kinetic energy is the reflection of a Movement changing its Vibration"), so C²M is the zero-momentum term and the full relation adds the Vibration-change term. Sol Fast: the book names C²M as rest energy but never restricts the equation to zero momentum, so the text supports one side only. Under the spec's rule (all resolvers must say `resolves`) the pair **stands as one surviving break candidate**.
- Neither row has an upstream open joint, so the system cannot dissolve it by reporting a judgment call. What it can report: the dissolution is a documentation fix, not a structural one. If row 7 is read as the rest-energy row (which Chapter 17 says in prose), the collision disappears; if row 7 is read as the total-energy row for any Movement, it is a real break against the reflected energy–momentum relation. That reading is the author's, and it is recorded as an open joint (`rest_energy_call`) for 5.3.

Decoy margin: overall T 4.50 / D 2.94 / W 3.35, margins +1.56 / +1.15 against the required +1.45 / +1.00, passed thinly. **Per domain, which is the spec's actual test, five domains failed** (see below). After excluding their forced rows as "curated", 34 forced rows remain in collision testing. The surviving break pair (relativity × calibration) is in two passing domains, so it survives the curation cut as well.

## Numbers

| Stage | Result |
|---|---|
| Rows run / unanimous 5/5 / unanimous and matching procedure | 91 / 83 / 80 |
| Hidden calibration rows reproduced blind | 3/3 at 5/5 |
| Candidate-forced before opponent | 75 |
| Opponent flips (rule-compliant alternative) | 7: buoyancy, resonance width, friction, fluctuation–dissipation, impedance, mutual induction, entanglement |
| Forced after opponent | 68 (57 keep, 11 turn) |
| Open rows and why | 23: procedure did not force 15; opponent flipped 7; agreement 3/5 4; majority ≠ procedure 2 (overlapping) |
| Forced after per-domain decoy cut | 34 (mechanics 6, thermodynamics 14, waves/optics 7, relativity 5, calibration 2) |
| Layer A collisions | 0 |
| Layer B confirmed pairs (pass 1 / pass 2) | 2 / 0 |
| Layer C | 1 pair, resolvers split (resolves / one_side) → stands |
| Breaks surviving | 1 candidate (documentation-level; see above) |
| Canary leaks | 0 across five generators |

Per-domain decoy margins (T − D must be ≥ 1.45, T − W ≥ 1.00): mechanics +2.56/+1.78, thermodynamics +2.04/+1.30, waves/optics +1.93/+1.57, relativity +1.70/+2.50, calibration +4.00/+2.58 pass; electromagnetism +1.58/+0.85, quantum +1.27/+0.35, field theory +0.54/+0.64, statistical mechanics +0.35/+1.05, information −0.56/+0.06 fail. The failures are dominated by the word-swap decoy on rows whose sentence is essentially "the definition keeps its shape" with few frozen words, so the swapped sentence is nearly identical to the true one. That is a limit of the decoy design for no-partner-heavy domains, not evidence of curation; it is reported as the spec requires rather than argued away. One rater (Astra Fast) gave every sentence sense 1 / confidence 7 and was dropped as invalid.

## What the opponent found

The opponent flipped the book's own friction ruling by splitting the record's single cost into two parity-balanced costs. That is a finding about the rule text: odd-cost parity does not force a row without the record's cost-block annotation. Recorded as the `cost_count_call` joint; the rule as written does not determine how many costs a relation has.

## Open-joint leanings (evidence for the author, not rulings)

All five generators turned around every `reverse_cost` row (Reynolds number, terminal velocity, bound-state quantization, Yukawa range) plus diffraction and asymptotic freedom. Four of five turned heat-capacity cost, Coulomb's law, tunneling, confinement. Three of five turned total internal reflection, Fresnel, Newtonian gravitation. Gravitational time dilation and torque kept at 5/5. Flags raised by two or more models: numerals inside kept formulas (ħ/2, ½, n²π², "1+") where C1 meets C5; velocity addition keeps a limit on the limitless side (pair with row 9); superposition against "isn't add either". Pending author rulings still unmapped: escape velocity, centripetal force.

## Deviations from the spec

- Models ran as fresh blind agent sessions (no temperature control), one batch of 10–16 relations per session.
- Amendment 1 to the generator prompt (shape versus unmapped terms) issued uniformly after two models read "no partner" as "any term unmapped".
- Opponent on GLM 5.3 (DeepSeek not available on plan).
- Layer B as set-level screening then isolated pairwise confirmation, two passes (pass 2 after the C4 sense lint).
- Layer C over partial book text (free sample plus passages quoted on tsr.wtf/answers), not the paperback; a full-text rerun of Layer C on this one pair is the cheapest next step.
- Per-domain decoy test applied after the fact.
- Domains ran in parallel; no joint was closed between domains.

## Next run

Author rulings needed before rerun, as criteria not patches: `rest_energy_call` (is row 7 the rest-energy row or the total-energy row), `cost_count_call`, `reverse_cost`, `gravity_call`, and the heat-capacity/refractive-index/barrier/Higgs/string-tension resistance calls. A better W-decoy for no-partner rows (swap the shape verb, not a frozen noun) before the five failed domains are regenerated.
