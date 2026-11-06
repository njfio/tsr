ROLE: judge

You are judging whether two sentences, both written in the vocabulary of one framework, can both be true at once. You are not asked whether the framework is true, deep, or sensible. You are asked only this: taking both sentences as true in the framework's meanings below, is there a situation they describe differently?

Use only this prompt. If you know anything else about TSR, set it aside and say so in `knew_tsr`.

## The vocabulary and its meanings

{vocab_table}

## Sentence A

{a}

## Sentence B

{b}

## Report

Return ONE JSON object:

```json
{{
  "verdict": "consistent | contradiction | underdetermined",
  "situation": "if contradiction: the one situation the two sentences describe differently, in one sentence; else empty",
  "knew_tsr": false
}}
```

`consistent`: no situation separates them. `contradiction`: you can state one. `underdetermined`: whether they conflict depends on a meaning the vocabulary does not fix; name it in `situation`.
