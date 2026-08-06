---
name: g14-clean-code-audit
description: >
  Static clean-code audit of a whole codebase — NOT a diff review. Resolves a
  target path, runs the `clean-code-auditor` agent against it (sonnet, effort
  medium, read-only tools), and consolidates the agent's findings into a
  severity-ranked markdown report saved to
  <target>/reports/clean-code-audit-<timestamp>.md with concrete file:line
  citations and fix steps. Trigger when the user says: "clean code audit",
  "code quality review", "scan this codebase for code smells", "audit for
  maintainability", "find tech debt in this project", "review the craftsmanship
  of this code", "check code quality", "identify code smells", "look for bad
  code patterns", "maintainability audit", or any phrasing asking for a
  per-file craftsmanship review rather than a diff/PR review or high-level
  architecture review.
---

# audit:g14-clean-code-audit

Thin runner. The `clean-code-auditor` agent at `${CLAUDE_PLUGIN_ROOT}/agents/clean-code-auditor.md` is the **source of truth** for the clean-code lens (what counts as a smell, what's out of scope, severity rubric, output contract). This skill only resolves the target, invokes the agent, and consolidates its output into the deliverable report.

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
REPORT_PATH="$TARGET/reports/clean-code-audit-$TIMESTAMP.md"
```

Confirm in one line **only if the target wasn't explicit**. If the user gave an exact path, just launch.

### 2 · Launch the clean-code-auditor agent

Send **one `Task` tool call** with `subagent_type: "clean-code-auditor"`. The agent already knows its lens, scope boundaries, sampling strategy and output format — pass only the inputs it expects.

Prompt:

```
target_path: {{TARGET}}
project_name: {{basename of TARGET}}
language: {{user's conversation language, default English}}

Run a full clean-code audit against target_path and return the report verbatim
in the format your agent file specifies.
```

Set `description` to `"Clean-code audit — <project name>"`. Do NOT override the agent's model/effort/tools — they are fixed in the agent frontmatter for a reason.

If the `Task` call errors, times out, or the returned report doesn't match the agent's documented output shape (`# Clean-Code Analysis` / `## Summary` / `## Findings`), stop and tell the user the audit could not complete. Never fill the template with guessed or partial content.

### 3 · Consolidate the final report

Read `${CLAUDE_PLUGIN_ROOT}/skills/g14-clean-code-audit/assets/report-template.md`. Fill every placeholder using the agent's output:

- **Project name** — infer from the target folder name or top-level package manifest.
- **Executive summary** — write fresh from the agent's Summary section; don't copy verbatim. State overall craftsmanship posture in 2–4 sentences.
- **Top findings table** — pick the top 5 by severity, then blast radius. If fewer than 5 findings, fill as many rows as exist.
- **Severity counts** — real numbers from the agent's output.
- **Findings section** — paste the agent's findings verbatim, preserving ordering (CRITICAL → HIGH → MEDIUM → LOW → INFO).
- **Prioritized action plan** — build it yourself from effort × severity × blast radius. "Do first" = CRITICAL/HIGH with S/M effort. "Do next" = HIGH with L effort + MEDIUM that compounds. "Backlog" = LOW + INFO + opportunistic.
- **Sampling notes** — copy the agent's Notes section verbatim into the Methodology block.
- **Language** — report prose matches the language the user is using in the current conversation. Default to English if unclear. Severity labels (CRITICAL / HIGH / MEDIUM / LOW / INFO) always stay in English — they're greppable.

Save with `Write` to `$REPORT_PATH`.

### 4 · Report back

Brief chat message only — the full report is in the file. Do NOT dump the report into chat.

```
Clean-code audit complete → <report-path>

Counts: X CRITICAL / Y HIGH / Z MEDIUM / W LOW / V INFO

Top 3 findings:
1. [SEV] Title — category
2. [SEV] Title — category
3. [SEV] Title — category
```

## Hard rules

- **Don't duplicate the agent.** All lens content (what to look for, what's out of scope, severity rubric, sampling strategy, output contract) lives in `${CLAUDE_PLUGIN_ROOT}/agents/clean-code-auditor.md`. If you find yourself tempted to re-state it here, stop — update the agent instead.
- **One agent, one lens.** No scope creep into security, scalability, architecture, or database — those have their own agents.
- **Read-only.** Never modify any file in the target codebase. Non-negotiable.
- **Template is the contract.** Don't renegotiate the structure mid-run.
- **Severity labels stay English** — they are greppable across reports.
