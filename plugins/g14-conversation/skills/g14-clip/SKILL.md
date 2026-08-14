---
name: g14-clip
description: 'Response transformer: shortens the answer to the essential, leading with the conclusion and cutting preamble, hedging and repetition. If the invocation carries input, answer that input directly in clipped mode; if invoked bare, rewrite the previous response. Trigger on: "/g14-clip", "shorten this", "get to the point", "TLDR this", "acórtalo", "ve al grano", "resúmelo al máximo".'
---

# g14-clip — Cut to the point

## Target resolution (shared logic)

1. If the invocation includes input (a question or text after the skill name), produce the answer to that input and deliver it already transformed.
2. If there is no input, take your own most recent response in this conversation and rewrite it transformed. Output only the rewritten version — no preamble about what you are doing.
3. If there is no input AND no previous response of yours, ask the user what to transform.

## Transformation rules

- First sentence = the answer or conclusion. Everything else supports it or gets cut.
- Cut entirely: preambles, restating the question, hedging ("it depends, but…"), caveats that don't change the action, transitions, closing summaries, offers of follow-up.
- Collapse repetition: if something is said twice, keep the better instance.
- Merge structure: sections that survive become at most a short bullet list; a single point becomes plain prose.
- Target roughly one third of the original length, or less. If the whole answer fits in 2–3 sentences, deliver just that.

## Invariants

- Never cut: the actual answer, facts and numbers the user needs, commands/code required to act, a warning about a destructive or irreversible action.
- Clipping changes selection and density, not correctness — do not simplify the technical level (that is g14-explain / g14-eli5's job).
- Output language matches the conversation language.
