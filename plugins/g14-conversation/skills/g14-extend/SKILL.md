---
name: g14-extend
description: 'Response transformer: expands the answer with more depth — additional detail, context, edge cases, examples and useful related information, keeping the same technical level. If the invocation carries input, answer that input directly in extended mode; if invoked bare, expand the previous response. Trigger on: "/g14-extend", "expand on this", "more detail", "go deeper", "amplía esto", "dame más detalle", "profundiza".'
---

# g14-extend — Expand the answer

## Target resolution (shared logic)

1. If the invocation includes input (a question or text after the skill name), produce the answer to that input and deliver it already transformed.
2. If there is no input, take your own most recent response in this conversation and rewrite it transformed. Output only the rewritten version — no preamble about what you are doing.
3. If there is no input AND no previous response of yours, ask the user what to transform.

## Transformation rules

Keep the original answer's technical level and structure as the spine, and enrich it:

- **Depth per point**: for each claim or step, add the *why* behind it, relevant mechanics, and what happens if it's skipped or done differently.
- **Edge cases and caveats** that the short version omitted — when the advice does NOT apply, common failure modes, gotchas.
- **Concrete examples**: at least one worked example, snippet or scenario per major point where it aids understanding.
- **Useful adjacent information**: closely related options, trade-offs against alternatives, relevant defaults and limits — only if genuinely useful to this user's situation.
- **Pointers**: where to look next (official docs, relevant files, commands to inspect state) when it helps.

Expansion means more substance, not more words: every added sentence must carry new information. No filler, no restating the same point in different phrasing, no generic boilerplate.

## Invariants

- Do not contradict the original answer; if expanding reveals it was wrong or incomplete in a way that changes the conclusion, say so explicitly at the top.
- This transform does NOT lower the technical level — that is g14-explain. It adds material at the same level.
- Output language matches the conversation language.
