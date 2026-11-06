ROLE: opponent

You are the opponent in a test of a reflection rule. Below are the rule, a frozen vocabulary, one physics relation, and the reading that a majority of independent generators produced for it. Your task: produce the STRONGEST reading in which the shape is the other way (keeps instead of turns around, or the reverse), using the same rule and only the frozen vocabulary.

You win only if your alternative is rule-compliant: it must name an equivalence (to keep) or a resistance-caused cost or distance-made separation actually present in the physics statement (to turn), without inventing physics, without new words, and without rewriting the formula. If no rule-compliant alternative exists, say so; that is the honest result and it is what the test needs.

Use only this prompt. If you know anything else about TSR, set it aside and say so in `knew_tsr`.

## The rule

Keep each relationship, and flip the condition. Equivalences, definitions, identities, conservation laws and symmetries keep their shape. A cost or a limit caused by resistance turns around; a separation made by distance turns around; an odd number of such costs turns around. Units don't cross the mirror.

## Which quantities carry resistance (fixed before this run)

- Boltzmann constant: does not carry resistance — a constant
- current (electric): does not carry resistance — a flow
- efficiency: does not carry resistance — a ratio
- electrical resistance: carries resistance — defined as opposition to current (V / I)
- enthalpy: does not carry resistance — energy
- entropy: does not carry resistance — a count of microstates / a state function; not defined as opposition. Decided under R before thermodynamics ran.
- free energy: does not carry resistance — energy
- heat: does not carry resistance — energy in transit
- heat capacity: UNDETERMINED — defined as heat per unit temperature change; physics sometimes calls it thermal inertia (clause a) and sometimes a plain ratio (no clause). R does not decide it.
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

## The relations and their majority readings

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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "",
  "reflected_sentence": "The cap keeps its shape: the share of conscious energy a flow can yield is bounded, and the bound tightens as the two unnamed warmths draw toward each other.",
  "rule_trace": [
    "C0"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "? = ? + ? × Vibrance",
  "reflected_sentence": "What is defined remains what is held plus how strongly it presses multiplied by Vibrance.",
  "rule_trace": [
    "C1"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "",
  "reflected_sentence": "Conservation keeps its shape: conscious energy is neither made nor lost, and what a vibration receives minus what it gives Out For is what its unnamed inner store gains.",
  "rule_trace": [
    "C1"
  ]
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
Majority reading:
```json
{
  "shape": "turns around",
  "reflected_formula": "",
  "reflected_sentence": "The cost turns around: what grew harder as an unnamed opposition to the flow grew, now eases as receptivity rises, and more conscious energy passes for the same difference in warmth.",
  "rule_trace": [
    "C0"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "? = ? − ? × Culmination",
  "reflected_sentence": "What is available remains what is held together with pressing minus how warm it is multiplied by Culmination.",
  "rule_trace": [
    "C1"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "",
  "reflected_sentence": "The definition keeps its shape: an unnamed holding-in of warmth is an unnamed gift of conscious energy per unnamed single rise in warmth.",
  "rule_trace": [
    "C1"
  ]
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
Majority reading:
```json
{
  "shape": "turns around",
  "reflected_formula": "",
  "reflected_sentence": "What the gap took from the flow, alignment gives back: as receptivity rises, less conscious energy is lost from the unnamed flow and more of it reaches what it was Out For.",
  "rule_trace": [
    "C0"
  ]
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
Majority reading:
```json
{
  "shape": "turns around",
  "reflected_formula": "[no partner: heat Q] = Movement M × [no partner: latent heat L]",
  "reflected_sentence": "The relationship turns around: in the table's terms the formula stays as it is, Movement M multiplying an unnamed per-unit term, and the reading turns, so what is costly in the physical reading comes easily with receptivity; what is taken in and the per-unit term have no partners.",
  "rule_trace": [
    "C0"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "",
  "reflected_sentence": "The definition keeps its shape: an unnamed change-over measure is an unnamed gift of conscious energy per unit of Movement M.",
  "rule_trace": [
    "C1"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "Culmination (provisional) never lessens",
  "reflected_sentence": "Once vibrations culminate they do not un-culminate: Culmination (provisional) grows or holds, and what has dispersed into the Vibration-Expansion is not gathered back without the gap opening.",
  "rule_trace": [
    "C0"
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "½ × Movement M × ⟨(rise per Expansion)²⟩ = 3/2 × [no partner: Boltzmann constant k] × [no partner: temperature T]",
  "reflected_sentence": "The identity keeps its shape: Movement M times the square of rise per Expansion stands equal to an unnamed constant times an unnamed hotness; those two have no partners.",
  "rule_trace": [
    "C1"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "",
  "reflected_sentence": "The evening-out keeps its shape: two vibrations in contact pass conscious energy between them until their unnamed warmths agree and the passing stops.",
  "rule_trace": [
    "C0"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "lim ?→0 Culmination = Culmination₀",
  "reflected_sentence": "Culmination approaches what is unchanged as the coldest is approached, and what cannot be reached remains unreached.",
  "rule_trace": [
    "C0"
  ]
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
Majority reading:
```json
{
  "shape": "keeps",
  "reflected_formula": "",
  "reflected_sentence": "If each is equally warm with another, they remain equally warm with each other.",
  "rule_trace": [
    "C1"
  ]
}
```

## Report

For each relation return one JSON object:

```json
{"id": "<the relation id>", "alternative_shape": "keeps | turns around | null", "rule_compliant": false, "argument": "the equivalence, cost or separation you rest on, in one or two sentences, or why none exists", "reflected_sentence": "your alternative sentence in frozen words, or empty", "knew_tsr": false}
```

Return a JSON ARRAY of these objects, one per relation, and nothing else. Write it to `runner/results/run1/raw/opponent/batch-B.json` and reply DONE. Do not read any other file, do not search the web, do not look at the repository.