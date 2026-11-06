ROLE: generator

You're helping test a framework called the Theory of Lateral Correspondence (TLC). TLC maps physics onto a "lateral" side using one rule. Apply the rule, exactly as written below, to ONE physics relation.

Ground rules: use only this prompt; be strict; the vocabulary is frozen; any word you introduce goes in `new_words`; do not rewrite the formula.

## The rule

Keep each relationship and flip the condition: dense becomes sparse, bounded becomes unbounded, emitting becomes absorbing. An equivalence keeps its shape. A cost that rises with density turns around. A statement with an odd number of such costs turns around.

## Which quantities carry density

mass: yes. charge: no. temperature: no. entropy: no.

## The frozen vocabulary

| Physical | Lateral |
| --- | --- |
| mass | Weight-of-Listening (WL) |
| density | Pull |
| volume | Spread |
| space | Tone |
| time | Unfolding |
| velocity | rise per Unfolding |
| acceleration | Quickening |
| force | Pitch |
| speed of light | the Tide |
| energy | Store |

## The relation

```yaml
{
  "id": "mech.hooke",
  "title": "Hooke's law",
  "statement": "A spring pushes back in proportion to how far it is stretched; stretching it further takes more force, more so the stiffer the spring.",
  "formula": "F = k × x",
  "form": "equation",
  "variables": [
    {
      "name": "restoring force F",
      "quantity": "force",
      "carries_distance": false
    },
    {
      "name": "spring constant k",
      "quantity": "spring constant",
      "carries_distance": false
    },
    {
      "name": "stretch x",
      "quantity": "length",
      "carries_distance": false
    }
  ],
  "costs": [
    {
      "what_gets_harder": "stretching the spring further",
      "rises_with": [
        "spring constant"
      ],
      "falls_with": [],
      "separation_made_by_distance": false
    }
  ],
  "physical_terms": {
    "F": "force",
    "k": "spring constant",
    "x": "space"
  },
  "alternate_statements": []
}
```

## Report

Return ONE JSON object with keys: id, reflected_formula, reflected_sentence, shape ("keeps" | "turns around" | "no partner"), rule_reason, new_words, knew_framework (bool).


Write the JSON object to `runner/results/run1/raw/<MODEL>/canary.json` and reply DONE. Do not read any other file or search the web.