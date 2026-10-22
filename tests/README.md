# Testing TSR

These tests check whether TSR's one rule does what *The Sovereign Mirror* says it does: that it decides how each piece of physics reflects, rather than the author placing each word by hand. They test coherence, not truth. A perfectly consistent table could still describe nothing real.

The model, the prompts and the blind statements were built with Claude (Anthropic). Every input is in this folder, so anyone can rerun or dispute a step.

## 1. Internal checks

`tsr_formal.py` is a first formal model of the Map: the table as an olog (a structure of types and the relations between them) and the rule as an operation on directions ("rises with" or "falls as"). Run `python3 tsr_formal.py`; the output is in `results.txt`. Cells that are judgments rather than quotations are marked in the script.

| Check | Result on the final text |
| --- | --- |
| Composition | All five stated formulas carry across intact: velocity, acceleration, mass, force, energy. |
| Mirror twice | One-to-one except at two words with two roles each, as the book intends: the Current (c and the Past) and Desire (density and Belief). |
| The rule against the book's own 17 rulings | Chapter 16's wording, "an equivalence" keeps and "a cost that rises with resistance" turns around, matches 17. Chapter 2's first clause alone matches 10. |
| Frequency as a product or a ratio | Only the book's product, Movement × Appreciation, guarantees that Frequency rises with alignment. |
| Constraint count, one slot (a demo) | Of 11 candidate words for the Current's slot, only "Current" meets the book's three requirements: the flow, the collecting and the present moment. |

One structural finding: row 8 is built from rows the book keeps (rows 5 and 7), yet the book turns it around. So the mirror acts on claims about difficulty, not on formulas.

## 2. The extension test

`extension-test-prompt.md` gives an AI the rule, the Map and the book's rulings, and asks it to reflect 15 physics relations the book doesn't cover. Three are hidden calibration items the book does reflect: friction, pressure and Boyle's law, and wave interference. Their answers are in `extension-test-key.md`.

Run on 22 October 2026 with five AIs (Astra, Kimi K3, Fable 5.1, Argon, Grok 4.7). Raw answers are in `results/round1.json`.

- 8 of the 15 drew a unanimous call on keep versus turn around.
- Friction: all five turned it around, as the book does.
- Interference: one of five reached the book's answer, that vibrations can't cancel because a point needs distance.
- Every split was a relation that is both a definition and a cost: work, power, kinetic energy, centripetal force, potential energy.
- Four of five found that kinetic energy, kept as a definition, clashes with row 8.

## 3. The blind round

`round2-prompt.md` holds 30 statements: the rule's reflections from round 1, each beside a decoy with the direction reversed and a decoy with other TSR words swapped in. Fresh sessions rated them against TSR's meanings without knowing which was which. Two of the ten sets are controls taken from the book. The key is in `round2-key.md`, the ratings in `results/round2-ratings.json`.

- Four valid judges. The rule's version topped its set in 27 of 32 cases, where chance would give about 1 in 3.
- Mean rating: 4.8 for the rule's reflections, 1.9 for the reversed decoys, 2.8 for the swapped ones.
- Weakest row: escape velocity. In TSR a pull draws you toward what you've expanded into, so there's nothing to escape.
- One statement, the first law, was worded by the test builder in a way that made feeling the cause of change. Frequency is how a change is felt, not what causes it.
- A fifth judge rated nearly everything 4, controls included, and was excluded by the rule set before scoring.

## What the tests leave open

1. Which wins when a relation is both a definition and a cost?
2. How is a law written once it turns around? Five AIs reversed Hooke's law five different ways.
3. The vocabulary ends at mechanics: temperature, waves, phase and heat have no partners.
4. Kinetic energy kept as a definition clashes with row 8.
5. Escape velocity may not have a reflection at all.

## Run it yourself

Paste a prompt into a fresh chat with web search off. Don't give it the book, the site or the key. If your results differ, or you find a sixth open question, [open an issue](https://github.com/njfio/tsr/issues).
