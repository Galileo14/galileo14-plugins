# audit plugin — architecture

Codebase audits for Galileo14 across four lenses — security, scalability, architecture, clean-code. Four user-facing **skills** that produce a severity-ranked markdown report each, all delegating to **four single-lens auditor agents** at the plugin root.

## The shape

```
plugins/audit/
├── agents/
│   ├── security-auditor.md           ← owns the security lens (OWASP-shaped checklist + rubric)
│   ├── scalability-auditor.md        ← owns the scalability lens (DB / cache / I/O / etc.)
│   ├── architecture-auditor.md       ← owns the architecture lens (coupling / cohesion / layering)
│   └── clean-code-auditor.md         ← owns the per-file craftsmanship lens
└── skills/
    ├── g14-security-audit/                ← runner — resolves target, invokes agent, consolidates
    ├── g14-scalability-audit/             ← runner — same shape
    ├── g14-architecture-audit/            ← runner — same shape
    ├── g14-clean-code-audit/              ← runner — same shape
    │   └── assets/report-template.md  ← per-skill report skeleton (skill-specific output)
    └── g14-skill-audit/                   ← SELF-CONTAINED orchestrator (see note below), NOT a thin runner
        ├── scripts/scan_skill.py     ← deterministic structural inventory of a target skill
        ├── references/               ← pinned audit rubric + best-practices + vendored framework docs
        ├── assets/report-template.md ← report skeleton
        ├── agents/                   ← nested instruction files (dimension-auditor, grader)
        └── tests/                    ← four fresh-grader rubrics (quality gate)
```

## Exception — g14-skill-audit does NOT follow the thin-runner norm

The four codebase-audit skills are thin runners over a single plugin-root lens
agent. **g14-skill-audit is deliberately different** — the one skill that breaks
that mould, for good reasons:

- Its "lens" (auditing Claude Code *skills* against the five-controls framework)
  is not shared with any other skill, so the no-duplication rationale for hoisting
  lens content into a plugin-root agent doesn't apply.
- It is a multi-step *orchestrator*, not a one-Task runner: it runs a
  deterministic scan script (Control 2), reads a pinned rubric (Control 1),
  fans out grouped fresh auditors scaled to target size (Control 4), fills a
  fixed template saved to a deterministic path (Control 3), and runs a
  fresh-grader quality gate (Control 5). It dogfoods the framework it audits.
- It keeps its agents *nested* (`agents/dimension-auditor.md`, `agents/grader.md`)
  and dispatches them as `general-purpose` subagents that read the instruction
  file (model set at dispatch) — the documented portable alternative to
  plugin-root registration. It vendors the framework reference docs
  (`five-controls.md`, `decision-table.md`) and the grader contract, so it has no
  cross-plugin dependencies.

If you extend it, keep it self-contained — don't hoist its agents to the plugin
root unless a second skill ever needs the same skill-audit lens.

## The norm — agents own, skills compose

**The audit lens lives in the agent. The skill is a thin runner.** Each agent is the single source of truth for one lens: what to look for, severity rubric, scope rules, output contract. The skill knows nothing about the lens — it only:

1. Resolves the target path from the user message.
2. Invokes the matching agent via the `Task` tool, passing `target_path`, `project_name`, `language`.
3. Consolidates the agent's findings into the skill's `assets/report-template.md`.
4. Writes the report and posts a brief chat summary.

If two skills ever needed the same lens content (they don't, but if they did), they would call the same agent. No duplication. Update the agent once, both runners benefit.

| Concept | Owner (single source of truth) | Skill that consumes it |
|---|---|---|
| Security lens (what to look for, OWASP-shaped checklist, severity rubric) | `security-auditor` agent | g14-security-audit |
| Scalability lens (ceilings, DB / cache / I/O / concurrency / infra) | `scalability-auditor` agent | g14-scalability-audit |
| Architecture lens (coupling / cohesion / layering / abstraction / tech debt) | `architecture-auditor` agent | g14-architecture-audit |
| Clean-code lens (per-file craftsmanship: naming / nesting / duplication / smells) | `clean-code-auditor` agent | g14-clean-code-audit |
| Report skeleton (executive summary, top findings table, action plan, severity legend) | `assets/report-template.md` inside each skill | the same skill |

Skills keep what is genuinely **skill-specific**: the target-resolution heuristic, the report template, the final chat-summary format. Everything about *what an audit is and how to judge severity* belongs in the agent.

## When to add a new agent vs a new skill

**New agent** if:
- A new audit lens emerges (e.g. accessibility, ops/SRE, cost) that doesn't fit any existing lens.
- Two or more skills would start duplicating the same lens content.

**New skill** if:
- A new audit workflow needs a different output shape (e.g. a JSON-only audit for CI, a slack-summary audit, a diff-only review). The agent stays — the runner around it changes.

If you find yourself adding lens content (categories, severity rules, output fields) to a skill, stop — that belongs in the agent.

## Model + effort + tools per agent

All four agents are fixed in frontmatter so the runner can't tune them mid-flight:

| Agent | model | effort | tools | Why |
|---|---|---|---|---|
| `security-auditor` | sonnet | high | Read, Grep, Glob, Bash | High-stakes pattern matching across many dimensions; needs careful reasoning on attack surface |
| `scalability-auditor` | sonnet | high | Read, Grep, Glob, Bash | Judgment about where ceilings are and how close the project is to them |
| `architecture-auditor` | sonnet | high | Read, Grep, Glob, Bash | Synthesis across coupling / cohesion / layering — multi-signal reasoning |
| `clean-code-auditor` | sonnet | medium | Read, Grep, Glob, Bash | Breadth over depth; per-file craftsmanship checks with less cross-cutting judgment |

Plugin agents do not support `thinking` / `reasoning` in frontmatter; `effort` (low / medium / high / xhigh / max) is the available knob. Tools are read-only intentionally: agents must never modify the target.

## How the skill invokes the agent

Each skill sends one `Task` tool call with `subagent_type` set to the agent name (e.g. `"security-auditor"`). The prompt passes only the inputs the agent expects:

```
target_path: <absolute path>
project_name: <basename>
language: <user's conversation language>

Run a full <lens> audit against target_path and return the report verbatim
in the format your agent file specifies.
```

The skill never re-states the agent's rubric or output format in the prompt — the agent already knows. The skill never overrides the agent's `model` / `effort` / `tools` — they are fixed for a reason.

## Adding to the plugin

When adding a skill or agent, update this file's tree, the table of owners, and the model/effort/tools table. This file is the entry point for anyone (including future-you) trying to understand how the plugin composes.
