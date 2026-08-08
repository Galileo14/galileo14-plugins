---
name: g14-visual-plan
description: 'Turns a feature/refactor/architecture plan into a reviewable, self-contained HTML visual plan saved locally in a .plans/ folder, styled with the Galileo14 design system (light theme, Geist + violet #3e38f2). Use it BEFORE implementing any non-trivial change — multi-file work, data-model or API decisions, UI flows, migrations, anything the user should approve before code is written. Triggers on: "visual plan", "plan visual", "make a plan I can review", "crea un plan visual", "haz el plan en HTML", "plan this feature", "planifica esto antes de tocar código", or when an existing text/Markdown plan needs a richer review surface. Not for trivial one-line fixes, and not a replacement for implementation — planning here is read-only.'
---

# g14-visual-plan — Local HTML Visual Plans

## What this does

Builds the plan you would normally write in chat Markdown as a scannable,
standalone HTML document — TL;DR, context, hard-to-reverse decisions, steps
with reuse-first framing, file map, risks, and open questions — saved to
`.plans/<yyyy-mm-dd>-<slug>.html` in the current working directory and branded
with the Galileo14 design system. The plan file is the review artifact and the
approval gate: the user reads it, comments, approves, and only then does
implementation start.

## When to use it

Whenever the plan is better as a reviewable artifact than a chat paragraph:
multi-file or ambiguous work, data-model/API/wire-format decisions, UI flows,
migrations, risky refactors, or an existing text plan the user wants to review
properly. Skip it for trivial, unambiguous changes whose diff fits in one
sentence — just make the change. This skill is local-first by design: no hosted
services, no MCP connectors; the deliverable is a file in the repo.

**Output language:** the plan's content matches the language the user is using
in the conversation. Default to English if unclear. The brand (wordmark,
footer, design system) stays Galileo14 regardless of language.

## Step 0 — Preflight

1. Confirm `${CLAUDE_PLUGIN_ROOT}/skills/g14-visual-plan/assets/plan-template.html`
   exists and is readable. If missing, stop and say so.
2. Check the design system is reachable:
   `curl -sf https://g14.link/design-system/index.json -o /dev/null`.
   If unreachable, do NOT block the plan — content beats branding. Continue,
   inline a minimal fallback `<style>` marked `/* fallback — design system
   unreachable */`, and report it in the handoff.

## Step 1 — Read the quality bar, then research (read-only)

Read `references/plan-quality.md` in full before drafting — it is the single
source of truth for plan discipline (gate thoughtfully, research first,
hard-to-reverse decisions, standalone writing, reuse-first steps, open
questions with defaults). Do not draft from memory.

Then research the codebase: read the real files, schema, and patterns the work
touches. Name actual files and symbols. For a large surface, delegate
exploration to one `Explore` subagent and keep only its conclusions. Make no
source edits — the only file this skill writes is the plan HTML. If a source
plan already exists (pasted, referenced, or in a file), gather its exact text
and treat it as source material for a clean standalone rewrite.

## Step 2 — Create the plan file from the template

1. Ensure the folder exists: `mkdir -p .plans` in the current working
   directory. (If the repo has a `.gitignore` and the user has not said plans
   should be committed, leave git handling to the user — do not edit
   `.gitignore` yourself.)
2. Copy `assets/plan-template.html` to `.plans/<yyyy-mm-dd>-<slug>.html`,
   where `<slug>` is a short kebab-case name for the work.
3. Fetch the stylesheet and inline it verbatim into the empty `<style>` block:
   `curl -s https://g14.link/design-system/galileo14.css`. Never edit its
   rules. Never use `/design-system/assets/design-system.css` (its font URLs
   are relative and break outside the site).
4. Fill every `{{SLOT}}` and repeat the marked repeatable blocks
   (`<!-- repeat ... -->`) as many times as the content needs. Do not change
   the structure, section order, classes, or scripts — the template IS the
   design; you only supply content. Status starts as `DRAFT` (tag variant
   `amber`); switch to `APPROVED` (variant `green`) only after user sign-off.
5. If the plan needs markup beyond the template (a table, a diff, a timeline,
   a schema), check the catalogue first —
   `https://g14.link/design-system/index.json`, then
   `https://g14.link/design-system/c/<component>.md` for exact markup
   (`g-table`, `g-diff`, `g-timeline`, `g-schema`, `g-code`...). 132
   components exist; assume what you need is one of them. Inline SVG diagrams
   use CSS variables for every color, never hex.

## Step 3 — Quality gate (before delivering)

For EACH criteria file in `tests/`, dispatch a SEPARATE general-purpose
subagent in fresh context, all in parallel — NEVER the agent that wrote the
plan grading its own work.

Dispatch config (mirror the grader's frontmatter — skill-nested agents are not
auto-registered): `model: sonnet`, `effort: high`, tools limited to
`Read, Glob, Grep`, `subagent_type: general-purpose`.

Inputs to pass in each prompt:
1. `criteria_path` — full path to the criteria file.
2. `output` — the path to the plan HTML under `.plans/`.
3. `skill_context` — "a standalone HTML visual plan for review before
   implementation".

Tell each subagent to follow `agents/grader.md` (the local vendored copy inside
this skill). Collect the JSON gradings. Fix every clear-cut failure (template
residue, invented paths, brand violations) and re-check; route genuine judgment
calls into the plan's Open Questions section. Never ship a failing item
silently.

## Step 4 — Hand off and iterate

1. Surface the plan: give the absolute path as inline code and a clickable
   `file://` link, and open it in the browser preview when available.
2. Ask the user to review and approve, naming the files/areas the work
   touches. This IS the approval question — do not ask a separate "does this
   look good?".
3. Feedback goes into the same file: edit the plan HTML in place, keep it
   standalone (no "changed since last draft" language), and re-run the quality
   gate after substantial edits. The document, not the chat, is the source of
   truth. On approval, flip the status tag to `APPROVED` and start
   implementation, re-reading the plan before major steps.

## Rules that do not bend

- Planning is read-only: no source-code edits until approval.
- One plan, one file, always under `.plans/` — never inline the plan as chat
  Markdown as the deliverable, and never scatter multiple drafts.
- The template's structure, tokens, and fonts are fixed; only content varies.
- Real files and symbols only — a plan that names invented paths is worse than
  no plan.
