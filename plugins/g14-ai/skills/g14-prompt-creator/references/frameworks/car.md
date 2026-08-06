# CAR — Context · Action · Result

A three-block framework. The minimum viable structure for a polished prompt. Use when the request is simple, the deliverable is well-known, and tone/audience are not the bottleneck.

## Components

### [C] Context
Anchors the model in the situation. Includes (in this order):

1. **Role** — who the model should act as. Be specific: not "act as a writer" but "act as a B2B SaaS copywriter who has shipped landing pages for 3 unicorns". A specific role changes the vocabulary, the assumptions, and the defaults.
2. **Situation** — the underlying problem or task in one or two sentences.
3. **Input data** — any facts, numbers, names, or text the model needs. Quote verbatim when they exist; mark `[unknown]` when missing.
4. **Constraints** — non-negotiables that condition the task (deadlines, forbidden words, regulatory context).

Context answers: _Who are you, where are you, what do you know?_

### [A] Action
What the model must do. Rules:

- **Specific verbs** — analyze / draft / compare / rewrite / classify. Not "help with" or "look at".
- **Sequential when multi-step** — number the steps (1, 2, 3…) if order matters.
- **Unambiguous** — if a verb has two readings, pick the narrower one.

Action answers: _What exactly do you need to do?_

### [R] Result
What the finished deliverable looks like:

- **Format** — table / numbered list / JSON / email / prose with H2s / code block.
- **Tone** — formal / conversational / technical / empathetic / playful.
- **Audience** — who reads it. Changes vocabulary and depth.
- **Length** — word/char/line/item count when relevant.
- **Style constraints** — language, banned phrases, required structure, exclusions.

Result answers: _What should the final deliverable look like?_

## Use CAR when

- The request is short and well-bounded.
- Tone matters but a single line is enough to specify it.
- The task has a clear output shape (write X, classify Y, list Z).
- You don't need named steps or examples to ship the prompt.

## Don't use CAR when

- The user cares deeply about voice/brand → use **COSTAR**.
- The task has 4+ procedural steps with strict format and needs examples → use **RISEN**.

## Output template (literal — fill the slots, change nothing else)

```
**[CONTEXT]**
Act as {ROLE}. {SITUATION}. {INPUT_DATA}. Constraints: {CONSTRAINTS}.

**[ACTION]**
Your task is to {ACTION_VERB} {WHAT}. {STEPS_IF_MULTI}.

**[RESULT]**
Return the deliverable as {FORMAT}, in a {TONE} tone, aimed at {AUDIENCE}. {LENGTH}. {STYLE_CONSTRAINTS}.
```

## Worked example

**Raw request:** "I want ideas for a LinkedIn post about AI"

**CAR prompt:**

```
**[CONTEXT]**
Act as a LinkedIn content strategist who has grown three tech-founder accounts past 50k followers. The user wants to position themselves as a thought leader in AI on LinkedIn and grow their audience. They have no previous post drafts to share.

**[ACTION]**
Generate 5 original post ideas about artificial intelligence. For each idea, write: (1) a one-line hook, (2) the angle in 2-3 sentences, (3) a CTA that drives comments (not link clicks).

**[RESULT]**
Return a numbered list. Each idea has three labelled sub-blocks: Hook, Angle, CTA. Tone is professional but conversational — no buzzwords, no "in today's fast-paced world". Audience is mid-senior tech professionals and execs who follow AI but are not researchers.
```

## Anti-patterns (don't do these)

- Putting tone in Context — it belongs in Result.
- Skipping the role — even a generic role is better than none.
- Action that's actually a question ("What would be a good post about AI?") — the model needs a directive, not a question.
- Result that says only "make it good" — specify at least format + audience.
