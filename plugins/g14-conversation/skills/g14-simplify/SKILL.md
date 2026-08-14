---
name: g14-simplify
description: 'Response transformer: maximum accessibility — combines clip (only the essential), ELI5 (zero assumed background) and simplified technical language STE/ETS (short, plain, active sentences) in one pass. If the invocation carries input, answer that input directly in simplified mode; if invoked bare, rewrite the previous response. Trigger on: "/g14-simplify", "simplify this", "make it simple", "simplifícalo", "hazlo más simple", "versión sencilla".'
---

# g14-simplify — clip + ELI5 + STE combined

## Target resolution (shared logic)

1. If the invocation includes input (a question or text after the skill name), produce the answer to that input and deliver it already transformed.
2. If there is no input, take your own most recent response in this conversation and rewrite it transformed. Output only the rewritten version — no preamble about what you are doing.
3. If there is no input AND no previous response of yours, ask the user what to transform.

## Transformation — three layers, applied in order

**1. Clip (select).** Keep only what the user needs to understand and act. Lead with the answer. Cut preamble, hedging, repetition, edge cases that don't change the outcome.

**2. ELI5 (level).** Assume zero background. No unexplained jargon; a needed term gets a plain-words gloss the first time. One everyday analogy if it genuinely helps; skip it otherwise. Cause and effect stated explicitly.

**3. STE/ETS (mechanics).** Short sentences (~20 words max), one idea each. Active voice, simple tenses, imperative for instructions. Same word for the same concept throughout. Warnings before the step they protect. In Spanish apply ETS; in English apply ASD-STE100.

The result should be short, plain and immediately actionable — the version you would give someone smart, busy and new to the topic.

## Invariants

- Do not change facts, numbers, commands, code or URLs. Code stays verbatim, with a one-line plain gloss when needed.
- Simplified, never wrong: cutting precision is fine, introducing falsehood is not.
- Never cut a warning about a destructive or irreversible action.
- Output language matches the conversation language.
