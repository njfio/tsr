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

- Boltzmann constant: does not carry resistance — a constant
- current (electric): does not carry resistance — a flow
- efficiency: does not carry resistance — a ratio
- electrical resistance: carries resistance — defined as opposition to current (V / I)
- enthalpy: does not carry resistance — energy
- entropy: does not carry resistance — a count of microstates / a state function; not defined as opposition. Decided under R before thermodynamics ran.
- free energy: does not carry resistance — energy
- heat: does not carry resistance — energy in transit
- heat capacity: UNDETERMINED (a judgment call; say so) — defined as heat per unit temperature change; physics sometimes calls it thermal inertia (clause a) and sometimes a plain ratio (no clause). R does not decide it.
- internal energy: does not carry resistance — energy
- latent heat: does not carry resistance — energy per unit mass; its rise with mass is relation-level
- mass m: carries resistance — inertial mass is defined as opposition to a change in motion
- power: does not carry resistance — a rate of energy
- pressure: does not carry resistance — force per area; the book places it at the crossing, not as a resistance quantity
- temperature: does not carry resistance — mean kinetic energy per degree of freedom (or dS/dU inverse); not defined as opposition to change. Decided under R before thermodynamics ran.
- thermal resistance: carries resistance — defined as opposition to heat flow (L / kA)
- velocity: does not carry resistance — a rate, not an opposition
- volume: does not carry resistance — extent
- work: does not carry resistance — energy transferred

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

### thermo.carnot_limit
```yaml
{
  "id": "thermo.carnot_limit",
  "title": "Carnot limit",
  "statement": "No heat engine between two reservoirs can be more efficient than a reversible one; the limit is one minus the ratio of the cold to the hot temperature.",
  "formula": "η ≤ 1 − T_c ÷ T_h",
  "form": "inequality",
  "variables": [
    {
      "name": "efficiency η",
      "quantity": "efficiency",
      "carries_distance": false
    },
    {
      "name": "cold temperature T_c",
      "quantity": "temperature",
      "carries_distance": false
    },
    {
      "name": "hot temperature T_h",
      "quantity": "temperature",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "extracting work; the cap tightens as the two temperatures approach each other",
      "rises_with": [
        "temperature"
      ],
      "falls_with": [],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {},
  "alternate_statements": []
}
```

### thermo.enthalpy
```yaml
{
  "id": "thermo.enthalpy",
  "title": "Enthalpy",
  "statement": "Enthalpy is internal energy plus pressure times volume; at constant pressure the heat absorbed equals the change in enthalpy.",
  "formula": "H = U + P × V",
  "form": "definition",
  "variables": [
    {
      "name": "enthalpy H",
      "quantity": "enthalpy",
      "carries_distance": false
    },
    {
      "name": "internal energy U",
      "quantity": "internal energy",
      "carries_distance": false
    },
    {
      "name": "pressure P",
      "quantity": "pressure",
      "carries_distance": false
    },
    {
      "name": "volume V",
      "quantity": "volume",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### thermo.first_law
```yaml
{
  "id": "thermo.first_law",
  "title": "First law",
  "statement": "The change in a system's internal energy equals the heat added minus the work it does: energy is conserved.",
  "formula": "ΔU = Q − W",
  "form": "conservation",
  "variables": [
    {
      "name": "internal energy U",
      "quantity": "internal energy",
      "carries_distance": false
    },
    {
      "name": "heat Q",
      "quantity": "heat",
      "carries_distance": false
    },
    {
      "name": "work W",
      "quantity": "work",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### thermo.fourier_conduction
```yaml
{
  "id": "thermo.fourier_conduction",
  "title": "Heat conduction (Fourier) and thermal resistance",
  "statement": "The heat flowing through a slab for a given temperature difference falls as the slab's thermal resistance (thickness over conductivity times area) rises.",
  "formula": "q = ΔT ÷ R_th",
  "form": "equation",
  "variables": [
    {
      "name": "heat flow q",
      "quantity": "heat",
      "carries_distance": false
    },
    {
      "name": "temperature difference ΔT",
      "quantity": "temperature",
      "carries_distance": false
    },
    {
      "name": "thermal resistance R_th",
      "quantity": "thermal resistance",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "heat getting through for a given temperature difference",
      "rises_with": [
        "thermal resistance"
      ],
      "falls_with": [],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {},
  "alternate_statements": []
}
```

### thermo.free_energy
```yaml
{
  "id": "thermo.free_energy",
  "title": "Free energy",
  "statement": "Gibbs free energy is enthalpy minus temperature times entropy; at fixed temperature and pressure a process is spontaneous when it lowers the free energy.",
  "formula": "G = H − T × S",
  "form": "definition",
  "variables": [
    {
      "name": "free energy G",
      "quantity": "free energy",
      "carries_distance": false
    },
    {
      "name": "enthalpy H",
      "quantity": "enthalpy",
      "carries_distance": false
    },
    {
      "name": "temperature T",
      "quantity": "temperature",
      "carries_distance": false
    },
    {
      "name": "entropy S",
      "quantity": "entropy",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### thermo.heat_capacity_cost
```yaml
{
  "id": "thermo.heat_capacity_cost",
  "title": "Heat capacity (the cost reading)",
  "statement": "Warming a body by a given amount takes more heat the larger its heat capacity: thermal inertia.",
  "formula": "Q = C × ΔT",
  "form": "equation",
  "variables": [
    {
      "name": "heat capacity C",
      "quantity": "heat capacity",
      "carries_distance": false
    },
    {
      "name": "heat Q",
      "quantity": "heat",
      "carries_distance": false
    },
    {
      "name": "temperature change ΔT",
      "quantity": "temperature",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "warming the body by a given amount",
      "rises_with": [
        "heat capacity"
      ],
      "falls_with": [],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {},
  "alternate_statements": []
}
```

### thermo.heat_capacity_definition
```yaml
{
  "id": "thermo.heat_capacity_definition",
  "title": "Heat capacity (the definition)",
  "statement": "Heat capacity is the heat required per unit rise in temperature.",
  "formula": "C = Q ÷ ΔT",
  "form": "definition",
  "variables": [
    {
      "name": "heat capacity C",
      "quantity": "heat capacity",
      "carries_distance": false
    },
    {
      "name": "heat Q",
      "quantity": "heat",
      "carries_distance": false
    },
    {
      "name": "temperature change ΔT",
      "quantity": "temperature",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### thermo.joule_heating
```yaml
{
  "id": "thermo.joule_heating",
  "title": "Joule heating",
  "statement": "A current through a resistance dissipates power as heat in proportion to the resistance and the square of the current.",
  "formula": "P = I² × R",
  "form": "equation",
  "variables": [
    {
      "name": "power P",
      "quantity": "power",
      "carries_distance": false
    },
    {
      "name": "current I",
      "quantity": "current (electric)",
      "carries_distance": false
    },
    {
      "name": "resistance R",
      "quantity": "electrical resistance",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "carrying the current without loss; the energy lost to heat",
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

### thermo.latent_heat_cost
```yaml
{
  "id": "thermo.latent_heat_cost",
  "title": "Latent heat (the cost reading)",
  "statement": "Changing a body's phase takes heat in proportion to its mass, with no rise in temperature while it happens.",
  "formula": "Q = m × L",
  "form": "equation",
  "variables": [
    {
      "name": "latent heat L",
      "quantity": "latent heat",
      "carries_distance": false
    },
    {
      "name": "heat Q",
      "quantity": "heat",
      "carries_distance": false
    },
    {
      "name": "mass m",
      "quantity": "mass m",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "changing the body's phase; the heat it takes",
      "rises_with": [
        "mass m"
      ],
      "falls_with": [],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {},
  "alternate_statements": []
}
```

### thermo.latent_heat_definition
```yaml
{
  "id": "thermo.latent_heat_definition",
  "title": "Latent heat (the definition)",
  "statement": "Latent heat is the heat absorbed per unit mass in a phase change at constant temperature.",
  "formula": "L = Q ÷ m",
  "form": "definition",
  "variables": [
    {
      "name": "latent heat L",
      "quantity": "latent heat",
      "carries_distance": false
    },
    {
      "name": "heat Q",
      "quantity": "heat",
      "carries_distance": false
    },
    {
      "name": "mass m",
      "quantity": "mass m",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### thermo.second_law_clausius
```yaml
{
  "id": "thermo.second_law_clausius",
  "title": "Second law (Clausius)",
  "statement": "Heat does not spontaneously flow from a colder body to a hotter body; the entropy of an isolated system never decreases.",
  "formula": "ΔS_universe ≥ 0",
  "form": "inequality",
  "variables": [
    {
      "name": "entropy S",
      "quantity": "entropy",
      "carries_distance": false
    },
    {
      "name": "temperature T",
      "quantity": "temperature",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "undoing a spontaneous flow; getting the dispersed energy back as work",
      "rises_with": [
        "entropy"
      ],
      "falls_with": [],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {},
  "alternate_statements": [
    {
      "statement": "Kelvin-Planck: no cyclic process can convert heat entirely into work.",
      "form": "limit",
      "costs": [
        {
          "what_gets_harder": "turning all of the heat into work",
          "rises_with": [
            "heat"
          ],
          "falls_with": [],
          "separation_made_by_distance": false
        }
      ]
    }
  ]
}
```

### thermo.temperature_mean_kinetic_energy
```yaml
{
  "id": "thermo.temperature_mean_kinetic_energy",
  "title": "Temperature as mean kinetic energy",
  "statement": "In an ideal gas the average translational kinetic energy per molecule is three halves of k times the temperature: temperature measures mean molecular kinetic energy.",
  "formula": "½ × m × ⟨v²⟩ = 3/2 × k × T",
  "form": "identity",
  "variables": [
    {
      "name": "molecular mass m",
      "quantity": "mass m",
      "carries_distance": false
    },
    {
      "name": "mean square speed",
      "quantity": "velocity",
      "carries_distance": false
    },
    {
      "name": "temperature T",
      "quantity": "temperature",
      "carries_distance": false
    },
    {
      "name": "Boltzmann constant k",
      "quantity": "Boltzmann constant",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### thermo.thermal_equilibrium
```yaml
{
  "id": "thermo.thermal_equilibrium",
  "title": "Approach to thermal equilibrium",
  "statement": "Two bodies in thermal contact exchange heat from the hotter to the colder until they reach a common temperature.",
  "formula": "",
  "form": "equation",
  "variables": [
    {
      "name": "temperature T",
      "quantity": "temperature",
      "carries_distance": false
    },
    {
      "name": "heat Q",
      "quantity": "heat",
      "carries_distance": false
    }
  ],
  "costs": [],
  "physical_terms": {},
  "alternate_statements": []
}
```

### thermo.third_law
```yaml
{
  "id": "thermo.third_law",
  "title": "Third law",
  "statement": "As temperature approaches absolute zero the entropy approaches a constant, and absolute zero cannot be reached in a finite number of steps.",
  "formula": "lim T→0 S = S0",
  "form": "limit",
  "variables": [
    {
      "name": "entropy S",
      "quantity": "entropy",
      "carries_distance": false
    },
    {
      "name": "temperature T",
      "quantity": "temperature",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "reaching the zero of temperature; each step removes a smaller fraction",
      "rises_with": [
        "temperature"
      ],
      "falls_with": [],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {},
  "alternate_statements": []
}
```

### thermo.zeroth_law
```yaml
{
  "id": "thermo.zeroth_law",
  "title": "Zeroth law",
  "statement": "If two bodies are each in thermal equilibrium with a third, they are in thermal equilibrium with each other; this is what makes temperature a well-defined property.",
  "formula": "",
  "form": "definition",
  "variables": [
    {
      "name": "temperature T",
      "quantity": "temperature",
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

Return a JSON ARRAY with one such object per relation, in the order given, and nothing else in the file. Write it to the file `runner/results/run1/raw/<MODEL>/batch-B.json` and then reply with the single word DONE. Do not read any other file, do not search the web, do not look at the repository.