# TSR extension test: answer key and scoring

Don't give this file to the AI you're testing.

## Hidden calibration items

Three of the fifteen relations are ones the book already reflects, in Chapter 16. The prompt doesn't give their answers. If independent AIs land where the book did, the rule is determinate enough that someone else running it reaches your result.

| Item | Book's ruling | Book's words (Ch 16) |
| --- | --- | --- |
| 7. Friction | turns around → resonance | "It depends on resistance, so it turns around: two Movements meeting don't lose to each other, they build each other up. That's resonance." |
| 11. Pressure and Boyle's law | pressure exists only where the two sides touch; Boyle keeps its shape | "Walls are resistance, so there's nothing on the nonphysical side for pressure to be. It can only exist where the two sides touch, and there it's the Current pressing against the resistance of your experience." "Hold the Movement steady and squeeze how much of you is vibrating, and the same wanting gets packed denser against the same resistance... Where it presses, it's the gap, felt." |
| 12. Wave interference | no cancellation; vibrations culminate (resonance); conservation keeps | "Cancellation happens at a point... A location is a distance from somewhere, and distance is what resistance makes... What two vibrations do there isn't cancel, and it isn't add either. It's culminate, which is resonance again." |

Item 1 also touches the book: it reflects momentum *through time* as M × C (Ch 17). The prompt gives that, so a conflict check on item 1 is fair game.

## How to score the runs

1. **Calibration.** For items 7, 11 and 12, did each AI reach the book's direction and the same idea (resonance; pressure only at the crossing; culmination)? Count matches out of 3 per AI.
2. **Determinacy.** For each of the 12 new items, do the AIs agree on the keeps-or-turns-around call and on the TSR words used? Agreement means the rule decides; disagreement marks a judgment call (the "constrained" or "open" column).
3. **Sense.** Median sense score per item across AIs, and which items needed NEW words.
4. **Conflicts.** Any reflection that contradicts a book claim, flagged by two or more AIs.

## Round 2 (blind)

The round-1 replies feed a blind list: each item's consensus reflection, plus a decoy with the direction flipped and a decoy with other TSR words swapped in. Fresh sessions rate them without knowing which is which. If the rule's reflections don't outscore the decoys, the mirror was being curated rather than run. That round is `round2-prompt.md`, with its key in `round2-key.md`.
