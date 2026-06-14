---
name: g14-skill-creator
description: 'Scaffolds a new Claude Code skill using the five-controls deterministic framework — turning a drifting one-file prompt into a near-deterministic system whose output stays consistent run to run. Use this whenever the user wants to build, design, or scaffold a skill and cares that it produce the SAME shape of result every time — phrases like "create a skill", "build a skill that doesn''t drift", "make a reliable/repeatable skill", "skill with consistent output", "apply the five controls", "deterministic skill", or describes a skill whose runs currently give inconsistent results. Prefer this over a generic skill draft whenever repeatability, trust, or controlled inputs/outputs matter.'
---

# g14-skill-creator — Deterministic Skill Scaffolder

## What this does

Helps the user build a new skill that produces the **same shape of output every
run** — same sources, same process, same layout, fast, and quality-checked.

A skill is a folder, not a markdown file. That folder lets you control five
distinct parts of a run. Every part you *don't* control is a decision Claude
re-makes — differently — on every run. That re-deciding is **drift**. This skill
walks the user from a plain drifting draft to a controlled system, adding only
the controls a real, observed failure justifies.

## The core principle

**Determinism is decided once, then replayed.** You don't pin Claude down by
writing a longer prompt — you pin it down by giving it an *artifact to follow*
instead of a *decision to make*. Each of the five controls replaces one decision
with one artifact.

**Only `SKILL.md` is structural.** When a skill runs, Claude loads exactly one
file: `SKILL.md`. It never auto-scans `references/`, `scripts/`, `assets/`,
`agents/`, or `tests/`. Those folders are *convention*. A folder does nothing
until `SKILL.md` explicitly tells Claude to read or run what's inside. So every
control below is two things: an **artifact** in a folder, and a **wiring
instruction** in `SKILL.md`. Build the artifact, then wire it up — a control
with no wiring is dead weight.

## The five controls

| # | Control | Folder        | Replaces the drift of…                                                |
|---|---------|---------------|-----------------------------------------------------------------------|
| 1 | Input   | `references/` | Claude picking its own sources/facts each run                         |
| 2 | Process | `scripts/`    | Claude reinventing the method each run                                |
| 3 | Output  | `assets/`     | Claude redesigning the deliverable each run                           |
| 4 | Speed   | `agents/`     | Slow serial runs; main context filling with noise                     |
| 5 | Tests   | `tests/`      | Output looks right but the *content* is wrong, stale or off-topic — checked by an LLM-as-judge subagent against a fixed rubric, in fresh context |

Controls 1–3 and 5 raise *determinism*. Control 4 raises *efficiency* — it
doesn't make output more repeatable, it makes runs fast and keeps the main
context clean, which indirectly protects accuracy.

Full build instructions for each control — folder layout, artifact examples,
and the exact `SKILL.md` wiring — are in **`${CLAUDE_PLUGIN_ROOT}/skills/g14-skill-creator/references/five-controls.md`**.
Read it before building any control.

## Language rule

**Output language:** the scaffolded `SKILL.md` frontmatter, body, and any
explanations match the language the user is using. Default to English if
unclear.

## Workflow

Work through these steps with the user. Don't skip the interview, and don't
front-load all five controls — see Step 3.

### Step 1 — Capture intent

Interview the user until you can answer all of these. Pull what you can from
the conversation already; only ask the gaps.

1. **What should the skill let Claude do?** One concrete sentence.
2. **When should it trigger?** Real phrases a user would type.
3. **What's the deliverable?** A file? A report? A code change? What format?
4. **Where does its information come from?** Named sources, an API, an MCP, the
   open web, the user's own files?
5. **Is the process fixed or open-ended?** Same steps every time, or genuinely
   novel each run?
6. **What would "wrong" look like?** This is the seed for the test rubrics in
   Control 5.

### Step 2 — Write the plain skill first (zero controls)

Write a single `SKILL.md` — frontmatter plus plain-language instructions. No
subfolders yet. This is deliberate: a skill that works fine as one file doesn't
need scaffolding, and you can't know which controls it needs until you've seen
it drift.

Use `${CLAUDE_PLUGIN_ROOT}/skills/g14-skill-creator/assets/skill-md-skeleton.md` as the
starting shape. Write a **pushy, specific `description`** — Claude tends to
*under*-trigger skills, so the description must say both what the skill does
and the concrete contexts and phrases that should invoke it.

### Step 3 — Diagnose the drift

Now decide which controls this skill actually needs. **Start at zero and add a
control only to fix a failure you can name.** Over-controlling a skill that
should stay flexible just makes it brittle.

Two ways to diagnose:

- **Reason it through** with the user against
  `${CLAUDE_PLUGIN_ROOT}/skills/g14-skill-creator/references/decision-table.md` —
  for each row, ask "does this failure apply to our skill?"
- **Run it a few times** (mentally or for real) and watch what changes between
  runs. Each observed inconsistency points at exactly one control.

Common outcomes:

- A skill that summarizes the user's *own* uploaded file needs **no input
  control** — the input is already pinned.
- A skill whose whole job is open-ended exploration should **skip the process
  control** — improvising is the point.
- A low-stakes skill a human reviews every run can **skip tests** — the human
  is the grader.

State explicitly which controls you're adding and which you're skipping, with
the reason. This list is the build plan for Step 4. Capture it like:

```
## Controls decision
- Control 1 (Input):   ADDED — sources from 3 named feeds
- Control 2 (Process): SKIPPED — task is novel each run
- Control 3 (Output):  ADDED — fixed HTML template
- Control 4 (Speed):   SKIPPED — sequential work
- Control 5 (Tests):   ADDED — claims must trace to sources
```

### Step 4 — Add the controls, one per observed failure

For each control in your plan, follow
`${CLAUDE_PLUGIN_ROOT}/skills/g14-skill-creator/references/five-controls.md`:

- **Control 1 — Input (`references/`).** Pin the sources/facts. One file per
  source or a whitelist; tell `SKILL.md` to use *only* those.
- **Control 2 — Process (`scripts/`).** Capture the method as code the skill
  *runs* instead of reasoning through. For tool/MCP steps that can't be
  scripted, name the exact tool and arguments in `SKILL.md`. Keep an escape
  hatch.
- **Control 3 — Output (`assets/`).** Hand Claude a literal template to fill,
  not a layout to invent. Lock structure; let only content vary.
- **Control 4 — Speed (`agents/`).** Fan independent work out to parallel
  subagents so the main context stays clean. Registration caveat in the
  reference — nested `agents/` files aren't auto-registered; either promote
  real agents to `.claude/agents/`, or have `SKILL.md` spawn a general-purpose
  subagent that reads the instruction file.
- **Control 5 — Tests (`tests/`).** Write one markdown rubric per concern
  (accuracy, freshness, tone, safety). Wire `SKILL.md` to dispatch a fresh
  general-purpose subagent per rubric *as a quality gate* before delivery —
  never let the same agent grade its own work. Point each subagent at the
  grader contract at `${CLAUDE_PLUGIN_ROOT}/skills/g14-skill-creator/agents/grader.md`
  and mirror its recommended dispatch config (`model: sonnet`, tools limited
  to `Read, Glob, Grep`).

### Step 5 — Wire everything into SKILL.md

Make `SKILL.md` the orchestrator. For every folder you created, add an
explicit instruction: read this, run that, dispatch these, fill that template,
grade against those rubrics. Verify nothing is orphaned — if a folder exists
but `SKILL.md` never mentions it, it will simply never be used.

Quick wiring reference:

| Control | One-line wiring pattern in the new skill's SKILL.md                                                |
|---------|----------------------------------------------------------------------------------------------------|
| 1       | "Read every file in references/sources/. Use ONLY these — do not fall back to open web."           |
| 2       | "Run: python scripts/<name>.py <args>. Improvise only if it fails, and report the failure."        |
| 3       | "Load assets/<template>. Fill every {{SLOT}}. Do not change the structure."                        |
| 4       | "Dispatch one general-purpose subagent per <unit-of-work>, all in parallel, model: haiku."         |
| 5       | "Before delivering output, dispatch a fresh grader subagent per file in tests/, in parallel — `model: sonnet`, follow `agents/grader.md`." |

### Step 6 — Verify and iterate

Re-read the finished `SKILL.md` as if you were Claude running it cold. Confirm:
the description triggers correctly, every control is wired, the escape hatches
exist, and the skill is no longer re-deciding anything it shouldn't.

Then drive it: pick 2-3 realistic prompts and run end-to-end. If Control 5
(Tests) is wired, every run produces grader output you can inspect to see
whether the rubric criteria hold. The grader's `evidence` field per item tells
you *why* something failed — usually where the skill needs sharpening.

## Judgement, in one line

The drift you actually observe tells you which control to add next. A skill
earns its scaffolding one observed failure at a time — never pre-emptively.
Tests (Control 5) turn quality from a feeling into a judgement against a
written rubric — add them when the cost of shipping wrong content is real.
