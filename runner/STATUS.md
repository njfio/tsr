# Status against the spec's phases

6 November 2026. Criteria v1, lexicon R1 v1. **Run 1 complete: see `results/run1/report.md`.**

| Phase | Acceptance in the spec | State |
| --- | --- | --- |
| 0 Harness | Port `tsr_formal.py`; record schema; extractor + procedure; reproduce 17/17 and the October rulings from records alone; no hand-coded rulings in the decision path | **Done.** 22/22 reproduced (17 book rows + friction, interference, work, kinetic-energy definition, damping). `tests/test_phase0.py` checks that `rule.py` never reads a ruling. |
| 1 Close the joints | The five criteria, tested against all rulings; a list of joints that could not be closed; stop if R1 cannot be stated domain-independently | **Done.** `rule/criteria.yaml` v1. R1 is stated once and decides charge, temperature and entropy (all no) without reference to any domain. Joints that stay open: gravity_call (the book's), form_call, separation_call, reverse_cost, and five R1-undetermined quantities. Two of these (separation_call, reverse_cost) were not in the spec's list; they surfaced while entering the corpus. |
| 2 Corpus | 82+ relations, second-pass physics review, no accidental nulls | **Entered, review pending.** 88 unreflected records across nine domains, at or above every minimum in the spec's table. Every record is schema-valid. All 88 carry `review: pending`; the second pass has not been done. |
| 3 Mechanics remainder | Full pipeline with decoys; damping lands as turns around → culmination blind | **Run (run1).** Damping, friction and interference cancellation reproduced blind at 5/5. Mechanics decoy margin +2.56/+1.78, passed. |
| 4 Unrun domains | Domain by domain, report before the next | **Run (run1), in parallel, deviation noted.** 91 rows, 68 forced after the opponent; per-domain decoy margin failed in five domains (EM, quantum, field theory, stat mech, information), whose rows are excluded as curated pending a better word-swap decoy. |
| 5 Cross-domain | Layers A–C over all forced rows | **Run (run1).** Layer A: 0 collisions. Layer B: 2 confirmed pairs, Ohm dissolved by the C4 sense lint, energy–momentum × row 7 survived. Layer C on partial book text: resolvers split, pair stands. Recorded as open joint `rest_energy_call`. |

## What run 2 needs from the author

0. Rulings on `rest_energy_call` and `cost_count_call` (both surfaced by run 1), recorded as criteria; then the relativity and calibration domains rerun.

## What a real run needs from the author (run 1 ran without items 1–2 via agent sessions; see report deviations)

1. `models.yaml` (copy `models.example.yaml`) and the API keys in the environment. Five generators, three vendors, one open-weights, opponent from a non-majority vendor.
2. A plain-text copy of the paperback for Layer C (`--book`), with `Chapter N` and `[p. N]` markers. Not committed.
3. The two unpublished October rulings, entered in `corpus/calibration/mech.escape_velocity.yaml` and `mech.centripetal_force.yaml` under `ruling.shape`.
4. A second-pass physics reviewer for the 88 records (`review: reviewed:<name>`).
5. Decisions on the open joints, recorded as criteria (never as edits to a row), after the first domain reports exist: whether heat capacity is thermal inertia (before thermodynamics is forced), whether the refractive index is resistance (before waves), whether a separation with no named difficulty counts (before electromagnetism), whether a cost that falls with resistance is covered at all.

## Findings from building it, before any model ran

- **Reading parity is not compositional, by the book's own precedent.** Row 8 is derived from rows 5 and 7, both kept, and turns. So Layer A.4 can only be a collision check at the formula level, where under the October ruling every formula keeps; at the reading level it is informational. The spec's A.4 as written would flag the book's own row 8. The harness reports it as informational instead and says why.
- **Under R1, thermodynamics mostly keeps.** The second law, the third law, the Carnot limit, Landauer and both uncertainty relations are costs or limits with no resistance-carrying quantity in them, so the closed rule keeps their direction, the way it keeps time dilation. The only thermodynamic rows that turn are the ones where mass, thermal resistance or electrical resistance is the thing the cost rises with (latent heat, Fourier, Joule). If the author's intuition is that the third law should turn like row 9, that is a change to R1 (temperature carries resistance), made once.
- **Newton's second law reproduces the book only as a definition.** Read as a law it turns. The book rules it a definition (Ch 2), so the calibration passes, and the alternate is logged under form_call rather than resolved. Torque and centripetal force inherit the same joint.
- **The book's two separation rulings don't settle inverse-square laws.** Rows 2 and interference turn because distance splits something otherwise shared. Coulomb and Newtonian gravitation depend on separation without naming a difficulty. Both readings are encoded; neither row is forced.
- **Superposition keeps and the book says "it isn't add either."** `waves.superposition` (linearity, an identity) will be forced to keep; the book's interference ruling says two vibrations without a point culminate rather than add. That pair is the first thing Layer B should see, and Layer C should find whether Ch 16's "at a point" dissolves it.
