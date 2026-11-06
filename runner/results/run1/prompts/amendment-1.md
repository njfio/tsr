# Amendment 1 to the generator prompt (sent to every generator session, all models, all batches)

Clarification of one field. Nothing else changes.

`shape` is the call the rule makes about the RELATIONSHIP: `keeps` or `turns around`, decided from the record's form and cost block exactly as the rule states, whether or not every physical term has a partner in the frozen vocabulary. Physical terms with no partner go in `unmapped_terms`; they do not change the shape. Use `no partner` only when the reflection cannot be stated at all without introducing a NEW word (one not in the frozen vocabulary), and list that word in `new_words`.

So a definition with unmapped terms is `keeps` with those terms in `unmapped_terms`; a resistance-caused cost with unmapped terms is `turns around` with those terms in `unmapped_terms`. The `reflected_sentence` should state the keeps-or-turns reading in frozen words, describing any unmapped quantity in plain words rather than naming it.

Rewrite your answer file under this reading, keeping everything else as you had it, then reply DONE.
