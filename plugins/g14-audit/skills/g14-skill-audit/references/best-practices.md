# Best-practices checklist: cross-cutting

Beyond the five controls, a skill is graded against these checkable practices,
distilled from the Claude Code self-learning curriculum (lessons 04 to 12). Each
item is something the auditor can verify by reading files. Flag a violation only
when it actually applies to the skill under audit; many are conditional.

Group findings under these areas in the report's "Cross-cutting findings"
section. Severity guidance is in brackets.

## A. SKILL.md authoring and triggering

- **Description triggers reliably** [P1 if it would mis-trigger]. The
  `description` says BOTH what the skill does AND the concrete contexts/phrases
  that should invoke it. Claude under-triggers skills, so a vague description
  ("helps with news") is a real defect. Good: lists real user phrases, file
  types, adjacent situations. (lesson-05)
- **Frontmatter is valid** [P1 if broken]. Exactly two `---` fences; `name` and
  `description` present; no misspelled keys. A typo silently drops the skill from
  the menu. The scan reports `has_frontmatter`, `name_matches_folder`,
  `extra_frontmatter_keys`. (lesson-04/05)
- **Name is kebab-case and matches the folder** [P2]. Scan: `name_matches_folder`.
- **"What this does" + "When to use it" present** [P3]. Triggering and scope kept
  in the description and a When section, not buried in steps. Scan signals
  `has_what_section` / `has_when_section`. (lesson-05)
- **Imperative instructions that explain WHY** [P2]. Steps state the reasoning,
  what to avoid, and what "done" means; a model given reasons outperforms one
  following rote rules. Vague directions ("find the best stories") cause drift.
  (lesson-05)
- **No magic values scattered across files** [P3]. Numeric limits/dates/counts
  ("10 stories", "7 days") defined once with a reason, not duplicated across
  template, rubric and body where they can drift apart. (lesson-05)
- **Explicit failure modes** [P2]. The skill says what to do when a step fails
  (source down → record as skipped; fact-check fails → drop, don't fix). Missing
  fallback behaviour means Claude improvises and defeats the control. (lesson-05)

## B. Subagents, parallelism and model selection

- **Independent work is fanned out, not serial** [P2]. If the skill has N
  independent units (one per source/file/dimension), it dispatches one subagent
  each *in parallel*, not a sequential loop. Scan signals `mentions_parallel`,
  `mentions_subagent`. (lesson-06)
- **Missing subagent opportunities are flagged, not just existing ones graded**
  [P2]. Look for independent, repeated, or per-unit work done inline or serially
  that is not delegated to a subagent (scrape each source, fetch each page,
  process each record, run several independent analyses). Each is a candidate to
  extract into a subagent dispatched in parallel. The check is about work the
  skill *could* parallelise but doesn't, regardless of how many subagents it
  already has. Scan: `summary.likely_missing_subagent_opportunity`,
  `signals.mentions_per_item_work`. (lesson-06)
- **Model matched to job** [P2, the user cares about this]. Mechanical workers →
  `haiku`. Orchestrator and graders → `sonnet`/stronger. Every dispatched agent
  declares a model; "no model" defaults to the expensive path. Scan:
  `agents[].model_declared`, `summary.agents_missing_model`,
  `signals.mentions_haiku`. (lesson-06, lesson-12)
- **Fresh context for grading** [P1 if quality is verified by the producer].
  Any quality check runs in a *separate* agent from the one that produced the
  output; a model grading its own work is primed to agree. (lesson-05/06)
- **Least-privilege tools on agents** [P2, security]. Each agent's `tools` lists
  only what it needs; a read-only worker has no `Write`/`Edit`/`Bash`. Blank
  `tools` means all tools, which is over-granted. Scan: `agents[].tools`,
  `summary.agents_missing_tools`. (lesson-06, lesson-11)
- **Registration caveat handled** [P2]. Skill-nested `agents/*.md` are NOT
  auto-registered; their `model`/`tools` frontmatter does not auto-apply. The
  skill must either promote them to `.claude/agents/` or dispatch a
  general-purpose subagent that reads the file with the model set at dispatch
  time. Flag if `SKILL.md` dispatches a nested agent by name as if registered.
  (lesson-06)

## C. Token and context hygiene

- **SKILL.md is lean** [P3, P2 if extreme]. Long references/templates/rubrics
  live in their own files, not inline in `SKILL.md`, since the description and
  body are re-read often, so bloat costs tokens every turn. Scan: `line_count`,
  `char_count`. A multi-hundred-line SKILL.md with inline templates is a smell.
  (lesson-12)
- **Templates reused, not regenerated** [P3]. Structured output fills a fixed
  `assets/` template rather than inventing a layout each run (also Control 3).
  (lesson-05/12)
- **Concise-output discipline where it matters** [P3]. For high-frequency or
  loop/routine skills, instructions ask for terse output (final result, skip
  preamble) since output tokens dominate cost. (lesson-12)

## D. Security and permissions

- **No secrets in any skill file** [P1]. No API keys, passwords, tokens, or
  secret file contents in `SKILL.md`, agents, references, assets. Anything in a
  read file can reach the model or servers. Reference secrets indirectly
  (settings.local.json), never inline. (lesson-11)
- **No dangerous defaults** [P1 if present]. No instruction to delete or
  overwrite outside a named boundary without confirmation; risky actions default
  to ask, not allow. (lesson-11)
- **Untrusted content treated as data** [P2 if the skill reads the open web or
  user docs]. Instructions say not to follow instructions embedded in fetched
  content (prompt-injection guard). (lesson-11)
- **External MCP/connector dependencies declared** [P2]. If the skill uses an
  MCP/connector or a specific tool (say a search MCP), `SKILL.md` names it and
  notes any setup or auth needed, so it doesn't fail silently on install.
  (lesson-07/11)

## E. Packaging (only if the skill is part of a plugin/marketplace)

- **Plugin structure correct** [P2]. `.claude-plugin/plugin.json` at plugin
  root; skills under top-level `skills/`; `name`, `description`, `version`,
  `author` present; `version` is real semver, not `0.0.0`. (lesson-08)
- **`${CLAUDE_PLUGIN_ROOT}` used for in-plugin paths** [P2]. Cross-file
  references inside a plugin use `${CLAUDE_PLUGIN_ROOT}/skills/<name>/…` so they
  resolve wherever the plugin is installed, not a hardcoded absolute path. Scan:
  `uses_plugin_root`, and any absolute `/Users/...` paths in `SKILL.md` are a
  red flag. (lesson-08)
- **Routine-shaped skills are unattended** [P2 if it's a routine]. Fixed
  input/process/output paths; explicit "do not ask for confirmation"; no pauses
  for approval; a routine that waits for a human hangs. (lesson-09)

## F. Reliability, runtime and scaling

- **Preflight dependency check / fail-fast** [P1 if long or writes partial
  state, else P2]. As an EARLY step the skill verifies it has access to every
  hard dependency (required tools, MCP/connectors, credentials, input files, its
  own scripts/templates) and aborts with a clear message if any is missing.
  The failure to prevent: a long pipeline that only discovers a missing tool at
  the last step, wasting time/tokens and leaving partial output. Scan:
  `mentions_preflight_check` (hint only), `broken_referenced_paths` (proves a
  script/template the skill needs is absent). (lesson-09/11)
- **Scripts pre-stored, not generated at run time** [P2]. Deterministic process
  logic lives as committed files in `scripts/` that the skill *runs*; the skill
  must not write/create/generate scripts on the fly (unreviewed, non-
  deterministic, re-authored each run). Scan: `writes_scripts_on_the_fly`.
  (Control 2)
- **Runtime estimated and independent work parallelised** [P2 for a missed
  parallel win]. The audit should estimate end-to-end wall-clock and flag
  independent work done serially. Match the mechanism to the scale:
  - a handful of independent units → parallel subagent dispatch (Control 4);
  - a **large or unbounded** fan-out (one-per-page across a whole site →
    hundreds/thousands of units, per-record over a big dataset, loop-until-done)
    → a **dynamic Workflow** (`pipeline()`/`parallel()`), which provides a
    concurrency cap, batching, per-item isolation and resumability that
    hand-dispatching N subagents from `SKILL.md` cannot. Recommend it explicitly
    for those cases. Scan: `mentions_large_fanout`, `mentions_dynamic_workflow`.
- **Output stored in a structured, repeatable way** [P2]. Beyond a fixed
  template (Control 3), the deliverable has a deterministic destination and
  naming: a named folder plus a predictable filename scheme (e.g.
  `reports/<thing>-<date>.md`), or a defined database/table write, not a path
  and filename Claude invents each run. Ad-hoc output location is output drift.
  (Control 3)
- **Error handling: retries, fallbacks, stop-steps** [P2, P1 if a silent
  failure would corrupt output]. The skill anticipates that tools, MCPs and
  scripts can fail and says what to do; it does not assume the happy path. At
  least one of these, matched to the step:
  - **retry** a transient failure a bounded number of times (e.g. up to 3) before
    giving up, bounded, never an infinite loop;
  - a **fallback** tool/process when the primary is unavailable (and a note to
    report that the fallback was used);
  - a **stop-step**: if a step genuinely can't be done (no access, hard error,
    empty required input), STOP with a clear message rather than blundering on
    with bad or partial data.
  The anti-pattern: no error handling, so one tool hiccup silently produces a
  wrong or half-built deliverable. Distinguish this from the Control-2 escape
  hatch (which is about *improvising* when a script's assumptions change); this is
  about *failures*: retry, fall back, or stop. Scan: `mentions_error_handling`,
  `mentions_retry`, `mentions_stop_step` (hints; confirm by reading). (lesson-09)
- **Intermediate state / checkpointing for long skills** [P2 for a long skill;
  ⚠️ over-engineering (P3) if a trivially short skill carries checkpointing it
  doesn't need; N/A otherwise]. A long, many-step skill (roughly 8+ steps, and
  especially 30+) should persist intermediate state after each step to a file
  (e.g. `state.json` or a progress file) so that (a) results survive context
  compaction in a long run, and (b) on an error the skill can resume from the
  last good step instead of restarting from zero. Without it, a failure at step
  28 throws away the work of steps 1 to 27. Scan: `step_count`,
  `mentions_state_checkpoint`. Recommend it when `step_count` is high and no
  checkpointing is mentioned; for very large fan-outs the dynamic Workflow's
  built-in resumability covers this instead.

## G. Subagent and runtime economics (speed / quality / cost)

Concrete levers from lessons 06/10/12/03 that cut cost and wall-clock without
losing quality. Most are checkable from agent frontmatter and dispatch prose.

- **`effort` matched to task difficulty** [P2, the highest-value new lever].
  Each agent declares an `effort` (low/medium/high/xhigh/max) proportionate to
  the reasoning needed: `low`/`medium` for mechanical or rote work (extract,
  filter, format, count), `high`+ only for multi-signal judgement. `effort` is
  the per-agent reasoning-cost knob; defaulting it runs rote work at full
  reasoning cost. Registration caveat: a skill-nested agent's `effort` frontmatter
  is NOT auto-applied; the orchestrator must set it at dispatch or it's silently
  lost (the same trap as `model`). Scan: `agents[].effort_declared`,
  `summary.agents_missing_effort`, `signals.mentions_effort`. ❌ a mechanical
  worker at `effort: high` or no effort; a judgement agent left at default.
  (lesson-06/12)
- **Batch many small units per subagent, don't go 1-per-tiny-unit** [P2 for a
  large fan-out]. Each subagent costs spawn overhead (~0.5 to 1k tokens). 500
  agents × 1 item each wastes ~500k tokens of overhead; 10 to 50 agents each
  handling a batch amortises it. Recommend batching when the fan-out is many tiny
  units (and a dynamic Workflow when it's huge, area F). Scan:
  `signals.mentions_batching`, `signals.mentions_large_fanout`. ❌ "dispatch one
  subagent per row" over a big dataset. (lesson-06)
- **Pass only the relevant context slice to a subagent** [P2]. The dispatch
  prompt gives the agent just what it needs (a file path, a scoped query, the
  relevant slice of upstream data), not the whole conversation/project/blob.
  Bloated dispatch inputs cost tokens on every spawn. Scan:
  `signals.mentions_context_slice`. ❌ handing each worker the entire context to
  do a narrow job. (lesson-06)
- **Subagents return only clean results, not transcripts** [P2]. The worker
  prompt says "return only the final result (JSON/list/markdown); no reasoning,
  no transcript." A subagent that returns its full chain-of-thought piles into
  the orchestrator context and is re-read every later turn. Scan:
  `signals.mentions_return_only_result`. ❌ workers that narrate their process
  back to the orchestrator. (lesson-06/12)
- **Cache-friendly read ordering** [P3]. Large, stable files (references,
  templates, rubrics) are read once, early, in a deterministic order, not
  re-opened per item across many turns (each re-read is a cache miss). Lazy-read
  deep-rationale docs only when a borderline call needs them. ❌ the same 10k
  reference re-read on turns 1, 5 and 12. (lesson-12/03)
- **Model-tiering discipline: don't default to the biggest model** [P2]. Choose
  Haiku → Sonnet → Opus by genuine need; reserve Opus for the hardest synthesis,
  and never put Opus on a per-iteration path by default. Scan:
  `signals.mentions_opus`, `agents[].model`. ❌ every agent on Opus "to be safe".
  (lesson-12)
- **High-frequency (loop/routine) cost awareness** [P2 if it runs often]. A skill
  meant to run on `/loop` or as a scheduled routine names its per-iteration cost
  driver, picks a cheap model/effort for the repeated path, and notes when the
  interval must lengthen to stay in budget; a 1-minute Opus loop is silently
  expensive. Scan: `signals.mentions_loop_or_routine`,
  `signals.mentions_cost_awareness`. (lesson-10/09/12)
- **Context-window discipline and memory reuse for long/recurring skills** [P3].
  Long runs note `/compact` or context discipline (complements checkpointing,
  area F); recurring skills cache stable derived facts (source lists, glossaries)
  in `references/`, CLAUDE.md or memory rather than re-deriving them each run.
  Scan: `signals.mentions_compact`, `signals.mentions_memory_reuse`. (lesson-03/12)

## How to use this list

- Only raise an item that genuinely applies; most of D/E/G are conditional.
- Tie every finding to evidence: a quoted line, a `file:line`, or a scan field.
- Prefer a few high-confidence findings over a long speculative list. An
  unverifiable "maybe" belongs in a short "worth checking" note, not as a defect.
