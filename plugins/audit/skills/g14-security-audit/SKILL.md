---
name: g14-security-audit
description: >
  Focused single-lens security audit of a codebase. Resolves a target path, runs
  the `security-auditor` agent against it (sonnet, effort high, read-only tools),
  and consolidates the agent's findings into a severity-ranked markdown report
  saved under <target>/reports/. Trigger whenever the user asks for a security
  audit, wants to check the security posture of a project, scan for
  vulnerabilities, or says things like "security audit of this project", "audit
  security of X", "check security posture", "scan for vulnerabilities",
  "security review of this codebase", "find security issues in X", "is this code
  secure".
---

# audit:g14-security-audit

Thin runner. The `security-auditor` agent at `${CLAUDE_PLUGIN_ROOT}/agents/security-auditor.md` is the **source of truth** for the security lens (what to look for, severity rubric, output contract). This skill only resolves the target, invokes the agent, and consolidates its output into the deliverable report.

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
REPORT_PATH="$TARGET/reports/security-audit-$TIMESTAMP.md"
```

Confirm in one line **only if the target wasn't explicit**. If the user said "audit `/exact/path`", just launch.

### 2 · Launch the security-auditor agent

Send **one `Task` tool call** with `subagent_type: "security-auditor"`. The agent already knows its lens, rubric and output format — pass only the inputs it expects.

Prompt:

```
target_path: {{TARGET}}
project_name: {{basename of TARGET}}
language: {{user's conversation language, default English}}

Run a full security audit against target_path and return the report verbatim in
the format your agent file specifies.
```

Set `description` to `"Security audit — <project name>"`. Do NOT override the agent's model/effort/tools — they are fixed in the agent frontmatter for a reason.

### 3 · Consolidate the final report

Read `${CLAUDE_PLUGIN_ROOT}/skills/g14-security-audit/assets/report-template.md` and fill every placeholder using the agent's output:

- **Executive summary** — write fresh from the agent's Summary and Overall rating. Don't copy verbatim; synthesize the posture in 2–4 sentences.
- **Top findings table** — pick up to 5 highest-severity findings, ordered by severity then blast radius.
- **Severity counts** — real numbers from the agent's findings.
- **Findings section** — paste the agent's findings verbatim, preserving their ordering (CRITICAL → HIGH → MEDIUM → LOW → INFO).
- **Prioritized action plan** — build it from effort × severity × blast radius. "Do first" = CRITICAL/HIGH with S/M effort + anything imminently exploitable. "Do next" = HIGH with L effort + MEDIUM that compounds. "Backlog" = LOW + INFO + hardening.
- **Methodology caveats** — copy the agent's Notes & caveats verbatim.
- **Output language** — report prose matches the language the user is using in the current conversation. Default to English if unclear. Severity labels (CRITICAL / HIGH / MEDIUM / LOW / INFO) always stay in English — they are greppable.

Save the filled report with `Write` to `$REPORT_PATH`.

### 4 · Report back

Brief chat message only — the full report is in the file:

```
Security audit complete → <report-path>

Counts: X CRITICAL / Y HIGH / Z MEDIUM / W LOW / V INFO

Top 3 findings:
1. [SEV] Title — category
2. [SEV] Title — category
3. [SEV] Title — category
```

Don't dump the full report into chat.

## Hard rules

- **Don't duplicate the agent.** All lens content (what to look for, severity rubric, output contract) lives in `${CLAUDE_PLUGIN_ROOT}/agents/security-auditor.md`. If you find yourself tempted to re-state it here, stop — update the agent instead.
- **One agent, one lens.** No scope creep into scalability, architecture, clean-code, or database — those have their own agents.
- **Read-only.** Never modify target code. The agent's tools are constrained to read-only; keep this skill aligned.
- **Template is the contract.** Fill every placeholder; don't drop sections.
- **Severity labels stay English** — they are greppable across reports.
