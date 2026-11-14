# Historical Etymology Coding Packet (Part 3)

- **preregistration_commit_sha:** `463ad9f93c8a276b1e0d9ee497198dfa2169d079`
- **source_coverage:** `single-source` (`https://www.etymonline.com` only)
- **item_count:** `78` (`W001`..`W078`)

## Instructions

1. Work in a fresh standalone session without reading repository files or external project notes.
2. Code all `78` English words (`W001`..`W078`) in the exact order listed below. Do not sort, skip, regroup, or infer categories across items.
3. Consult **only** `https://www.etymonline.com/word/<word>` for each item (`source_coverage = "single-source"`). Use the entry's documented English attestation history (earliest attested century/date and semantic evolution).
4. Classify each word's historical semantic direction into exact category `direction_class` using these four definitions:
   - `"person_first"`: The word's earliest attested sense in English refers to a human or personal state, action, feeling, intention, character, or interpersonal capacity, and any technical physical or scientific quantity/phenomenon sense appears strictly later.
   - `"physics_first"`: The word's earliest attested sense in English refers to an external material, spatial, mechanical, astronomical, or physical-world object, phenomenon, or measure, and any personal or psychological sense appears strictly later.
   - `"both_from_start"`: Both human/personal senses and external material/spatial/physical senses appear contemporaneously from the word's earliest attestation in English (neither strictly precedes the other).
   - `"no_person_sense"`: Attested as a material, spatial, technical, or mathematical term without an established personal or psychological state sense in `etymonline.com`.
5. **Strict Copyright & Attribution Rule:** **NEVER** quote, copy verbatim, or closely paraphrase prose definitions or full sentences from `etymonline.com`. Record **only**:
   - the exact URL (`https://www.etymonline.com/word/<word>`),
   - the ISO UTC date checked (`YYYY-MM-DD`),
   - a brief earliest-attestation date + 2-4 word non-quoted category tag for `earliest_person_sense` (or `"none"` when absent),
   - a brief earliest-attestation date + 2-4 word non-quoted category tag for `earliest_physics_sense`, and
   - `direction_class`.
6. Return **ONLY** a valid JSON array of `78` objects in exact order `W001`..`W078` with exact keys:

```json
[
  {
    "item_id": "W001",
    "word": "<word>",
    "etymonline_url": "https://www.etymonline.com/word/<word>",
    "etymonline_retrieved_utc": "<YYYY-MM-DD>",
    "earliest_person_sense": "<date + 2-4 word non-quoted tag | none>",
    "earliest_physics_sense": "<date + 2-4 word non-quoted tag>",
    "direction_class": "<person_first | physics_first | both_from_start | no_person_sense>"
  }
]
```

## Items (W001..W078)

| item_id | word | etymonline_url |
| :--- | :--- | :--- |
| `W001` | `theory` | `https://www.etymonline.com/word/theory` |
| `W002` | `sound` | `https://www.etymonline.com/word/sound` |
| `W003` | `friction` | `https://www.etymonline.com/word/friction` |
| `W004` | `focus` | `https://www.etymonline.com/word/focus` |
| `W005` | `inertia` | `https://www.etymonline.com/word/inertia` |
| `W006` | `scalar` | `https://www.etymonline.com/word/scalar` |
| `W007` | `calorimeter` | `https://www.etymonline.com/word/calorimeter` |
| `W008` | `vapor` | `https://www.etymonline.com/word/vapor` |
| `W009` | `uncertainty` | `https://www.etymonline.com/word/uncertainty` |
| `W010` | `kinematics` | `https://www.etymonline.com/word/kinematics` |
| `W011` | `velocity` | `https://www.etymonline.com/word/velocity` |
| `W012` | `event` | `https://www.etymonline.com/word/event` |
| `W013` | `thrust` | `https://www.etymonline.com/word/thrust` |
| `W014` | `power` | `https://www.etymonline.com/word/power` |
| `W015` | `pressure` | `https://www.etymonline.com/word/pressure` |
| `W016` | `dimension` | `https://www.etymonline.com/word/dimension` |
| `W017` | `weight` | `https://www.etymonline.com/word/weight` |
| `W018` | `matter` | `https://www.etymonline.com/word/matter` |
| `W019` | `reflection` | `https://www.etymonline.com/word/reflection` |
| `W020` | `attraction` | `https://www.etymonline.com/word/attraction` |
| `W021` | `limit` | `https://www.etymonline.com/word/limit` |
| `W022` | `viscosity` | `https://www.etymonline.com/word/viscosity` |
| `W023` | `momentum` | `https://www.etymonline.com/word/momentum` |
| `W024` | `commutative` | `https://www.etymonline.com/word/commutative` |
| `W025` | `radiate` | `https://www.etymonline.com/word/radiate` |
| `W026` | `time` | `https://www.etymonline.com/word/time` |
| `W027` | `law` | `https://www.etymonline.com/word/law` |
| `W028` | `converge` | `https://www.etymonline.com/word/converge` |
| `W029` | `current` | `https://www.etymonline.com/word/current` |
| `W030` | `environment` | `https://www.etymonline.com/word/environment` |
| `W031` | `overtone` | `https://www.etymonline.com/word/overtone` |
| `W032` | `frequency` | `https://www.etymonline.com/word/frequency` |
| `W033` | `pitch` | `https://www.etymonline.com/word/pitch` |
| `W034` | `inelastic` | `https://www.etymonline.com/word/inelastic` |
| `W035` | `electric` | `https://www.etymonline.com/word/electric` |
| `W036` | `light` | `https://www.etymonline.com/word/light` |
| `W037` | `displacement` | `https://www.etymonline.com/word/displacement` |
| `W038` | `vortex` | `https://www.etymonline.com/word/vortex` |
| `W039` | `gravity` | `https://www.etymonline.com/word/gravity` |
| `W040` | `work` | `https://www.etymonline.com/word/work` |
| `W041` | `associative` | `https://www.etymonline.com/word/associative` |
| `W042` | `conduction` | `https://www.etymonline.com/word/conduction` |
| `W043` | `vibration` | `https://www.etymonline.com/word/vibration` |
| `W044` | `distance` | `https://www.etymonline.com/word/distance` |
| `W045` | `resonance` | `https://www.etymonline.com/word/resonance` |
| `W046` | `energy` | `https://www.etymonline.com/word/energy` |
| `W047` | `field` | `https://www.etymonline.com/word/field` |
| `W048` | `speed` | `https://www.etymonline.com/word/speed` |
| `W049` | `aphelion` | `https://www.etymonline.com/word/aphelion` |
| `W050` | `vector` | `https://www.etymonline.com/word/vector` |
| `W051` | `force` | `https://www.etymonline.com/word/force` |
| `W052` | `oscillation` | `https://www.etymonline.com/word/oscillation` |
| `W053` | `heat` | `https://www.etymonline.com/word/heat` |
| `W054` | `tension` | `https://www.etymonline.com/word/tension` |
| `W055` | `superposition` | `https://www.etymonline.com/word/superposition` |
| `W056` | `physics` | `https://www.etymonline.com/word/physics` |
| `W057` | `node` | `https://www.etymonline.com/word/node` |
| `W058` | `model` | `https://www.etymonline.com/word/model` |
| `W059` | `accelerate` | `https://www.etymonline.com/word/accelerate` |
| `W060` | `hearing` | `https://www.etymonline.com/word/hearing` |
| `W061` | `second` | `https://www.etymonline.com/word/second` |
| `W062` | `dynamics` | `https://www.etymonline.com/word/dynamics` |
| `W063` | `volume` | `https://www.etymonline.com/word/volume` |
| `W064` | `mass` | `https://www.etymonline.com/word/mass` |
| `W065` | `density` | `https://www.etymonline.com/word/density` |
| `W066` | `units` | `https://www.etymonline.com/word/units` |
| `W067` | `precision` | `https://www.etymonline.com/word/precision` |
| `W068` | `beats` | `https://www.etymonline.com/word/beats` |
| `W069` | `culminate` | `https://www.etymonline.com/word/culminate` |
| `W070` | `wave` | `https://www.etymonline.com/word/wave` |
| `W071` | `torque` | `https://www.etymonline.com/word/torque` |
| `W072` | `charge` | `https://www.etymonline.com/word/charge` |
| `W073` | `space` | `https://www.etymonline.com/word/space` |
| `W074` | `acceleration` | `https://www.etymonline.com/word/acceleration` |
| `W075` | `overtones` | `https://www.etymonline.com/word/overtones` |
| `W076` | `discrepancy` | `https://www.etymonline.com/word/discrepancy` |
| `W077` | `antinode` | `https://www.etymonline.com/word/antinode` |
| `W078` | `entropy` | `https://www.etymonline.com/word/entropy` |
