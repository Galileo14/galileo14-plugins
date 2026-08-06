# Audit rubric: the five controls

This is the **source of truth** for judging a skill against the five-controls
framework. The auditor uses ONLY this rubric (plus `best-practices.md`) so the
verdict is the same shape every run. The framework itself comes from the sibling
skill g14-skill-creator. Grade against *this* file; the framework's own docs are
vendored next to it for deep rationale on borderline calls:
`${CLAUDE_PLUGIN_ROOT}/skills/g14-skill-audit/references/five-controls.md`
and `${CLAUDE_PLUGIN_ROOT}/skills/g14-skill-audit/references/decision-table.md`.

## The cardinal rule: a skipped control is not a defect

The framework's central principle: **a skill earns scaffolding one observed
failure at a time. Controls are added only when a real failure justifies them.**

Therefore the auditor must NEVER flag a missing control as a defect on its own.
A skill that correctly skips a control it doesn't need is *well-built*, not
broken. Over-controlling a skill that should stay flexible is itself a finding
(brittleness). The judgement is always two questions, never one:

1. **Is the control PRESENT and WIRED?** (folder exists, is non-empty, and
   `SKILL.md` actually references it; the scan reports this)
2. **Is the control NEEDED**, given what this skill does?

The two answers form a 4-quadrant verdict applied to every control:

| | NEEDED | NOT NEEDED |
|---|---|---|
| **PRESENT + WIRED** | ✅ Correct: grade *how well* it's done, propose improvements | ⚠️ Over-engineered: flag as a candidate to simplify or remove (brittleness) |
| **ABSENT (or unwired)** | ❌ **GAP**: the important finding; the skill drifts here | ✅ Correct decision: note as a healthy, deliberate skip |

"Present but NOT wired" (an orphan folder the scan flags) counts as ABSENT for
the verdict **and** is its own finding: dead weight that misleads readers.

## How to decide "is it NEEDED?" per control

Apply the decision-table triggers. Decide from what the skill actually does, not
from its description's ambition.

- **Control 1 (Input, `references/`):** NEEDED when the skill pulls facts or
  sources that could vary between runs, or from places that must be trusted or
  fixed (named feeds, an API, the open web, a fixed schema/style guide).
  NOT needed when the skill explores freely (open-ended research/discovery) or
  the input is already pinned (it processes the user's own uploaded file).
- **Control 2 (Process, `scripts/`):** NEEDED when the same task is solved a
  different way each run, or deterministic work (fetch/dedupe/rank/validate) is
  being re-reasoned in prose, burning tokens. NOT needed when the task is
  genuinely novel each run, or inputs are unstable and need live improvising.
  (Tool/MCP steps that can't be scripted count as "process pinned" if `SKILL.md`
  names the exact tool and arguments; see best-practices.)
- **Control 3 (Output, `assets/`):** NEEDED when the deliverable has a structure,
  layout or format that should be byte-stable run to run (report, HTML, CSV,
  fixed schema). NOT needed when the output is meant to adapt to each request.
- **Control 4 (Speed, `agents/`):** NEEDED when there is independent work that
  could run in parallel, or the main context fills with raw intermediate noise.
  NOT needed when the work is small, sequential, or each step depends on the
  previous. (This is an efficiency control, not a determinism control, so judge
  it on speed and context-cleanliness, not repeatability.)
- **Control 5 (Tests, `tests/`):** NEEDED when the output makes claims that
  could be wrong-but-plausible (facts traceable to sources, freshness, on-topic,
  tone, PII/safety) AND no human reviews every run. NOT needed when the output
  is mechanical with nothing to verify, or a human is the grader on every run.

When NEEDED is genuinely ambiguous, say so and recommend the cheap diagnostic:
run the plain skill a few times and watch what drifts (the decision-table's
"diagnosis loop"). Do not assert a gap you can't ground.

## How to grade a PRESENT + NEEDED control: "is it done WELL?"

Only once a control is present, wired, and needed do you grade quality:

- **Control 1 (Input).** One file per source (or a clear whitelist). Each source
  file carries how to use it (url, recency, what to skip, why trusted). `SKILL.md`
  says *use ONLY these, do not fall back to open web, record unreachable as
  skipped*. ❌ if it says "use these, and if one is down find a replacement",
  which defeats the closed world.
- **Control 2 (Process).** Method captured as code that's *run*, not prose that's
  reasoned. Exact commands in `SKILL.md`. An **escape hatch** exists ("if the
  script fails, improvise and report it"). ❌ if scripts exist but `SKILL.md`
  still describes the method in vague prose, or there's no escape hatch (brittle).
  ❌ **Scripts must be pre-written artifacts committed in `scripts/`, not
  generated at run time.** A skill that tells Claude to *write/create/generate a
  script on the fly* defeats the control: the logic is unreviewed, non-
  deterministic and re-authored every run. The script is the artifact built
  once; the run only *executes* it. (Scan flag `writes_scripts_on_the_fly`.)
- **Control 3 (Output).** A literal template with `{{SLOT}}`s in `assets/`.
  `SKILL.md` says *fill every slot, do not change structure/headings/classes*.
  Only content varies. ❌ if the "template" is really a description of a layout
  to invent each time.
  - **Output destination and naming must be deterministic too.** A fixed template
    is only half the control; check *where* the deliverable lands and *how it's
    named*. The skill should define a specific destination (a named folder, a
    database/table, and so on) and a specific, predictable file-naming convention
    (for example `reports/audit-<skill>-<date>.md`), not leave Claude to choose a
    path and filename each run. ❌ if the output location or filename is decided
    ad-hoc per run, or outputs are scattered with no convention; that is output
    drift even when the template is fixed. ✅ structured, repeatable storage (a
    consistent folder and naming scheme, or a defined DB write).
- **Control 4 (Speed).** Independent units fanned out to subagents *in parallel*
  ("all at once, do not run in sequence"). Workers return only clean results.
  Model matched to job (mechanical work → Haiku). Registration handled correctly
  (skill-nested `agents/` files are NOT auto-registered, so they are either
  promoted to `.claude/agents/` or dispatched as general-purpose subagents that
  read the instruction file, with model set at dispatch). ❌ if dispatch is
  sequential, or a frontier model does mechanical work, or a nested agent's
  frontmatter is assumed to auto-apply.
  - **Don't only grade the subagents that exist; hunt for missing subagent
    opportunities.** Read the workflow steps and look for any independent,
    repeated, or per-unit work that is currently done inline (or serially) and is
    not delegated to a subagent (scrape each source, fetch each page, process
    each record, summarise each file, run several independent analyses). Each
    such piece of work is a candidate to extract into a subagent dispatched in
    parallel: it speeds the run and keeps the orchestrator context clean. Flag the
    opportunity as a Control 4 finding whatever subagents already exist (having
    one subagent doesn't mean every parallelisable step is covered). Recommend the
    specific subagent to add and how to fan it out ("add a per-source subagent,
    one dispatch per source, all in parallel"). Scan hints:
    `summary.likely_missing_subagent_opportunity` (independent/repeated work
    described with no sign of parallel dispatch) and
    `signals.mentions_per_item_work`. These are hints only; confirm by reading the
    steps that the work is genuinely independent and not already delegated.
  - **Control 4 has nothing to fan out unless there is independent work.** It
    depends on Control 2 being parallelisable or the task naturally splitting
    into independent units. Do NOT flag Speed as a gap on a skill whose work is
    inherently sequential or tiny.
  - **Runtime and scaling: estimate it, don't guess.** Walk the workflow and
    estimate end-to-end wall-clock: how many serial steps, how many units of
    independent work, how long each. Call out any independent work done serially
    that should be parallel. The danger to name: a long run that only fails near
    the end (see preflight, below).
  - **Large or unbounded fan-out: recommend a dynamic Workflow.** Plain parallel
    subagent dispatch is right for a handful of units. When the fan-out is large
    or unbounded (say "one subagent per page" across a whole site, hundreds or
    thousands of units, per-record over a big dataset, or a loop-until-done),
    recommend a **dynamic workflow** (the Workflow tool: `pipeline()`/`parallel()`
    with its concurrency cap, batching, per-item isolation and resumability)
    instead of hand-dispatching N subagents from `SKILL.md`. Hand-dispatch at
    that scale overflows context, has no backpressure, and can't resume.
    (Scan flags `mentions_large_fanout`, `mentions_dynamic_workflow`.)
- **Control 5 (Tests).** One rubric per concern (not one mega-rubric). Graded by
  a **fresh** subagent (never the agent that produced the output). Each rubric
  has hard PASS criteria checkable against something external (source, date,
  banned list). Wired as a quality gate *before delivery*, run in parallel,
  `model: sonnet`, tools limited to `Read, Glob, Grep`. ❌ if the producer grades
  itself, rubrics are soft or subjective ("is it comprehensive?"), or grading is
  "as you go" instead of an independent final pass.

## Specific improvement triggers (call these out explicitly)

These are the high-value, concrete recommendations the user expects:

- **Cheaper/faster models for subagents.** If a dispatched worker does
  mechanical work (scrape, extract, fetch, transform) on `opus`/`sonnet`, or
  declares no model at all, recommend pinning it to `haiku` and reserving the
  strong model for the orchestrator's judgement. The scan lists
  `agents_missing_model`. Note: grading or judging subagents should stay on
  `sonnet`; don't recommend Haiku for graders.
- **More / better tests.** If correctness matters (claims, sources, freshness,
  tone, PII) and `tests/` is missing or thin, recommend specific rubrics. If a
  mega-rubric mixes concerns, recommend splitting into one-concern rubrics. If
  the producer grades itself, recommend a fresh-context grader.
- **Wiring integrity.** Any orphan folder (present but unreferenced): remove or
  wire it. Any referenced path that doesn't exist (the scan's
  `broken_referenced_paths`) is broken wiring; fix the reference.
- **Escape hatches.** A pinned process or input with no recovery path is brittle,
  so recommend adding one and reporting failures so the user can update the
  artifact.
- **Trigger strength.** A weak `description` makes the skill under-trigger (see
  best-practices). Recommend a pushier, phrase-rich description.
- **On-the-fly scripts.** If `SKILL.md` tells Claude to write/create/generate a
  script at run time (scan `writes_scripts_on_the_fly`), recommend moving that
  logic into a committed `scripts/` artifact the skill *runs*.
- **Runtime and parallelisation.** Estimate the run's wall-clock. Recommend
  parallelising independent serial work; for large or unbounded fan-outs
  recommend a dynamic Workflow (see Control 4 above).
- **Preflight check.** If the skill has many steps and no early dependency
  verification, recommend a fail-fast preflight as step 1 (see Preflight section).
- **Output destination.** If the template is fixed but the output path or
  filename is ad-hoc, recommend a deterministic destination and naming convention
  (or a defined DB write).
- **Intermediate state / checkpointing.** For a long skill (high `step_count`)
  with no state persistence, recommend writing progress after each step (e.g.
  `state.json`) so the run survives compaction and can resume from the failed
  step instead of restarting (see best-practices F).
- **Error handling.** If the skill assumes the happy path with no handling for
  tool or script failures, recommend the right mechanism per step: bounded retry
  (e.g. up to 3×), a fallback tool/process, or a hard stop-step that halts with a
  clear message when something can't be done (no access, hard error). See
  best-practices F.
- **`effort` matched to task.** If an agent does mechanical work at high effort
  or declares no effort, recommend `effort: low/medium`; if a judgement agent has
  no effort set, recommend `high`. Remember it must be set at dispatch for nested
  agents (scan `agents[].effort_declared`, `summary.agents_missing_effort`). See
  best-practices G.
- **Batching and context slicing.** For a fan-out of many tiny units, recommend
  batching B units per worker (and a dynamic Workflow when huge). If workers get
  the whole context, recommend passing only the relevant slice, and having them
  return only clean results. See best-practices G.
- **Model-tiering and high-frequency cost.** Flag defaulting to Opus; recommend
  Haiku→Sonnet→Opus by need. For a `/loop` or routine skill, recommend a cheap
  model/effort on the repeated path and a per-iteration cost note. See
  best-practices G.
- **Cache ordering, context discipline, memory reuse** [P3]. Flag large stable
  files re-read per item instead of once early (cache misses); for long runs
  recommend `/compact` discipline; for recurring skills recommend caching stable
  derived facts (lists, glossaries) in `references/`/CLAUDE.md/memory instead of
  re-deriving them. Scan `signals.mentions_compact`, `signals.mentions_memory_reuse`.
  See best-practices G.

## Preflight and fail-fast (cross-cutting, always check)

A skill with many steps must **verify up front that it has everything it needs**,
then abort early with a clear message if not. The failure to avoid: running a
long, expensive pipeline and only discovering at step 18 that a required tool,
MCP/connector, credential, input file or script is missing. By then time and
tokens are wasted and partial state may have been written.

Check that, **as an early step**, the skill confirms access to its hard
dependencies before doing real work:

- required tools / MCP connectors are available (named and checked, not assumed),
- credentials / API keys it depends on are present,
- required input files / source folders exist and are readable,
- its own scripts and templates exist (`broken_referenced_paths` from the scan
  is direct evidence they don't),

and that it **fails fast** (stops with an actionable message) when a
dependency is missing, rather than pressing on. (Scan flag
`mentions_preflight_check`; absence is a hint, not proof, so confirm by reading.)

- ✅ Step 1 verifies the connector/tool/inputs exist and aborts with a clear
  message if any is missing.
- ❌ A 10-step skill that calls an MCP only at step 9 with no earlier check:
  recommend adding a preflight dependency check as the first step. Severity P1
  when the skill is long or expensive or writes partial state before the failure
  point; P2 otherwise.

## Severity definitions (canonical, use everywhere)

These definitions are the single source of truth for P1/P2/P3 across the report,
the cross-cutting checklist and the test rubrics. When a `best-practices.md` item
carries its own bracketed severity (e.g. a secret leak is P1), **that item's
severity wins** even if it's "just a best-practice violation".

- **P1:** a NEEDED control is a genuine gap (absent or unwired); a run would
  break (broken wiring to a real path) or fail late for a missing dependency that
  a preflight would catch; a secret is exposed; output is fabricated or ungrounded.
- **P2:** a present control done weakly; a real best-practice violation
  (wrong or under-specified model, missing escape hatch, on-the-fly scripts,
  ad-hoc output destination, over-engineering); a missing parallelisation win.
- **P3:** polish, such as wording, leanness, minor naming, optional niceties.

## Scoring

Produce a band, not false precision:

- **Strong:** every NEEDED control present, wired, and well-built; skips are
  justified; no broken wiring; no over-engineering.
- **Adequate:** needed controls present but one or more done weakly, or minor
  wiring or model issues; no critical gap.
- **Weak:** at least one NEEDED control is a real GAP (absent or unwired), or
  multiple correctness failures, or broken wiring that would break a run.

Always pair the band with the count of P1 gaps, P2 correctness issues, and P3
polish items from the report.
