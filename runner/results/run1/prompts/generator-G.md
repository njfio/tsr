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

- Higgs coupling (Yukawa): UNDETERMINED (a judgment call; say so) — the coupling that gives a particle its mass; mass carries resistance (a), and the coupling is monotone in it, but it is a coupling, not a redistribution by geometry. R does not decide it.
- Planck constant: does not carry resistance — a constant
- charge: does not carry resistance — a source / coupling strength; not defined as opposition. The book pairs electric and magnetic as co-creating partners, not as resistance. Decided under R before electromagnetism ran.
- coupling constant: does not carry resistance — interaction strength, not opposition
- energy: does not carry resistance — shared by both sides of the mirror (one E)
- frequency (physical): does not carry resistance — a rate; NB: not TSR Frequency
- gravitational constant G: does not carry resistance — a constant
- gravitational field g: does not carry resistance — an acceleration
- length: does not carry resistance — extent (separation is a relation-level feature)
- mass m: carries resistance — inertial mass is defined as opposition to a change in motion
- momentum: does not carry resistance — a conserved quantity, not an opposition
- potential energy: does not carry resistance — energy
- radius: does not carry resistance — extent
- running coupling: does not carry resistance — interaction strength
- speed of light c: does not carry resistance — the limit, not an opposition
- string tension (QCD): UNDETERMINED (a judgment call; say so) — energy per length of the color flux tube; it opposes separation but is defined as an energy density. R does not decide it.
- time: does not carry resistance — a continuum coordinate
- vacuum energy density: does not carry resistance — energy
- vacuum expectation value: does not carry resistance — a field value
- velocity: does not carry resistance — a rate, not an opposition

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

### field.asymptotic_freedom
```yaml
{
  "id": "field.asymptotic_freedom",
  "title": "Asymptotic freedom",
  "statement": "The strong coupling becomes weak at short distances and high energies: quarks close together interact almost freely, and the interaction grows as they are pulled apart.",
  "formula": "α_s(Q) → 0 as Q → ∞",
  "form": "equation",
  "variables": [
    {
      "name": "strong coupling α_s",
      "quantity": "running coupling",
      "carries_distance": false
    },
    {
      "name": "separation r",
      "quantity": "length",
      "carries_distance": true
    }
  ],
  "costs": [
    {
      "what_gets_harder": "the interaction: it grows with separation",
      "rises_with": [],
      "falls_with": [],
      "separation_made_by_distance": true
    }
  ],
  "physical_terms": {},
  "alternate_statements": [
    {
      "statement": "Read as a running of the coupling with energy scale, with no difficulty named.",
      "form": "equation",
      "costs": []
    }
  ]
}
```

### field.confinement
```yaml
{
  "id": "field.confinement",
  "title": "Confinement",
  "statement": "The force between two quarks does not weaken with separation; the energy stored in the color flux tube grows linearly with distance until it is enough to make a new quark-antiquark pair, so no quark is ever found free.",
  "formula": "V(r) ≈ σ × r",
  "form": "limit",
  "variables": [
    {
      "name": "potential energy V",
      "quantity": "potential energy",
      "carries_distance": false
    },
    {
      "name": "string tension σ",
      "quantity": "string tension (QCD)",
      "carries_distance": false
    },
    {
      "name": "separation r",
      "quantity": "length",
      "carries_distance": true
    }
  ],
  "costs": [
    {
      "what_gets_harder": "pulling the pair apart; impossible to finish",
      "rises_with": [
        "string tension (QCD)"
      ],
      "falls_with": [],
      "separation_made_by_distance": true
    }
  ],
  "physical_terms": {},
  "alternate_statements": []
}
```

### field.cp_violation
```yaml
{
  "id": "field.cp_violation",
  "title": "CP violation",
  "statement": "The weak interaction treats matter and antimatter slightly differently: the combined operation of charge conjugation and parity is not an exact symmetry.",
  "formula": "",
  "form": "equation",
  "variables": [],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### field.gauge_invariance
```yaml
{
  "id": "field.gauge_invariance",
  "title": "Gauge invariance",
  "statement": "Requiring the laws to be unchanged under local phase changes of the matter fields forces the existence of the gauge fields that carry the forces.",
  "formula": "",
  "form": "symmetry",
  "variables": [],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### field.higgs_mechanism
```yaml
{
  "id": "field.higgs_mechanism",
  "title": "Higgs mechanism",
  "statement": "The masses of the W and Z bosons and of the fundamental fermions arise from their coupling to the Higgs field's nonzero vacuum value; a particle's mass is its coupling strength times that value.",
  "formula": "m_f = y_f × v ÷ √2",
  "form": "equation",
  "variables": [
    {
      "name": "fermion mass m_f",
      "quantity": "mass m",
      "carries_distance": false
    },
    {
      "name": "Yukawa coupling y_f",
      "quantity": "Higgs coupling (Yukawa)",
      "carries_distance": false
    },
    {
      "name": "vacuum expectation value v",
      "quantity": "vacuum expectation value",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### field.noether
```yaml
{
  "id": "field.noether",
  "title": "Noether's theorem",
  "statement": "Every continuous symmetry of the action corresponds to a conserved quantity: time translation to energy, space translation to momentum, rotation to angular momentum, phase to charge.",
  "formula": "",
  "form": "identity",
  "variables": [
    {
      "name": "energy",
      "quantity": "energy",
      "carries_distance": false
    },
    {
      "name": "momentum",
      "quantity": "momentum",
      "carries_distance": false
    },
    {
      "name": "charge",
      "quantity": "charge",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### field.running_couplings
```yaml
{
  "id": "field.running_couplings",
  "title": "Running couplings",
  "statement": "The strengths of the interactions depend on the energy scale at which they are probed: the electromagnetic coupling grows with energy, the strong coupling falls.",
  "formula": "",
  "form": "equation",
  "variables": [
    {
      "name": "running coupling",
      "quantity": "running coupling",
      "carries_distance": false
    },
    {
      "name": "energy scale",
      "quantity": "energy",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### field.vacuum_energy
```yaml
{
  "id": "field.vacuum_energy",
  "title": "Vacuum energy",
  "statement": "The quantum vacuum has an energy density; the value field theory estimates and the value cosmology measures differ by many orders of magnitude.",
  "formula": "",
  "form": "definition",
  "variables": [
    {
      "name": "vacuum energy density",
      "quantity": "vacuum energy density",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### field.weak_flavor_change
```yaml
{
  "id": "field.weak_flavor_change",
  "title": "Flavor change via the weak interaction",
  "statement": "Only the weak interaction changes one kind of quark or lepton into another (through the charged W boson); the strong and electromagnetic interactions never do.",
  "formula": "",
  "form": "identity",
  "variables": [
    {
      "name": "coupling constant",
      "quantity": "coupling constant",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### field.yukawa_range
```yaml
{
  "id": "field.yukawa_range",
  "title": "Virtual particles and the range of a force",
  "statement": "A force carried by exchange of a virtual particle has a range of about the reduced Planck constant over the mediator's mass times c: the heavier the mediator, the shorter the reach.",
  "formula": "r ≈ ħ ÷ (m × c)",
  "form": "equation",
  "variables": [
    {
      "name": "range r",
      "quantity": "length",
      "carries_distance": false
    },
    {
      "name": "mediator mass m",
      "quantity": "mass m",
      "carries_distance": false
    },
    {
      "name": "speed of light c",
      "quantity": "speed of light c",
      "carries_distance": false
    },
    {
      "name": "Planck constant ħ",
      "quantity": "Planck constant",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "reaching far; the force's range",
      "rises_with": [],
      "falls_with": [
        "mass m"
      ],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {},
  "alternate_statements": []
}
```

### rel.energy_momentum_relation
```yaml
{
  "id": "rel.energy_momentum_relation",
  "title": "Energy-momentum relation",
  "statement": "A body's energy squared equals its momentum times c squared plus its rest energy squared; for a massless particle the energy is momentum times c.",
  "formula": "E² = (p × c)² + (m × c²)²",
  "form": "identity",
  "variables": [
    {
      "name": "energy E",
      "quantity": "energy",
      "carries_distance": false
    },
    {
      "name": "momentum p",
      "quantity": "momentum",
      "carries_distance": false
    },
    {
      "name": "mass m",
      "quantity": "mass m",
      "carries_distance": false
    },
    {
      "name": "speed of light c",
      "quantity": "speed of light c",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### rel.equivalence_principle
```yaml
{
  "id": "rel.equivalence_principle",
  "title": "Equivalence principle",
  "statement": "Gravitational mass equals inertial mass, so a freely falling observer feels no gravity: locally, free fall is indistinguishable from the absence of gravitation.",
  "formula": "",
  "form": "identity",
  "variables": [
    {
      "name": "mass m",
      "quantity": "mass m",
      "carries_distance": false
    },
    {
      "name": "gravitational field g",
      "quantity": "gravitational field g",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### rel.gravitational_time_dilation
```yaml
{
  "id": "rel.gravitational_time_dilation",
  "title": "Gravitational time dilation",
  "statement": "A clock deeper in a gravitational well runs slower than one higher up; the effect depends on depth in the well, not on the clock's own mass.",
  "formula": "Δt = Δτ ÷ √(1 − 2 × G × M ÷ (r × c²))",
  "form": "equation",
  "variables": [
    {
      "name": "proper time Δτ",
      "quantity": "time",
      "carries_distance": false
    },
    {
      "name": "central mass M",
      "quantity": "mass m",
      "carries_distance": false
    },
    {
      "name": "radius r",
      "quantity": "radius",
      "carries_distance": false
    },
    {
      "name": "gravitational constant G",
      "quantity": "gravitational constant G",
      "carries_distance": false
    },
    {
      "name": "speed of light c",
      "quantity": "speed of light c",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### rel.null_interval
```yaml
{
  "id": "rel.null_interval",
  "title": "Null interval",
  "statement": "Along a light ray the space-time interval is zero: no proper time passes for light, and its energy depends on who measures it.",
  "formula": "ds² = 0",
  "form": "identity",
  "variables": [
    {
      "name": "speed of light c",
      "quantity": "speed of light c",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### rel.relativistic_doppler
```yaml
{
  "id": "rel.relativistic_doppler",
  "title": "Relativistic Doppler effect",
  "statement": "Light from a source receding at speed v is received at a lower frequency by the factor square root of (1 − β) over (1 + β); approaching, higher. No medium is involved and only the relative velocity matters.",
  "formula": "f' = f × √((1 − β) ÷ (1 + β))",
  "form": "equation",
  "variables": [
    {
      "name": "emitted frequency f",
      "quantity": "frequency (physical)",
      "carries_distance": false
    },
    {
      "name": "relative velocity v",
      "quantity": "velocity",
      "carries_distance": false
    },
    {
      "name": "speed of light c",
      "quantity": "speed of light c",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### rel.velocity_addition
```yaml
{
  "id": "rel.velocity_addition",
  "title": "Relativistic velocity addition",
  "statement": "Velocities compose so that the result never exceeds c: the combined speed is the sum divided by one plus the product over c squared.",
  "formula": "u' = (u + v) ÷ (1 + u × v ÷ c²)",
  "form": "identity",
  "variables": [
    {
      "name": "velocity u",
      "quantity": "velocity",
      "carries_distance": false
    },
    {
      "name": "velocity v",
      "quantity": "velocity",
      "carries_distance": false
    },
    {
      "name": "speed of light c",
      "quantity": "speed of light c",
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

Return a JSON ARRAY with one such object per relation, in the order given, and nothing else in the file. Write it to the file `runner/results/run1/raw/<MODEL>/batch-G.json` and then reply with the single word DONE. Do not read any other file, do not search the web, do not look at the repository.