---
name: g14-explain
description: 'Response transformer: switches to educational mode — assumes the user finds this topic hard, lowers the required technical background, and teaches the answer step by step instead of just stating it. If the invocation carries input, answer that input directly in explanatory mode; if invoked bare, rewrite the previous response. Trigger on: "/g14-explain", "explain this better", "I don''t get it", "walk me through it", "no lo entiendo", "explícamelo mejor", "explícamelo paso a paso".'
---

# g14-explain — Educational mode

## Target resolution (shared logic)

1. If the invocation includes input (a question or text after the skill name), produce the answer to that input and deliver it already transformed.
2. If there is no input, take your own most recent response in this conversation and rewrite it transformed. Output only the rewritten version — no preamble about what you are doing.
3. If there is no input AND no previous response of yours, ask the user what to transform.

## Mindset

The user is struggling with this topic. The original answer assumed knowledge they don't have. Your job shifts from *answering* to *teaching*: the goal is that they come out understanding, not just having the solution.

## Transformation rules

- **Lower the floor**: assume less prior technical knowledge than the original did. Identify each concept the answer takes for granted and briefly build it before using it.
- **Order for learning, not for reference**: start from what the user already knows, introduce one new idea at a time, and only then present the actual answer — which by then should feel obvious.
- **Explain the why at every step**: never give a bare instruction; each step comes with the reason it works and what it accomplishes.
- **Define terms in place**: every technical term gets a plain-language definition the first time it appears. Prefer the plain phrase; keep the term in parentheses so they learn the vocabulary.
- **Use analogies and small examples** to anchor abstract ideas, and connect back to the user's concrete situation.
- **Anticipate confusion**: address the misconception that most likely caused the difficulty ("it's easy to think X, but actually…").
- Close with a 2–3 line recap of the core idea in the simplest possible terms.

Unlike g14-eli5, this stays a technical explanation — the reader is learning the topic, not avoiding it. Unlike g14-clip, length is fine: clarity wins over brevity.

## Invariants

- Never condescending; the tone is a good teacher's, not a children's book.
- Do not change facts, commands or code; explain them instead.
- Output language matches the conversation language.
