# RISEN — Role · Instruction · Steps · End-goal/Examples · Narrowing/Nuance

Five-block framework for **structured, procedural tasks** where format strictness and step-by-step execution matter more than voice. Gained traction in 2024-2025 as the go-to structured alternative to RTF/CAR. Pairs naturally with COSTAR (RISEN for structure, COSTAR for voice).

The key insight: RISEN bakes **Steps** and **Examples** in as first-class blocks. CAR and COSTAR rely on the model to infer ordering and examples; RISEN forces you to spell them out, which kills drift on procedural tasks.

## Components

### [R] Role
Same as CAR/COSTAR. Specific > generic. One sentence.

Examples: "Senior tax accountant specialised in cross-border ecommerce" · "OCR-pipeline engineer who has shipped 5 production extractors for medical PDFs".

### [I] Instruction
The single high-level task in one sentence. Imperative verb up front. This is the *what*; Steps is the *how*.

Examples:
- "Extract every product mention from this transcript and classify each by sentiment."
- "Rewrite the README so a new contributor can run the project end-to-end in under 10 minutes."

If you need to chain two unrelated tasks, run the skill twice — don't pack two Instructions into one prompt.

### [S] Steps
The *ordered* procedure the model follows. Numbered list. Each step is one verb + one object. No nested sub-steps inside a step; if a step needs sub-steps, promote them to their own numbered step.

Example:
```
1. Read the transcript top to bottom and list every line where a product is named.
2. For each named product, capture: name (verbatim), surrounding sentence, speaker.
3. Classify each mention as positive / neutral / negative using only the surrounding sentence as evidence.
4. Group identical product names; sum the counts per sentiment.
5. Output the result.
```

Steps answer: _What is the procedure, step by step, in order?_

### [E] End-goal / Examples
This block does double duty in the canonical RISEN spec — pick the interpretation that fits:

- **End-goal** — the outcome that defines success. "A clean CSV that the analytics team can import without manual cleanup."
- **Examples** — concrete few-shot demonstrations of input → output. Use when the task shape is non-obvious or when format strictness is critical.

Use **both** when you can: state the end-goal *and* show 1-3 examples.

Few-shot format:
```
Example 1:
Input: "I love the new keyboard but the trackpad is mushy."
Output: { name: "keyboard", sentiment: "positive" }, { name: "trackpad", sentiment: "negative" }
```

### [N] Narrowing / Nuance
The constraints, edge cases, and exclusions. Negative space.

- **What to skip** — "Ignore mentions of competitor products."
- **Edge cases** — "If a product is mentioned without a sentiment cue, mark as `neutral`, not `unknown`."
- **Tone/length constraints** — "Output rows under 80 chars each."
- **Forbidden moves** — "Do NOT infer sentiment from context outside the surrounding sentence."

Narrowing answers: _What does the model need to NOT do, and what edge cases must it handle?_

## Use RISEN when

- The task has 3+ procedural steps that must run in a fixed order.
- Output format is strict (CSV, JSON, structured table) and a wrong shape breaks downstream.
- Examples genuinely help (classification, extraction, formatting, code generation).
- There are edge cases that need explicit handling.
- The work is repeatable: same prompt, different inputs, every week.

## Don't use RISEN when

- The task is one verb on one object → **CAR** is enough.
- The task is voice/brand-driven prose → **COSTAR**.
- The work is genuinely exploratory and you don't know the steps yet — RISEN locks in a procedure; if you haven't found one, don't pretend.

## Output template (literal — fill the slots, change nothing else)

```
# Role
{ONE_SENTENCE_SPECIFIC_ROLE}

# Instruction
{ONE_SENTENCE_HIGH_LEVEL_TASK}

# Steps
1. {STEP_1}
2. {STEP_2}
3. {STEP_3}
{ADD_MORE_AS_NEEDED}

# End-goal / Examples
End-goal: {WHAT_SUCCESS_LOOKS_LIKE}

Examples:
Input: {EXAMPLE_INPUT_1}
Output: {EXAMPLE_OUTPUT_1}

Input: {EXAMPLE_INPUT_2}
Output: {EXAMPLE_OUTPUT_2}

# Narrowing / Nuance
- {CONSTRAINT_OR_EDGE_CASE_1}
- {CONSTRAINT_OR_EDGE_CASE_2}
- {FORBIDDEN_MOVES_OR_EXCLUSIONS}
```

## Worked example

**Raw request:** "I need to extract product mentions from customer call transcripts and tag the sentiment"

**RISEN prompt:**

```
# Role
You are an NLP engineer who has shipped three production sentiment-extraction pipelines for B2B SaaS support transcripts.

# Instruction
Extract every product mention from the provided customer-call transcript and classify each mention's sentiment.

# Steps
1. Read the transcript top to bottom. List every line where a product is named (the company's own products only).
2. For each mention, capture: product name (verbatim from transcript), the full surrounding sentence, the speaker (customer or agent).
3. Classify each mention as `positive`, `neutral`, or `negative` using only the surrounding sentence as evidence.
4. Group identical product names; aggregate counts per sentiment.
5. Output the result as JSON.

# End-goal / Examples
End-goal: A JSON object the analytics team can ingest into the weekly NPS dashboard without manual cleanup.

Examples:
Input: "I love the new dashboard but the export feature is broken."
Output: [
  { "product": "dashboard", "sentiment": "positive", "speaker": "customer" },
  { "product": "export feature", "sentiment": "negative", "speaker": "customer" }
]

Input: "Yeah we use the API daily."
Output: [
  { "product": "API", "sentiment": "neutral", "speaker": "customer" }
]

# Narrowing / Nuance
- Ignore mentions of competitor products entirely.
- If a product is mentioned without a sentiment cue, mark as `neutral` — never `unknown`.
- Do NOT infer sentiment from context outside the surrounding sentence.
- Output one row per mention, even if the same product is mentioned multiple times.
- Final aggregate counts go in a `summary` key at the end of the JSON.
```

## Anti-patterns (don't do these)

- Steps that overlap or skip ordering ("1. Do X. 2. Also do Y.") — promote each verb to its own step.
- End-goal that restates the Instruction ("The goal is to extract product mentions") — say what *success* looks like instead.
- Skipping Narrowing because "there are no edge cases" — there always are. If you can't think of one, you haven't thought hard enough.
- Examples that are too generic ("Input: a sentence. Output: a result.") — use real, concrete pairs.
