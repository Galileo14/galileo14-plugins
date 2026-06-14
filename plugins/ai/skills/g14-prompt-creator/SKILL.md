---
name: g14-prompt-creator
description: 'Prompt-engineering expert that transforms any user request into a polished, framework-structured prompt ready to paste into any LLM. Supports three frameworks: CAR (Context-Action-Result, lightweight), COSTAR (Context-Objective-Style-Tone-Audience-Response, for tone/voice/brand work) and RISEN (Role-Instruction-Steps-End-goal/Examples-Narrowing, for structured procedural tasks). Asks the user which framework to use unless the input already specifies one ("use CAR", "apply COSTAR", "with RISEN", "in CAR format"). Use whenever the user asks to: "make me a prompt for X", "improve this prompt", "optimize this prompt", "turn this idea into a prompt", "rewrite this prompt", "structure this prompt", "with CAR/COSTAR/RISEN", "apply prompt engineering", "make a professional/high-performance prompt". Do not use to execute the resulting prompt — only to generate it.'
---

# g14-prompt-creator — CAR · COSTAR · RISEN

Turn a raw user request into a polished, framework-structured prompt. One framework per run. Output language matches the user's conversation language (default English when unclear); framework block labels stay English regardless.

## Frameworks supported

- **CAR** — Context · Action · Result. Lightweight, fastest. For simple, well-bounded prompts where tone is not the bottleneck.
- **COSTAR** — Context · Objective · Style · Tone · Audience · Response. For brand/voice/audience-driven work (copy, comms, customer-facing).
- **RISEN** — Role · Instruction · Steps · End-goal/Examples · Narrowing. For structured procedural tasks with strict format and edge cases.

The authoritative spec for each framework lives in `${CLAUDE_PLUGIN_ROOT}/skills/g14-prompt-creator/references/frameworks/{car|costar|risen}.md`. These are the contracts; if your output disagrees with the spec, the spec wins.

## Pipeline (4 steps)

### Step 1 — Parse the input

Read the user's message. Extract:

- `raw_request` — the actual prompt-worthy content (strip framework mentions and meta-instructions).
- `framework_hint` — any explicit framework signal (see detection rules).
- `target_language` — the language the generated prompt should be in.

Apply the detection rules in `${CLAUDE_PLUGIN_ROOT}/skills/g14-prompt-creator/references/framework-detection.md`. Follow them verbatim — they handle false-positive traps ("car" the vehicle, "risen" the past participle, etc.) and edge cases (two frameworks specified, vague "best framework" request, etc.).

### Step 2 — Pick the framework

- If detection returned a framework with high confidence → use it. **Do not ask.** Acknowledge in one short line ("Using COSTAR for this.") and continue.
- If detection returned nothing → **ask the user once.** Use AskUserQuestion if available, otherwise plain text. Question template is in the detection reference. Three options: CAR, COSTAR, RISEN — each with the one-line "use when…" tagline.
- Edge cases (two frameworks, "best", "none") — handle exactly as the detection reference prescribes. Do not invent new behaviour.

### Step 3 — Dispatch to the framework applier subagent

Spawn ONE `general-purpose` subagent with `model: sonnet` (prompt craft is judgement work — Sonnet is the right tier; Haiku underperforms here, Opus is overkill).

- `description`: `Apply {FRAMEWORK} framework` (e.g. `Apply COSTAR framework`)
- `prompt`:

```
You are the {FRAMEWORK} prompt-engineering subagent.

STEP 1 — Read your instruction file in full:
   Read({CLAUDE_PLUGIN_ROOT}/skills/g14-prompt-creator/agents/{framework}-applier.md)

It tells you exactly what to do, what to read next, the JSON return contract, and the quality bar. Follow it literally.

STEP 2 — Apply the framework to this raw request:
"""
{RAW_REQUEST}
"""

STEP 3 — Output language for the generated prompt: {TARGET_LANGUAGE}
(Block labels stay in English; content inside blocks goes in {TARGET_LANGUAGE}.)

Return ONLY the JSON object specified in your instruction file. Nothing else.
```

Substitute `{FRAMEWORK}` with `CAR` / `COSTAR` / `RISEN`, `{framework}` with the lowercased name, `{RAW_REQUEST}` with the verbatim raw_request from Step 1, `{TARGET_LANGUAGE}` with the detected output language.

Wait for the subagent to return. Parse its JSON. If parsing fails or the contract is violated (missing keys, wrong shape), retry once with a clarifying line ("Your previous reply was not valid JSON matching the contract — return ONLY the JSON object, no surrounding prose."). If it still fails after one retry, present the raw output to the user and flag the contract violation — don't silently fix it.

### Step 4 — Render using the output template

Read `${CLAUDE_PLUGIN_ROOT}/skills/g14-prompt-creator/assets/output-template.md`. Fill every `{{SLOT}}` from the subagent's JSON:

| Slot                  | Source                                                                   |
| --------------------- | ------------------------------------------------------------------------ |
| `{{FRAMEWORK_NAME}}`  | `framework` field                                                         |
| `{{FRAMEWORK_TAGLINE}}` | `tagline` field                                                         |
| `{{POLISHED_PROMPT}}` | `prompt` field, verbatim                                                  |
| `{{COMPONENT_ROWS}}`  | One markdown table row per `components` entry: `\| {block} \| {content} \|` |
| `{{NOTES_ONE_LINE_OR_NONE}}` | `notes` field if non-null, else the literal word `None`            |

Strip the HTML comment header from the template before rendering.

Output the rendered template **verbatim**. No preamble ("Here's your prompt:"). No commentary after. The rendered template *is* the entire response.

## Hard rules

- **Never mix frameworks.** One framework per run. Even if the user says "apply CAR and also a bit of COSTAR".
- **Never invent a fourth framework.** Only CAR, COSTAR, RISEN. If the user asks for RTF, CRISPE, RACE, etc., tell them this skill supports those three and ask which to substitute.
- **Never skip the subagent.** Don't try to apply a framework in the main thread — the subagent is the determinism boundary. Each run goes through the dedicated applier.
- **Never reorder or rename framework blocks.** The block labels (`[CONTEXT]`, `# Objective`, etc.) are part of the contract. Don't translate them, don't shuffle them.
- **Output language** = detected target language. Block labels stay in English.
- **The output template is the entire response.** No preamble, no postscript.

## Repository layout (for reference)

```
g14-prompt-creator/
├── SKILL.md                                 (this file — orchestrator)
├── references/
│   ├── framework-detection.md               (parsing & question rules)
│   └── frameworks/
│       ├── car.md                           (CAR spec — authoritative)
│       ├── costar.md                        (COSTAR spec — authoritative)
│       └── risen.md                         (RISEN spec — authoritative)
├── agents/
│   ├── car-applier.md                       (CAR subagent instructions)
│   ├── costar-applier.md                    (COSTAR subagent instructions)
│   └── risen-applier.md                     (RISEN subagent instructions)
└── assets/
    └── output-template.md                   (canonical rendered shape)
```

_Skill location: `${CLAUDE_PLUGIN_ROOT}/skills/g14-prompt-creator/`_
