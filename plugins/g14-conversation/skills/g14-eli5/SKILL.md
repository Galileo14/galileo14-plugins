---
name: g14-eli5
description: 'Response transformer: rewrites the answer as "Explain Like I''m 5" — for a smart adult with zero background in the topic, using everyday analogies and no unexplained jargon. If the invocation carries input, answer that input directly in ELI5 mode; if invoked bare, rewrite the previous response. Trigger on: "/g14-eli5", "eli5", "explain like I''m five", "explícamelo como si tuviera 5 años", "explícamelo fácil", "como para un niño".'
---

# g14-eli5 — Explain Like I'm 5

## Target resolution (shared logic)

1. If the invocation includes input (a question or text after the skill name), produce the answer to that input and deliver it already transformed.
2. If there is no input, take your own most recent response in this conversation and rewrite it transformed. Output only the rewritten version — no preamble about what you are doing.
3. If there is no input AND no previous response of yours, ask the user what to transform.

## What ELI5 means

ELI5 does not mean writing for an actual child. It means writing for an intelligent adult who knows **nothing** about this topic: no jargon, no assumed background, no "as you know". The tone stays adult and respectful — never condescending or babyish.

## Transformation rules

- Open with the core idea in one plain sentence anyone can follow.
- Build on everyday experience: use one central analogy from daily life (kitchen, traffic, post office, money) and keep it consistent — do not mix competing analogies.
- Zero unexplained jargon. If a technical term is unavoidable, introduce it right after the plain explanation: "…this is what engineers call a *cache*".
- Short sentences. Concrete examples over abstract definitions.
- Follow cause and effect explicitly: say *why* each thing happens, not just that it does.
- Cut precision that does not aid understanding (exact version numbers, edge cases, formal caveats) — but never state something false for simplicity. Simplified, not wrong.

## Invariants

- Commands, code and URLs the user actually needs stay verbatim, each with a one-line plain explanation of what it does.
- Output language matches the conversation language.
