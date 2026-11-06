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

- amplitude: does not carry resistance — extent of oscillation
- angle: does not carry resistance — geometry
- aperture width: does not carry resistance — extent
- dispersion: does not carry resistance — a dependence, not an opposition
- frequency (physical): does not carry resistance — a rate; NB: not TSR Frequency
- group velocity: does not carry resistance — a rate
- index contrast: UNDETERMINED (a judgment call; say so) — difference of refractive indices across a boundary; inherits the refractive index joint
- length: does not carry resistance — extent (separation is a relation-level feature)
- phase: does not carry resistance — an angle
- phase velocity: does not carry resistance — a rate
- probability: does not carry resistance — a measure
- quantum number: does not carry resistance — a count
- refractive index: UNDETERMINED (a judgment call; say so) — n = c/v: the factor by which a medium slows light. Physics defines it as a ratio of speeds, not as opposition; but the Ch 16 reading of diffraction ('where the Current meets resistance, it diffracts') treats the medium as resistance. R does not decide it.
- velocity: does not carry resistance — a rate, not an opposition
- wave speed: does not carry resistance — a rate
- wavelength: does not carry resistance — extent
- wavenumber: does not carry resistance — inverse extent

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

### waves.diffraction
```yaml
{
  "id": "waves.diffraction",
  "title": "Diffraction",
  "statement": "A wave passing through an aperture spreads; the narrower the aperture compared with the wavelength, the wider the spread.",
  "formula": "sin θ ≈ λ ÷ a",
  "form": "equation",
  "variables": [
    {
      "name": "spreading angle θ",
      "quantity": "angle",
      "carries_distance": false
    },
    {
      "name": "wavelength λ",
      "quantity": "wavelength",
      "carries_distance": false
    },
    {
      "name": "aperture width a",
      "quantity": "aperture width",
      "carries_distance": true
    }
  ],
  "costs": [
    {
      "what_gets_harder": "passing through without spreading",
      "rises_with": [],
      "falls_with": [],
      "separation_made_by_distance": true
    }
  ],
  "physical_terms": {},
  "alternate_statements": [
    {
      "statement": "Read as a plain relation between spread, wavelength and aperture, with no difficulty named.",
      "form": "equation",
      "costs": []
    }
  ]
}
```

### waves.dispersion
```yaml
{
  "id": "waves.dispersion",
  "title": "Dispersion",
  "statement": "In a dispersive medium the phase velocity depends on wavelength, so a pulse made of many wavelengths spreads as it travels.",
  "formula": "v_p = v_p(λ)",
  "form": "equation",
  "variables": [
    {
      "name": "phase velocity v_p",
      "quantity": "phase velocity",
      "carries_distance": false
    },
    {
      "name": "wavelength λ",
      "quantity": "wavelength",
      "carries_distance": false
    },
    {
      "name": "dispersion",
      "quantity": "dispersion",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "a pulse keeping its shape",
      "rises_with": [
        "dispersion"
      ],
      "falls_with": [],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {},
  "alternate_statements": []
}
```

### waves.doppler
```yaml
{
  "id": "waves.doppler",
  "title": "Doppler effect (waves in a medium)",
  "statement": "A receiver moving toward a source, or a source moving toward a receiver, measures a higher frequency than the one emitted; moving apart, a lower one.",
  "formula": "f' = f × (v + v_r) ÷ (v − v_s)",
  "form": "equation",
  "variables": [
    {
      "name": "emitted frequency f",
      "quantity": "frequency (physical)",
      "carries_distance": false
    },
    {
      "name": "wave speed v",
      "quantity": "wave speed",
      "carries_distance": false
    },
    {
      "name": "receiver speed v_r",
      "quantity": "velocity",
      "carries_distance": false
    },
    {
      "name": "source speed v_s",
      "quantity": "velocity",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### waves.fresnel_partial_reflection
```yaml
{
  "id": "waves.fresnel_partial_reflection",
  "title": "Fresnel partial reflection and transmission",
  "statement": "At an interface between two media part of the light reflects and part transmits; the reflected fraction grows with the index contrast and the two fractions sum to one.",
  "formula": "R = ((n1 − n2) ÷ (n1 + n2))²",
  "form": "equation",
  "variables": [
    {
      "name": "reflected fraction R",
      "quantity": "probability",
      "carries_distance": false
    },
    {
      "name": "index contrast",
      "quantity": "index contrast",
      "carries_distance": false
    },
    {
      "name": "refractive index n",
      "quantity": "refractive index",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "getting through the boundary",
      "rises_with": [
        "index contrast"
      ],
      "falls_with": [],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {},
  "alternate_statements": []
}
```

### waves.group_velocity
```yaml
{
  "id": "waves.group_velocity",
  "title": "Group velocity",
  "statement": "The envelope of a wave packet travels at the group velocity, the derivative of angular frequency with respect to wavenumber; it is the speed at which energy and signal travel.",
  "formula": "v_g = dω ÷ dk",
  "form": "definition",
  "variables": [
    {
      "name": "group velocity v_g",
      "quantity": "group velocity",
      "carries_distance": false
    },
    {
      "name": "angular frequency ω",
      "quantity": "frequency (physical)",
      "carries_distance": false
    },
    {
      "name": "wavenumber k",
      "quantity": "wavenumber",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### waves.phase_velocity
```yaml
{
  "id": "waves.phase_velocity",
  "title": "Phase and phase velocity",
  "statement": "A wave's phase advances by one cycle per wavelength; the phase velocity is wavelength times frequency, or angular frequency over wavenumber.",
  "formula": "v_p = ω ÷ k",
  "form": "definition",
  "variables": [
    {
      "name": "phase velocity v_p",
      "quantity": "phase velocity",
      "carries_distance": false
    },
    {
      "name": "angular frequency ω",
      "quantity": "frequency (physical)",
      "carries_distance": false
    },
    {
      "name": "wavenumber k",
      "quantity": "wavenumber",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### waves.snell_refraction
```yaml
{
  "id": "waves.snell_refraction",
  "title": "Refraction (Snell's law)",
  "statement": "Crossing into a medium with a different refractive index, a ray bends so that index times the sine of the angle is the same on both sides.",
  "formula": "n1 × sin θ1 = n2 × sin θ2",
  "form": "equation",
  "variables": [
    {
      "name": "refractive index n",
      "quantity": "refractive index",
      "carries_distance": false
    },
    {
      "name": "angle θ",
      "quantity": "angle",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### waves.standing_waves
```yaml
{
  "id": "waves.standing_waves",
  "title": "Standing waves",
  "statement": "Between two fixed ends only wavelengths that fit a whole number of half-waves into the length persist; the ends force nodes and the allowed modes are set by the separation.",
  "formula": "λ_n = 2 × L ÷ n",
  "form": "limit",
  "variables": [
    {
      "name": "wavelength λ",
      "quantity": "wavelength",
      "carries_distance": false
    },
    {
      "name": "length L between the ends",
      "quantity": "length",
      "carries_distance": true
    },
    {
      "name": "mode number n",
      "quantity": "quantum number",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "which vibrations can persist: only those that fit between the two ends",
      "rises_with": [],
      "falls_with": [],
      "separation_made_by_distance": true
    }
  ],
  "physical_terms": {},
  "alternate_statements": []
}
```

### waves.superposition
```yaml
{
  "id": "waves.superposition",
  "title": "Superposition",
  "statement": "In a linear medium the net displacement at any point is the sum of the displacements each wave would produce alone.",
  "formula": "y = y1 + y2",
  "form": "identity",
  "variables": [
    {
      "name": "amplitude",
      "quantity": "amplitude",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### waves.total_internal_reflection
```yaml
{
  "id": "waves.total_internal_reflection",
  "title": "Total internal reflection",
  "statement": "Going from a higher to a lower index, beyond the critical angle no light crosses the boundary; all of it is reflected, while an evanescent field reaches past the surface without carrying energy across.",
  "formula": "sin θ_c = n2 ÷ n1",
  "form": "limit",
  "variables": [
    {
      "name": "critical angle θ_c",
      "quantity": "angle",
      "carries_distance": false
    },
    {
      "name": "refractive index n",
      "quantity": "refractive index",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "crossing the boundary; impossible past the critical angle, sooner the larger the index contrast",
      "rises_with": [
        "refractive index"
      ],
      "falls_with": [],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {},
  "alternate_statements": []
}
```

### waves.interference_cancellation
```yaml
{
  "id": "waves.interference_cancellation",
  "title": "Destructive interference at a point",
  "statement": "Two waves in opposite phase cancel at a point; the cancellation is located, and energy is conserved overall.",
  "formula": "",
  "form": "equation",
  "variables": [
    {
      "name": "phase difference",
      "quantity": "phase",
      "carries_distance": false
    },
    {
      "name": "location of the point",
      "quantity": "length",
      "carries_distance": true
    },
    {
      "name": "amplitude",
      "quantity": "amplitude",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "two vibrations coexisting at one location",
      "rises_with": [],
      "falls_with": [],
      "separation_made_by_distance": true
    }
  ],
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

Return a JSON ARRAY with one such object per relation, in the order given, and nothing else in the file. Write it to the file `runner/results/run1/raw/<MODEL>/batch-D.json` and then reply with the single word DONE. Do not read any other file, do not search the web, do not look at the repository.