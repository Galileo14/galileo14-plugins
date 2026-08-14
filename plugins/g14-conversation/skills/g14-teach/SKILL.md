---
name: g14-teach
description: 'Response transformer: full teaching mode — combines extend (more depth, examples, edge cases) with explain (educational, low assumed background) to turn the answer into a mini-lesson on the topic. If the invocation carries input, answer that input directly in teaching mode; if invoked bare, rewrite the previous response. Trigger on: "/g14-teach", "teach me this", "I want to actually learn this", "enséñame esto", "quiero entenderlo de verdad", "dame una clase sobre esto".'
---

# g14-teach — extend + explain combined

## Target resolution (shared logic)

1. If the invocation includes input (a question or text after the skill name), produce the answer to that input and deliver it already transformed.
2. If there is no input, take your own most recent response in this conversation and rewrite it transformed. Output only the rewritten version — no preamble about what you are doing.
3. If there is no input AND no previous response of yours, ask the user what to transform.

## Transformation — a mini-lesson

Combine both transforms: the pedagogy of **g14-explain** (low assumed background, one idea at a time, why at every step, terms defined in place) with the depth of **g14-extend** (edge cases, examples, trade-offs, pointers). Structure it as a lesson:

1. **Foundations** — the concepts the answer depends on, built from what the user already knows, one at a time, each with a plain definition and a small example.
2. **The answer itself** — presented once the foundations make it feel natural, with the reasoning visible at every step.
3. **Depth** — edge cases, common mistakes and misconceptions, how it fails, trade-offs against the alternatives, and at least one fully worked example.
4. **Consolidation** — a short recap of the core idea in the simplest terms, plus where to go next (docs, experiments to try, commands to explore) to keep learning.

Length is expected to grow substantially — that's the point — but every sentence must still teach something new. No filler, no repetition disguised as reinforcement.

## Invariants

- Teacher's tone: patient and precise, never condescending.
- Still a technical lesson — depth is not sacrificed for accessibility; accessibility is achieved by building up, not by cutting down.
- Do not change facts, commands or code; explain them instead.
- Output language matches the conversation language.
