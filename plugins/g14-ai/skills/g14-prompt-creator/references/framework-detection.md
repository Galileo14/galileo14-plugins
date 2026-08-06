# Framework detection — parse the user's input

Before asking the user which framework to use, scan their message for explicit indicators. If you find one, **skip the question**.

## Detection rules — apply in order

### Rule 1 — Explicit framework name
If the message contains any of these tokens (case-insensitive, word-boundary match), pick the matching framework and skip the question:

| Token in input                                          | Framework |
| ------------------------------------------------------- | --------- |
| `car`, `CAR framework`, `with CAR`, `apply CAR`, `marco CAR`, `usa CAR` | CAR       |
| `costar`, `co-star`, `CO-STAR`, `COSTAR framework`      | COSTAR    |
| `risen`, `RISEN framework`, `apply RISEN`               | RISEN     |

Watch out for false positives:
- The English word "car" (vehicle) — only match when preceded by "framework", "format", "use", "apply", "with", "in", "marco", "usa", or when capitalised as "CAR" with no surrounding lowercase letters.
- The English word "risen" (past participle of rise) — only match when used as a standalone token or with "framework", "format", "use", "apply".

When in doubt → ask the user. False detection costs more than asking.

### Rule 2 — Strong intent signals (still skip the question)
Even without an exact framework name, these signal a clear framework choice:

| Signal in input                                       | Pick      |
| ----------------------------------------------------- | --------- |
| "structured prompt", "step by step", "for extraction", "for classification", "with examples", "few-shot" | RISEN     |
| "for our brand", "tone matters", "for marketing", "customer-facing copy", "voice", "audience", "rewrite for X audience" | COSTAR    |
| "quick prompt", "simple prompt", "basic prompt", "just turn this into a prompt" | CAR       |

### Rule 3 — Default behaviour when nothing detected
If neither rule matched, **ask the user**. One short question, three options:

```
Which framework should I use for this prompt?

- CAR (Context · Action · Result) — lightweight, fastest. Good for simple, well-bounded prompts.
- COSTAR (Context · Objective · Style · Tone · Audience · Response) — best when voice, tone and audience matter (brand, copy, customer-facing).
- RISEN (Role · Instruction · Steps · End-goal/Examples · Narrowing) — best for structured procedural tasks with strict format and edge cases.
```

Use the AskUserQuestion tool when available; otherwise ask in plain text.

## Language detection

Separately, detect the **output language** the generated prompt should be in:

- If the user's message contains the phrase "in {language}" / "en {idioma}" / "auf {sprache}" → use that language.
- Otherwise → match the language of the user's most recent message in this conversation.
- Default to English if unclear.

The generated prompt's slots (role, action, tone, etc.) are filled in that language. The framework component *labels* (`[CONTEXT]`, `# Role`, `# Objective`) stay in English regardless — they're structural, not content.

## Edge cases

- **User says "use the best framework"** → don't pick silently. Reply briefly: "For your task I'd recommend X because Y — shall I proceed with X?". One-line answer, then proceed on yes.
- **User specifies two frameworks** ("apply CAR and COSTAR") → tell them this skill produces one prompt per run, ask which one to do first. Don't try to merge frameworks.
- **User says "no framework, just clean it up"** → this skill is framework-only. Tell them and ask if they want CAR (the most minimal) or to skip the skill.
- **User pastes an existing prompt and says "improve this"** → still detect framework using the rules above. If undetectable, ask.
