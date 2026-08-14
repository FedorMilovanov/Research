# Bot Learning Architecture — 1 Peter

## Goal

The bot should be serious enough that an advanced user can go deep, but simple enough that a new reader learns Scripture rather than learns to fear a wall of academic jargon.

The architecture should expose **depth on demand**.

## 1. Four learner layers

### Simple

Question types:
- who/what/why in the immediate text;
- sequence of the argument;
- one memorable phrase;
- one-sentence explanation.

No unnecessary Greek.

### Standard

Add:
- paragraph context;
- why one distractor is wrong;
- OT quotation/background;
- one key word where it changes understanding.

### Deep

Add:
- morphology vs semantics;
- syntax;
- LXX comparison;
- historical/social background;
- explicit disputed maps;
- manuscript/textual-critical observations.

### Research

Add:
- compare two commentaries;
- apparatus literacy;
- source inspection status;
- why a claim remains HOLD;
- distinguish project position from neutral evidence.

The same verse can produce cards at several layers without duplicating the same proposition.

## 2. Mastery model

Do not make one perfect quiz score equal mastery.

Recommended state per concept:

```text
UNSEEN
SEEN
RECALLED_ONCE
RECALLED_SPACED
MASTERED
NEEDS_REVIEW
CONTESTED_AWARENESS
```

Promote mastery through repeated successful retrieval across time, not clicks.

## 3. Spaced retrieval

Research base supports:

- retrieval practice;
- distributed/spaced practice;
- successive relearning;
- feedback after multiple choice.

Practical scheduling can begin simple rather than pretending to have a psychometric model:

```text
new -> same session short retry if wrong
correct but unsure -> 1 day
correct with confidence -> 3 days
second spaced success -> 7 days
third spaced success -> 21 days
later maintenance -> 45–90 days
```

Intervals should be tunable from real bot data.

## 4. Confidence calibration

After selected questions:

- `Знал`
- `Сомневался`
- `Угадал`

Use confidence to route review:
- wrong + confident = misconception priority;
- right + guessed = not mastered;
- right + confident across spaced sessions = mastery candidate.

Do **not** convert confidence to competitive points.

## 5. Feedback design

After answering, show compactly:

1. correct/incorrect;
2. one-sentence reason;
3. verse anchor;
4. optional `Почему остальные ответы неверны`;
5. optional `Глубже`;
6. optional `Источники`.

For disputed items:
- `Что установлено`;
- `Где начинается спор`;
- `Позиция курса`;
- `Другие серьёзные чтения`.

This teaches epistemic literacy without dumping a seminary footnote on every beginner.

## 6. Question formats

Use a mix:

- multiple choice;
- true/false only for genuinely binary facts;
- short free recall;
- "put the argument in order";
- match Greek form to parsing;
- match OT text to Petrine use;
- choose which statement is text vs interpretation;
- manuscript/apparatus literacy at advanced level;
- scenario/application cards, always noncompetitive.

## 7. Distractor standard

Wrong options should be:
- plausible;
- same semantic category;
- comparable length;
- traceable to a real confusion.

Never:
- absurd filler;
- three caricatures against one nuanced answer;
- theology vs morphology as competing answer types;
- morally grotesque options that reveal the answer.

## 8. Ranking boundary

Competitive pools may contain only propositions with strong objective answerability.

Default noncompetitive:
- applications;
- disputed exegesis;
- project-systematic conclusions;
- historical reconstructions;
- sophisticated Greek claims not yet independently source-reviewed.

Learning mastery and competitive ranking are separate systems.

## 9. Memory features worth building

- verse anchors and key-phrase recall;
- "your weak verses" review deck;
- Greek forms deck;
- OT/LXX connections deck;
- suffering/hope thematic deck;
- disputed-passages awareness deck;
- 5-minute daily spaced review;
- "explain it simply" summary after a deep unit;
- chapter map showing mastery by pericope/domain, not just % correct;
- resurfacing low-confidence correct answers;
- end-of-week mixed retrieval across chapters.

## 10. Analytics

Track learning-specific metrics separately from points:

- first-attempt accuracy;
- delayed-recall accuracy;
- confidence calibration;
- misconception recurrence;
- time-to-mastery;
- retention after 7/21/45 days;
- performance by domain: text / Greek / OT / history / interpretation.

Do not optimize the bot merely for session length or question volume.

## 11. Learning-science source direction

This wave includes Roediger/Karpicke, Cepeda, Dunlosky, Karpicke/Blunt, Yang et al., Butler/Roediger and successive-relearning work. Their collective use supports retrieval, spacing, feedback, and repeated recall. It does not prove one exact interval schedule for this bot; the actual schedule remains a product hypothesis to validate.
