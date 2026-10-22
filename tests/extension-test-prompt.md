# TSR extension test: generator prompt

You're helping test a framework called the Theory of Sovereign Reflectivity (TSR), set out in the book *The Sovereign Mirror* (Nicholas Ferguson, 2026). TSR reflects physics onto a "nonphysical" side using one rule. The book reflects a few dozen physics relations. Your job is to apply the same rule, exactly as written below, to relations the book doesn't cover, and to report honestly where the result holds up and where it doesn't.

Ground rules:

- Use only the material in this prompt. Don't search the web. If you know anything else about TSR or this book, set it aside, and say so at the end.
- Be strict, not generous. A reflection that reads as nonsense in TSR's own terms is a useful result. Don't rescue it with creative reinterpretation.
- Don't invent TSR words silently. If a physical term has no partner below, say so, and mark any word you introduce as NEW.
- Apply the rule as stated, even where you think it's wrong. Put your disagreement in the closing paragraph, not in the reflections.

## The rule

> "So you take the world Einstein described and reflect it: keep each relationship, and flip the condition. Resistant becomes receptive, limited becomes limitless, radiating becomes collecting. ... Every term reflects; that part always happens. What you have to know is whether the relationship keeps its shape or turns around."

The deciding question for each relation, in the book's words: "One is an equivalence. The other is a cost that rises with resistance."

- Equivalences, definitions, identities and conservation laws keep their shape.
- A cost or a limit caused by resistance turns around: what gets harder with more resistance gets easier with more receptivity. In TSR, mass is resistance, and distance is "what resistance makes."
- "Units don't cross the mirror, only relationships do." Nothing on the nonphysical side has a number or a distance.

## The reflections the book already gives

| Physical | Nonphysical | Meaning in the book |
| --- | --- | --- |
| mass m | Movement M | Mass is "resistance to a change in motion. So its reflection is receptivity to a change in motion." |
| density | Desire | "What is wanted"; "how much wanting is packed into a Movement, how concentrated it is." |
| volume | Vibrance | "How much of the Movement is vibrating: its extent in Vibration." |
| mass = density × volume | Movement = Desire × Vibrance | |
| space | Vibration | With no distance, particulars "differ by how they vibrate." |
| time | Expansion | "What the Current does, and can't undo." |
| velocity (space over time) | Vibration over Expansion | "It isn't a speed... It's how much a Movement's vibration rises per Expansion." |
| acceleration | Appreciation | "How a Movement's rising changes, its quickening or slowing," which "comes down to how much of the Current's pull on you you're letting move you." |
| force = mass × acceleration | Frequency = Movement × Appreciation | "Frequency is what you feel, and a change in Frequency is what you notice." "Force reads how hard you're pushed against resistance, Frequency reads how freely you're yielding to receptivity." |
| speed of light c | the Current C | "The whole, flowing, always at the furthest point it has reached"; the same for every entity. |
| E = m × c² | C² × M = E | One E, shared by both sides, at the center. |
| momentum through time, m × c | M × C | "A Movement that isn't changing in Vibration is still expanding with the Current. That expansion, M × C, is its momentum." |
| electric, magnetic | Idle, Reflected | The pair that makes light, and the pair that makes the Current. |
| radiation | collection | |
| gravity | Attraction and Vortexes | "What you've already expanded into draws you toward it." |
| focus | Tune | |
| manifestation | imagination | |
| empirical evidence | emotional evidence | "Force, measured" and "Frequency, felt. The level is a feeling; a change in the level is an emotion." |
| the Now, the Past | the Future, the Current | Two of the four directions of energy flow. |
| Belief, Expectation | Desire, Intuition | Straight across the mirror. |
| strong force (Expectation), weak force (Belief) | strong frequency (Desire), weak frequency (Intuition) | Paired diagonally, through the center. |
| Objective Reality, Subjective Reality, Space-Time | Collective Reality, Vibrational Reality, Vibration-Expansion | |

## Rulings the book already makes

- E = m × c² keeps its shape: "an equivalence."
- F = m × a keeps its product: Frequency = Movement × Appreciation.
- mass = density × volume keeps: Movement = Desire × Vibrance.
- Time dilation and length contraction keep (no mass in them): Expansion Dilation and Vibrational Contraction.
- The cost of more speed turns around: "The faster an object moves, the more energy it takes to speed it up further. Reflected, and inverted: the closer you move to the Current, the more receptive you become, so each next step takes less."
- The limit turns around: "Nothing with mass can reach the speed of light... Nonphysically, nothing a Movement expands into can ever fall short of it."
- Simultaneity turns around: physically, two observers moving relative to each other don't share a now, because of distance; nonphysically, "every Movement shares the Current's now."
- Newton's third law keeps (an identity): "everything that goes Out Through lands In From on somebody, the same act running the other way, as a real return."
- Conservation laws keep (identities).

## Relations to reflect

1. Momentum through space: p = m × v.
2. Work: W = F × d (force times distance).
3. Power: P = F × v.
4. Kinetic energy: K = ½ × m × v².
5. Impulse: J = F × t, which equals the change in momentum.
6. Weight: w = m × g.
7. Friction: resistance between two surfaces sliding past each other; it turns motion into heat (F = μ × N).
8. Hooke's law: a spring pushes back in proportion to how far it is stretched (F = −k × x).
9. Centripetal force: keeping a mass on a curved path takes F = m × v² ÷ r.
10. Gravitational potential energy: U = m × g × h.
11. Pressure and Boyle's law: pressure is force per area (P = F ÷ A); with the amount of gas and its temperature held steady, squeezing the volume raises the pressure (P × V stays constant).
12. Wave interference: two waves in opposite phase cancel at a point.
13. Conservation of momentum: in a closed system, total momentum stays constant.
14. Newton's first law: a body keeps its state of motion unless a force acts on it.
15. Escape velocity: the speed needed to leave a planet rises with the planet's mass (v = √(2GM ÷ r)).

## What to report

Return a JSON array with one object per relation, using exactly these keys:

```json
{
  "id": 1,
  "physical": "the relation as given",
  "reflected_formula": "the reflection in TSR words, with × ÷ and so on",
  "reflected_sentence": "one plain sentence",
  "shape": "keeps | turns around | no partner",
  "rule_reason": "equivalence or definition, or which cost or limit caused by resistance",
  "unmapped_terms": ["physical terms with no partner above"],
  "new_words": ["any word you introduced, marked NEW"],
  "interpretation": "2 or 3 sentences: what it would mean in a person's life, using only the meanings above",
  "conflicts": "any book claim above that it contradicts, quoted, or \"none\"",
  "sense": 1,
  "confidence": 1
}
```

- **sense** (1–7): 1 = nonsense in TSR's own terms; 4 = coherent but says nothing new; 7 = coherent, and says something true-feeling the book doesn't.
- **confidence** (1–7): how sure you are of the keeps-or-turns-around call under the rule as stated.

If a relation can't be reflected without a NEW word, still give your best reflection and lower its sense score.

After the JSON, write one short paragraph: which items the rule decided on its own, which needed a judgment call, and where the rule as stated was ambiguous. End with one line saying whether you knew anything about TSR beyond this prompt.
