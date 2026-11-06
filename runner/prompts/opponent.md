ROLE: opponent

You are the opponent in a test of a reflection rule. Below are the rule, a frozen vocabulary, one physics relation, and the reading that a majority of independent generators produced for it. Your task: produce the STRONGEST reading in which the shape is the other way (keeps instead of turns around, or the reverse), using the same rule and only the frozen vocabulary.

You win only if your alternative is rule-compliant: it must name an equivalence (to keep) or a resistance-caused cost or distance-made separation actually present in the physics statement (to turn), without inventing physics, without new words, and without rewriting the formula. If no rule-compliant alternative exists, say so; that is the honest result and it is what the test needs.

Use only this prompt. If you know anything else about TSR, set it aside and say so in `knew_tsr`.

## The rule

{rule}

## Which quantities carry resistance (fixed before this run)

{resistance_rules}

## The frozen vocabulary

{vocab_table}

## The relation

{relation}

## The majority reading

{majority}

## Report

Return ONE JSON object:

```json
{{
  "id": "{record_id}",
  "alternative_shape": "keeps | turns around | null",
  "rule_compliant": false,
  "argument": "the equivalence, cost or separation you rest on, in one or two sentences, or why none exists",
  "reflected_sentence": "your alternative sentence in frozen words, or empty",
  "knew_tsr": false
}}
```
