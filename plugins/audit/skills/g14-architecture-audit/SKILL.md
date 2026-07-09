---
name: g14-architecture-audit
description: >
  Single-lens focused architecture audit of a codebase — coupling, cohesion,
  layering, abstraction quality, testability, tech debt. Resolves a target path,
  runs the `architecture-auditor` agent against it (sonnet, effort high,
  read-only tools), and consolidates its findings into a severity-ranked
  markdown report saved under <target>/reports/. Trigger whenever the user asks
  to "architecture audit", "architecture review of this project", "check
  architectural soundness", "design review", "module structure review", or
  wants to know how well a codebase is organized, how easy it is to change, or
  what the architectural debt looks like.
---

# audit:g14-architecture-audit

Thin runner. The `architecture-auditor` agent at `${CLAUDE_PLUGIN_ROOT}/agents/architecture-auditor.md` is the **source of truth** for the architecture lens (what to look for, severity rubric, output contract). This skill only resolves the target, invokes the agent, and consolidates its output into the deliverable report.

## Pipeline (4 steps)

### 1 · Resolve target

Infer the target path from the user message:

- No hint → use `cwd`.
- Folder name mentioned → look relative to cwd, then one level up, then `find . -maxdepth 3 -type d -name '<hint>'`. Single match = use it; multiple = ask.
- Absolute path given → use verbatim.
- Ambiguous → ask one short question; don't run against the wrong target.

Then canonicalize and prepare output:

```bash
TARGET=$(cd "<inferred>" && pwd)
mkdir -p "$TARGET/reports"
TIMESTAMP=$(date +%Y-%m-%d-%H%M)
REPORT_PATH="$TARGET/reports/architecture-audit-$TIMESTAMP.md"
```

Confirm in one line **only if the target wasn't explicit**. If the user said "audit `/exact/path`", just launch.

### 2 · Launch the architecture-auditor agent

Send **one `Task` tool call** with `subagent_type: "architecture-auditor"`. The agent already knows its lens, rubric and output format — pass only the inputs it expects.

Prompt:

```
target_path: {{TARGET}}
project_name: {{basename of TARGET}}
language: {{user's conversation language, default English}}

Run a full architecture audit against target_path and return the report
verbatim in the format your agent file specifies.
```

Set `description` to `"Architecture audit — <project name>"`. Do NOT override the agent's model/effort/tools — they are fixed in the agent frontmatter for a reason.

If the `Task` call errors, times out, or the returned report doesn't match the agent's documented output shape (`# Architecture Analysis` / `## Summary` / `## Findings`), stop and tell the user the audit could not complete. Never write a partial or fabricated report.

### 3 · Consolidate the final report

Read `${CLAUDE_PLUGIN_ROOT}/skills/g14-architecture-audit/assets/report-template.md`. Fill every placeholder using the agent's output:

- **Executive summary** — write fresh from the agent's Summary and Overall rating. Highlight the single biggest architectural risk in one clear sentence.
- **Top findings table** — pick up to 5 highest-severity findings, ordered by severity then blast radius.
- **Severity counts** — real numbers per severity level.
- **Findings section** — paste the agent's findings verbatim, preserving their ordering (CRITICAL → HIGH → MEDIUM → LOW → INFO).
- **Prioritized action plan** — build it yourself from effort × severity × blast radius, NOT raw severity alone. "Do first" = CRITICAL/HIGH with S/M effort. "Do next" = HIGH with L effort + MEDIUM that compounds. "Backlog" = LOW + INFO + opportunistic.
- **Methodology caveats** — copy the agent's "Notes & caveats" section verbatim.
- **Output language** — report prose matches the language the user is using in the current conversation. Default to English if unclear. Severity labels (CRITICAL / HIGH / MEDIUM / LOW / INFO) always stay in English — they're greppable.

Save with `Write` to `$REPORT_PATH`.

### 4 · Report back

Brief chat message only — the full report is in the file:

```
Architecture audit complete → <report-path>

Counts: X CRITICAL / Y HIGH / Z MEDIUM / W LOW / V INFO

Top 3 findings:
1. [SEV] Title — category
2. [SEV] Title — category
3. [SEV] Title — category
```

Don't dump the report into chat.

## Hard rules

- **Don't duplicate the agent.** All lens content (what to look for, severity rubric, output contract) lives in `${CLAUDE_PLUGIN_ROOT}/agents/architecture-auditor.md`. If you find yourself tempted to re-state it here, stop — update the agent instead.
- **One agent, one lens.** No scope creep into security, scalability, clean-code, or database — those have their own agents.
- **Read-only.** Never modify target code. The agent's tools are constrained to read-only; keep this skill aligned.
- **Template is the contract.** Don't renegotiate mid-run.
- **Severity labels stay English** — they are greppable across reports.
