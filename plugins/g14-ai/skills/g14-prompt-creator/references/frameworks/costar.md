# COSTAR — Context · Objective · Style · Tone · Audience · Response

Six-block framework. Originated at GovTech Singapore (2024); winner of Singapore's first GPT-4 Prompt Engineering competition. Adopted by AWS and DataStax. **Use when voice and tone are the bottleneck** — brand content, customer-facing comms, copywriting where the *how* matters as much as the *what*.

The key insight: COSTAR splits "tone" into three independent dials — **Style** (sentence craft), **Tone** (emotional register), **Audience** (vocabulary level). CAR collapses these; COSTAR separates them so they can be tuned independently.

## Components

### [C] Context
The setup. Same as CAR's Context **minus the tonal hints** (those move to Style/Tone/Audience). Includes:

- The **role** the model adopts.
- The **business/personal situation** prompting the request.
- **Input data** — quoted verbatim where it exists.
- **Constraints** — deadlines, regulations, things to avoid.

Context answers: _What's the situation, and what does the model know about it?_

### [O] Objective
What you want to achieve — the *outcome*, not the action. This is the most-skipped block. The difference between "write a tweet about our launch" (action) and "convert launch-day visitors into newsletter subscribers" (objective) shapes everything downstream.

Objective answers: _Why is this prompt being run? What changes if it works?_

### [S] Style
How the prose is constructed. Sentence craft. Not emotion.

Examples:
- "Punchy two-sentence paragraphs. No subordinate clauses."
- "Long, flowing sentences in the style of long-form New Yorker essays."
- "Code-comment style: declarative, no adverbs, present tense."

Style answers: _How are the sentences built?_

### [T] Tone
The emotional register. Style is craft; Tone is *feeling*.

Examples: friendly · authoritative · playful · sober · urgent · understated · self-deprecating · academic · evangelical.

Tone answers: _What does it feel like to read?_

### [A] Audience
The reader's profile — what they know, what they don't, what they care about.

Examples:
- "C-level execs who don't read docs but skim slides."
- "Junior engineers learning Rust from a JavaScript background."
- "Existing customers on the highest tier — already convinced, looking for power features."

Audience answers: _Who reads it, and what do they bring to it?_

### [R] Response
The deliverable format. **Pure shape** — no tone words allowed here (they belong in Tone).

Examples: "JSON with keys `title`, `body`, `cta`" · "Markdown email under 150 words" · "Three-column table" · "Tweet thread of exactly 6 tweets, each ≤270 chars".

Response answers: _What's the literal shape that comes back?_

## Use COSTAR when

- Brand voice / tone matters and "professional" isn't enough.
- The output is customer-facing: copy, comms, announcements, support replies.
- The same content needs to be re-rendered for different audiences (Style/Tone/Audience can be tuned independently).
- The task has a clear desired *outcome* beyond just "produce X".

## Don't use COSTAR when

- The request is purely procedural with no voice concerns → use **CAR** (lighter) or **RISEN** (structured).
- You don't actually know the objective beyond "draft a thing" — COSTAR's six blocks become noise without a real Objective.

## Output template (literal — fill the slots, change nothing else)

```
# Context
{ROLE_AND_SITUATION_AND_INPUT_AND_CONSTRAINTS}

# Objective
{DESIRED_OUTCOME_NOT_ACTION}

# Style
{HOW_THE_PROSE_IS_CONSTRUCTED}

# Tone
{EMOTIONAL_REGISTER}

# Audience
{READER_PROFILE_WITH_DEPTH}

# Response
{LITERAL_FORMAT_AND_LENGTH}
```

## Worked example

**Raw request:** "Write a launch tweet for our new AI feature"

**COSTAR prompt:**

```
# Context
You are the social lead at a developer-tools company shipping its first AI feature (an inline code reviewer). You write the launch announcement on the company's main X account, which has ~40k followers, mostly senior backend engineers.

# Objective
Convert launch-day attention into trial signups. Success = clicks to the signup page, not retweets.

# Style
One opening line that lands a single specific claim. Then 2-3 lines of plain English. No bullet points. No emojis except one at the end. Sentences ≤14 words.

# Tone
Confident but not hyped. Speak like an engineer talking to engineers — quietly proud of the thing, no marketing varnish.

# Audience
Senior backend engineers (5+ YoE) who already use the product daily for non-AI tasks. They're sceptical of AI features and have seen 12 launches like this fail. They click only if they believe the demo.

# Response
Three tweets in a thread, each ≤270 characters. Tweet 1 = the hook + specific claim. Tweet 2 = one concrete code example. Tweet 3 = link to signup + one-line "free during launch week". No hashtags.
```

## Anti-patterns (don't do these)

- Mixing Style and Tone into one block — they're separate dials, that's the whole point.
- Putting "the AI should…" in Objective. Objective is about the user's outcome, not the model's behaviour.
- Audience as "everyone" or "general public" — that's not an audience, that's an absence.
- Response that says "good and short" — say `≤150 words, markdown email format`.
