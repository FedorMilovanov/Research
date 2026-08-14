# 1 Peter Bot — Learning Science and Item Analytics, Wave 2

**Status:** `PRODUCT-RESEARCH / NOT-YET-RUNTIME / FAIL-CLOSED`

## 0. Goal

The bot is not a digital stack of exam questions. Its purpose is to help a broad learner actually remember, understand, explain, and apply 1 Peter while keeping scholarship/source certainty visible.

The design therefore needs two different truth systems:

```text
CONTENT_TRUTH = evidence/source governance
LEARNING_TRUTH = measured learner performance
```

Neither substitutes for the other.

---

# 1. Retrieval before exposure

Where possible, ask the learner to retrieve before showing the explanation.

Useful forms:

- multiple choice;
- short answer / cloze;
- “which phrase belongs to this verse?”;
- OT-source matching;
- Greek lemma/form matching;
- explain-a-distinction prompt;
- confidence judgment before feedback.

Avoid turning every lesson into passive rereading.

---

# 2. Feedback

After an answer, feedback should usually include:

1. whether it was correct;
2. the correct answer;
3. one compact reason;
4. why the most tempting distractor is wrong;
5. optional “deeper” expansion;
6. source/evidence badge where useful.

A learner who selects a plausible but wrong interpretation should get a better explanation than someone who taps an absurd distractor.

---

# 3. Confidence calibration

Add a lightweight state such as:

```text
KNEW_IT
UNSURE
GUESSED
```

Use it diagnostically:

```text
correct + KNEW_IT = stronger mastery evidence
correct + GUESSED = retrieval success but weak mastery evidence
wrong + UNSURE = ordinary learning need
wrong + KNEW_IT = misconception priority
```

Never publicly shame confidence errors.

---

# 4. Spacing

The spacing literature does not support one universal magic interval. The useful gap depends partly on how long the learner should retain the material.

Therefore begin with a transparent heuristic and calibrate later.

Example product hypothesis, **not a scientific law**:

```text
NEW -> same session retrieval
SUCCESS_UNSURE -> 1 day
SUCCESS_KNOWN -> 3-4 days
ERROR -> later same session + next day
RELEARNED -> 3 days -> 10 days -> 30 days
MASTERED -> increasing interval with periodic cumulative retrieval
```

Run experiments before claiming superiority.

---

# 5. Successive relearning

A strong pattern for Bible learning is not merely “see card every N days,” but repeated successful retrieval across separated sessions.

Mastery should require something like:

```text
SUCCESSFUL_RETRIEVALS_ON_SEPARATE_DAYS >= threshold
AND
NO_RECENT_HIGH_CONFIDENCE_ERROR
AND
QUESTION_FORMS_NOT_ALL_IDENTICAL
```

A verse can be “known” in one wording but not transferable to a conceptual question; vary forms.

---

# 6. Item analytics

For each question after a meaningful sample size, collect at minimum:

```text
attempt_count
unique_user_count
correct_count
first_attempt_correct_count
median_response_ms
p90_response_ms
option_0_selected
option_1_selected
option_2_selected
option_3_selected
correct_position
confidence_known_count
confidence_unsure_count
confidence_guess_count
high_confidence_error_count
post_error_repeat_success_count
post_guess_repeat_success_count
```

Derived metrics:

```text
difficulty_p = correct_count / attempt_count
first_attempt_p
option_selection_rate[i]
nonfunctioning_distractor_candidate
confidence_accuracy_gap
repeat_recovery_rate
```

A later psychometric layer may add point-biserial/discrimination or an IRT model, but only when sample sizes and population assumptions justify it.

---

# 7. Distractor analytics

A distractor that almost nobody selects is often not doing useful diagnostic work.

Do not hard-code an eternal 5% rule as universal truth; use a configurable editorial threshold.

Example review trigger:

```text
attempt_count >= 200
AND distractor_selection_rate < 0.03
=> REVIEW_LOW_FUNCTIONING_DISTRACTOR
```

Other triggers:

```text
one wrong option dominates > 45% -> likely misconception or wording issue
correct option longest far more often than chance -> leakage review
one correct position overrepresented -> authoring leakage
response time extremely low + high accuracy -> possible giveaway
response time high + all distractors evenly selected -> ambiguity review
```

---

# 8. Correct-position hygiene

Current Chapter-3 hardening exposed a concrete product lesson: if options are not shuffled at runtime, canonical authoring data cannot put the correct answer first every time.

Repository/editorial guards should check:

- all positions represented;
- reasonable distribution;
- no long obvious sequences;
- correct option is not systematically longest/most precise;
- explanation does not leak exact answer phrase before user answers.

If runtime eventually shuffles options, canonical data should still remain editorially balanced because exports, previews, tests, static clients, and future bugs may expose source order.

---

# 9. Difficulty is not epistemic uncertainty

The bot needs separate fields:

```text
learner_difficulty = easy | standard | deep | research
content_confidence = high | medium | contested
```

Examples:

- a MorphGNT parsing fact can be `research` difficulty but `high` confidence;
- the identity of the spirits in 3:19 can be easy to state as a multiple-choice map but `contested` confidence;
- an application card can be simple while still noncompetitive/project-level.

Never let UI difficulty imply certainty.

---

# 10. Content balancing for adaptive delivery

A pure algorithm that always chooses the lowest predicted-success item can tunnel the learner into one topic.

The scheduler should maintain chapter/category quotas.

Possible content dimensions:

```text
chapter
verse_range
text
greek
OT_LXX
history
interpretation
disputed
application
project_theology
manuscripts
```

Example next-item score:

```text
need_score
+ forgetting_risk
+ misconception_priority
+ content_balance_bonus
+ due_spacing_bonus
- recent_repetition_penalty
```

Do not optimize only for short-term accuracy.

---

# 11. Explanations by learner level

Same source truth, different explanation depth.

### SIMPLE
One or two sentences, no unexplained Greek.

### STANDARD
Verse context + one key term/source relation.

### DEEP
Greek/LXX/syntax + interpretive alternatives.

### RESEARCH
Evidence status, source inspection level, textual variants, competing scholarship, unresolved HOLDs.

The answer key does not change between levels when the claim is factual. Only presentation depth changes.

---

# 12. Memory features specific to 1 Peter

## Verse-path memory

Build “journeys” through the argument:

- hope: 1:3 → 1:13 → 1:21 → 3:15;
- holiness: 1:15–16 → 2:5,9 → 3:15;
- suffering: 2:19–25 → 3:13–18 → 4:12–19 → 5:9–10;
- shepherding: 2:25 → 5:2–4;
- humility/submission: 2:13–3:7 → 5:5–6;
- Scripture reuse: Isa 40 → stone catena → Isa 53 → Ps 34 → Isa 8.

## Contrast cards

1 Peter is rich in contrasts:

```text
perishable / imperishable
former desires / holiness
malice/deceit / pure milk
rejected by people / chosen by God
evil-for-evil / blessing
fear of people / sanctifying Christ
flesh / spirit (interpretively disputed)
external washing / good-conscience clause
compulsion / willingness
shameful gain / eagerness
domineering / example
pride / humility
anxiety / God's care
resistible adversary / God who restores
```

Contrast-based retrieval may be more memorable than isolated trivia.

## Source-chain cards

Example:

> “1 Pet 2:6–8 combines which scriptural stone texts?”

Then deeper:

> “Which part is Isaiah 28, which is Psalm 118, and which is Isaiah 8?”

---

# 13. Disputed passages as learning opportunities

Do not hide disputes. Teach epistemic discipline.

A research-mode answer for 3:19 can show:

```text
WHAT_TEXT_SAYS
WHAT_GREEK_FORM_SAYS
WHAT_IT_DOES_NOT_SAY
READING_A
READING_B
READING_C
PROJECT_POSITION_IF_ANY
WHY_HOLD_REMAINS
```

This teaches learners how responsible interpretation works.

---

# 14. Ranking / competition

Competitive modes should use only sufficiently stable factual items.

Default exclusions:

- application;
- contested interpretations;
- project-position systematics;
- historical reconstruction with material uncertainty;
- manuscript questions before exact apparatus closure;
- newly launched items lacking editorial/analytics review.

Mastery points and competitive Elo should be distinct.

---

# 15. Experimental roadmap

### Experiment A — feedback depth
Compare compact feedback vs compact + “why tempting distractor is wrong.”

### Experiment B — confidence prompt
Measure whether `KNEW/UNSURE/GUESSED` improves repeat scheduling and misconception detection.

### Experiment C — successive relearning
Compare fixed review schedule vs successful-retrieval-on-separated-days requirement.

### Experiment D — 3 vs 4 options
Only after enough real selection data. If the fourth option is frequently nonfunctioning, test whether three high-quality options preserve discrimination with less authoring noise.

### Experiment E — mixed question forms
Compare identical-stem repeats with concept transfer across text/Greek/context formats.

No experiment should silently change doctrinal/source standards.

---

# 16. Privacy / analytics restraint

Collect learning telemetry needed to improve the course, not unrelated profiling.

Prefer aggregated item statistics and learner-local mastery state where possible.

Never infer sensitive beliefs beyond what the learning feature actually requires.

---

# 17. Research grounding

Wave-2 design is informed by:

- retrieval-practice/testing-effect literature;
- spacing-effect meta-analysis showing interaction between spacing gap and desired retention interval;
- successive relearning research;
- metacognitive calibration research;
- computer-adaptive testing / IRT literature;
- multiple-choice distractor-quality studies.

These literatures justify directions and experiments, not a claim that one scheduling formula is universally optimal.

---

# 18. Product acceptance gates

Before a new bank becomes “reviewed”:

```text
SOURCE_RESOLUTION = pass
CANONICAL_METADATA = pass
OPTION_UNIQUENESS = pass
ANSWER_POSITION_BIAS = pass
ANSWER_LENGTH_LEAKAGE = pass
DUPLICATE_NEAR_DUPLICATE = pass
CLAIM_CONFIDENCE = reviewed
RANKING_BOUNDARY = reviewed
EXPLANATION_LEVEL = reviewed
```

After launch:

```text
ITEM_ANALYTICS_SAMPLE = sufficient
DISTRACTOR_FUNCTION = reviewed
AMBIGUITY_REPORTS = reviewed
HIGH_CONFIDENCE_ERROR_RATE = reviewed
RETENTION_RETEST = reviewed
```
