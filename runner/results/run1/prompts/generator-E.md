ROLE: generator

You're helping test a framework called the Theory of Sovereign Reflectivity (TSR). TSR reflects physics onto a "nonphysical" side using one rule. Your job is to apply the rule, exactly as written below, to each of the physics relations below, one at a time, and to report honestly where the result holds up and where it doesn't.

Ground rules:

- Use only the material in this prompt. Don't search the web. If you know anything else about TSR, set it aside, and say so in the `knew_tsr` field.
- Be strict, not generous. A reflection that reads as nonsense in TSR's own terms is a useful result. Don't rescue it with creative reinterpretation.
- The vocabulary below is frozen. If a physical term has no partner, say so in `unmapped_terms`. Any word you introduce goes in `new_words`, and a row with new words is recorded as "no partner".
- Apply the rule as stated, even where you think it's wrong. Put your disagreement in `closing`, never in the reflection.
- Do not rewrite the formula. A relation that turns around keeps its formula in the table's terms; what turns is its reading (harder becomes easier, unreachable becomes already there).

## The rule

> "Keep each relationship, and flip the condition. Resistant becomes receptive, limited becomes limitless, radiating becomes collecting. ... Every term reflects; that part always happens. What you have to know is whether the relationship keeps its shape or turns around."

The deciding question: "One is an equivalence. The other is a cost that rises with resistance."

- Equivalences, definitions, identities, conservation laws and symmetries keep their shape.
- A cost or a limit caused by resistance turns around: what gets harder with more resistance gets easier with more receptivity. Mass is resistance, and distance is "what resistance makes." A separation made by distance also turns around.
- A statement with an odd number of such costs turns around; with none or an even number it keeps.
- "Units don't cross the mirror, only relationships do." Nothing on the nonphysical side has a number, a unit or a distance.

## Which quantities carry resistance (fixed before this run)

- Poynting vector: does not carry resistance — an energy flux
- charge: does not carry resistance — a source / coupling strength; not defined as opposition. The book pairs electric and magnetic as co-creating partners, not as resistance. Decided under R before electromagnetism ran.
- current (electric): does not carry resistance — a flow
- electric field: does not carry resistance — force per charge
- electric flux: does not carry resistance — a field integral
- electrical resistance: carries resistance — defined as opposition to current (V / I)
- force: does not carry resistance — not defined as opposition
- impedance: carries resistance — generalized opposition to alternating current
- inductance: carries resistance — opposition to a change in current (Lenz / Faraday)
- length: does not carry resistance — extent (separation is a relation-level feature)
- magnetic field: does not carry resistance — a field
- magnetic flux: does not carry resistance — a field integral
- permeability: does not carry resistance — a medium constant
- permittivity: does not carry resistance — a medium constant
- reactance: carries resistance — opposition to change of current or voltage
- speed of light c: does not carry resistance — the limit, not an opposition
- time: does not carry resistance — a continuum coordinate
- voltage: does not carry resistance — energy per charge

## The frozen vocabulary

| Physical | Nonphysical | Map row |
| --- | --- | --- |
| limited | limitless | property |
| resistant | receptive | property |
| radiation | collection | property |
| Subjective Reality | Vibrational Reality | reality |
| Objective Reality | Collective Reality | reality |
| Space-Time | Vibration-Expansion | continuum |
| empirical evidence | emotional evidence | evidence |
| Now | Future | energy flow |
| Past | Current | energy flow |
| Belief | Desire | entity contrast |
| Expectation | Intuition | entity contrast |
| speed of light c | Current | symbol |
| mass m | Movement M | symbol |
| Focus | Tune | entity action |
| electric | Idle | co-creating partner |
| magnetic | Reflected | co-creating partner |
| density | Desire | co-creating partner |
| volume | Vibrance | co-creating partner |
| physical energy | conscious energy | energy |
| actualization | realization | transmutation |
| Out Through | Out For | entity transmutation |
| In From | In To | entity transmutation |
| space | Vibration | reflected partnership |
| time | Expansion | reflected partnership |
| velocity | rise per Expansion | reflected partnership |
| acceleration | Appreciation | reflected partnership |
| manifestation | imagination | reflected partnership |
| force | Frequency | reflected partnership |
| gravitational pull | Attraction | gravity |
| gravity well | Vortex | gravity |
| gravitational lensing | Convergence | gravity |
| time dilation | Expansion Dilation | named reflection |
| length contraction | Vibrational Contraction | named reflection |
| friction | resonance | named reflection |
| entropy | Culmination (provisional) | named reflection |
| momentum | momentum | momentum |

Other legal nonphysical words: alignment (how little you resist; the nonphysical measure of nearness to the Current), receptivity (the flipped condition), the gap (resistance's only appearance on the nonphysical side: between the Current and what you're living), Point of Reflection (center of the crossing; where energy changes form), the Present (the whole equation C^2 x M = E = m x c^2), E (the one energy / the entity, shared by both sides), Awareness (limitless and limited met), Attraction (receptive and resistant met (entity property) and gravity's reflection), Momentum (collecting and radiating met), wanting (Desire in plain speech), culminate (verb of Culmination; what two vibrations do instead of cancel (Ch 16)), strong frequency (Desire), weak frequency (Intuition and imagination)

Words that must never appear on the nonphysical side: boundary, distance, edge, effort, inside, judgment, location, mental, mind, outside, place, radiate, radiates, radiating, rank, resistance, speed, time, travel, will.

## Traps (refuse each one)

- No distance, time, location, travel or quantities on the nonphysical side.
- No resistance on the nonphysical side; it appears only as the gap.
- No entity properties (Awareness, Momentum as a property) on things that are not entities.
- "Nonphysical" does not mean "mental".
- Frequency is not a rate and not cycles per second.
- No sums where the book has products.
- No physical words in disguise: belief, expectation, will, effort, judgment, rank belong to the physical side.

## The relations

Take each one on its own. Do not let one relation's reflection decide another's; the rule decides each.

### em.coulomb
```yaml
{
  "id": "em.coulomb",
  "title": "Coulomb's law",
  "statement": "Two charges push or pull with a force proportional to the product of the charges and inversely proportional to the square of their separation.",
  "formula": "F = k × q1 × q2 ÷ r²",
  "form": "equation",
  "variables": [
    {
      "name": "force F",
      "quantity": "force",
      "carries_distance": false
    },
    {
      "name": "charge q",
      "quantity": "charge",
      "carries_distance": false
    },
    {
      "name": "separation r",
      "quantity": "length",
      "carries_distance": true
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": [
    {
      "statement": "Read as a separation cost: the interaction between the charges is weakened by their separation.",
      "form": "equation",
      "costs": [
        {
          "what_gets_harder": "the interaction, weakened by separation",
          "rises_with": [],
          "falls_with": [],
          "separation_made_by_distance": true
        }
      ]
    }
  ]
}
```

### em.displacement_current
```yaml
{
  "id": "em.displacement_current",
  "title": "Maxwell's displacement current",
  "statement": "A changing electric field acts as a source of magnetic field just as a current does, which closes the symmetry between the two fields and makes electromagnetic waves possible.",
  "formula": "∇ × B = μ0 × J + μ0 × ε0 × dE ÷ dt",
  "form": "symmetry",
  "variables": [
    {
      "name": "electric field E",
      "quantity": "electric field",
      "carries_distance": false
    },
    {
      "name": "magnetic field B",
      "quantity": "magnetic field",
      "carries_distance": false
    },
    {
      "name": "time t",
      "quantity": "time",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### em.faraday
```yaml
{
  "id": "em.faraday",
  "title": "Faraday's law",
  "statement": "A changing magnetic flux through a loop induces an electromotive force equal to the rate of change of the flux.",
  "formula": "EMF = dΦ_B ÷ dt",
  "form": "equation",
  "variables": [
    {
      "name": "electromotive force",
      "quantity": "voltage",
      "carries_distance": false
    },
    {
      "name": "magnetic flux Φ_B",
      "quantity": "magnetic flux",
      "carries_distance": false
    },
    {
      "name": "time t",
      "quantity": "time",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### em.gauss
```yaml
{
  "id": "em.gauss",
  "title": "Gauss's law",
  "statement": "The electric flux through any closed surface equals the enclosed charge divided by the permittivity of free space.",
  "formula": "Φ_E = Q ÷ ε0",
  "form": "identity",
  "variables": [
    {
      "name": "electric flux Φ_E",
      "quantity": "electric flux",
      "carries_distance": false
    },
    {
      "name": "enclosed charge Q",
      "quantity": "charge",
      "carries_distance": false
    },
    {
      "name": "permittivity ε0",
      "quantity": "permittivity",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### em.impedance
```yaml
{
  "id": "em.impedance",
  "title": "Impedance",
  "statement": "In an alternating-current circuit the ratio of voltage to current is the impedance, whose magnitude combines resistance with the inductive and capacitive reactances.",
  "formula": "|Z| = √(R² + (X_L − X_C)²)",
  "form": "definition",
  "variables": [
    {
      "name": "impedance Z",
      "quantity": "impedance",
      "carries_distance": false
    },
    {
      "name": "resistance R",
      "quantity": "electrical resistance",
      "carries_distance": false
    },
    {
      "name": "reactance X",
      "quantity": "reactance",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### em.lenz_inductance
```yaml
{
  "id": "em.lenz_inductance",
  "title": "Lenz's law and self-inductance",
  "statement": "An induced current flows so as to oppose the change that produced it; a coil opposes a change in its own current with a back-EMF proportional to its inductance.",
  "formula": "EMF = L × dI ÷ dt",
  "form": "equation",
  "variables": [
    {
      "name": "back-EMF",
      "quantity": "voltage",
      "carries_distance": false
    },
    {
      "name": "inductance L",
      "quantity": "inductance",
      "carries_distance": false
    },
    {
      "name": "current I",
      "quantity": "current (electric)",
      "carries_distance": false
    },
    {
      "name": "time t",
      "quantity": "time",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "changing the current",
      "rises_with": [
        "inductance"
      ],
      "falls_with": [],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {},
  "alternate_statements": []
}
```

### em.mutual_induction
```yaml
{
  "id": "em.mutual_induction",
  "title": "Mutual induction",
  "statement": "A changing current in one coil induces an EMF in a nearby coil in proportion to their mutual inductance, which depends on their geometry and how much flux they share.",
  "formula": "EMF_2 = M × dI_1 ÷ dt",
  "form": "equation",
  "variables": [
    {
      "name": "induced EMF",
      "quantity": "voltage",
      "carries_distance": false
    },
    {
      "name": "mutual inductance M",
      "quantity": "inductance",
      "carries_distance": false
    },
    {
      "name": "current I_1",
      "quantity": "current (electric)",
      "carries_distance": false
    },
    {
      "name": "time t",
      "quantity": "time",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### em.ohm_cost
```yaml
{
  "id": "em.ohm_cost",
  "title": "Ohm's law (the cost reading)",
  "statement": "For a given voltage, the current that flows falls as the resistance rises.",
  "formula": "I = V ÷ R",
  "form": "equation",
  "variables": [
    {
      "name": "resistance R",
      "quantity": "electrical resistance",
      "carries_distance": false
    },
    {
      "name": "voltage V",
      "quantity": "voltage",
      "carries_distance": false
    },
    {
      "name": "current I",
      "quantity": "current (electric)",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "current flowing for a given voltage",
      "rises_with": [
        "electrical resistance"
      ],
      "falls_with": [],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {},
  "alternate_statements": []
}
```

### em.ohm_definition
```yaml
{
  "id": "em.ohm_definition",
  "title": "Ohm's law (the definition of resistance)",
  "statement": "Resistance is the ratio of the voltage across a conductor to the current through it.",
  "formula": "R = V ÷ I",
  "form": "definition",
  "variables": [
    {
      "name": "resistance R",
      "quantity": "electrical resistance",
      "carries_distance": false
    },
    {
      "name": "voltage V",
      "quantity": "voltage",
      "carries_distance": false
    },
    {
      "name": "current I",
      "quantity": "current (electric)",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### em.poynting
```yaml
{
  "id": "em.poynting",
  "title": "Poynting flux",
  "statement": "The energy carried by an electromagnetic field per unit area per unit time is the cross product of the electric and magnetic fields over the permeability.",
  "formula": "S = E × B ÷ μ0",
  "form": "definition",
  "variables": [
    {
      "name": "Poynting vector S",
      "quantity": "Poynting vector",
      "carries_distance": false
    },
    {
      "name": "electric field E",
      "quantity": "electric field",
      "carries_distance": false
    },
    {
      "name": "magnetic field B",
      "quantity": "magnetic field",
      "carries_distance": false
    },
    {
      "name": "permeability μ0",
      "quantity": "permeability",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {
    "S": "Poynting vector",
    "E": "electric",
    "B": "magnetic",
    "μ0": "permeability"
  },
  "alternate_statements": []
}
```

### em.wave_propagation
```yaml
{
  "id": "em.wave_propagation",
  "title": "Electromagnetic wave propagation",
  "statement": "A changing electric field makes a magnetic field and a changing magnetic field makes an electric field; the pair regenerates itself and travels at a speed fixed by the permittivity and permeability of free space.",
  "formula": "c = 1 ÷ √(ε0 × μ0)",
  "form": "identity",
  "variables": [
    {
      "name": "speed of light c",
      "quantity": "speed of light c",
      "carries_distance": false
    },
    {
      "name": "electric field E",
      "quantity": "electric field",
      "carries_distance": false
    },
    {
      "name": "magnetic field B",
      "quantity": "magnetic field",
      "carries_distance": false
    },
    {
      "name": "permittivity ε0",
      "quantity": "permittivity",
      "carries_distance": false
    },
    {
      "name": "permeability μ0",
      "quantity": "permeability",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

## What to report
Return ONE JSON object with exactly these keys:

```json
{
  "id": "<the relation id>",
  "physical": "the relation as given",
  "reflected_formula": "the word-map image of the formula, in frozen words, with × ÷ and so on (empty if the relation has no formula)",
  "reflected_sentence": "one plain sentence",
  "shape": "keeps | turns around | no partner",
  "rule_reason": "equivalence or definition, or which cost or limit caused by resistance, or which separation",
  "rule_trace": ["which of these fired: identity, resistance-cost, separation, none"],
  "forced": true,
  "unmapped_terms": [],
  "new_words": [],
  "monotone_claims": [{"rises": "a frozen word", "with": "a frozen word or 'alignment'", "sign": 1}],
  "interpretation": "2 or 3 sentences, frozen words only",
  "conflicts": "any claim in the vocabulary table it contradicts, quoted, or \"none\"",
  "sense": 1,
  "confidence": 1,
  "closing": "one short paragraph: did the rule decide on its own, or did you need a judgment call? where was it ambiguous?",
  "knew_tsr": false
}
```

`forced` is true only if the rule decided without a judgment call. `sense` 1–7 (1 = nonsense in TSR's terms; 7 = coherent and says something the table doesn't). `confidence` 1–7 on the keeps-or-turns call.

Return a JSON ARRAY with one such object per relation, in the order given, and nothing else in the file. Write it to the file `runner/results/run1/raw/<MODEL>/batch-E.json` and then reply with the single word DONE. Do not read any other file, do not search the web, do not look at the repository.