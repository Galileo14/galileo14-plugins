---
name: g14-database-audit
description: >
  Focused single-lens database audit of a codebase. Resolves a target path,
  runs the `database-auditor` agent against it (sonnet, effort high,
  read-only tools), and consolidates the agent's findings into a
  severity-ranked markdown report saved under <target>/reports/. Trigger
  whenever the user asks for a database audit, wants to check schema/query
  soundness, says things like "database audit", "audit the database layer",
  "check our schema/migrations", "review our queries for issues", "find
  database issues", "data integrity review", "N+1 query check", or
  "audit our ORM usage".
---

# audit:g14-database-audit

Thin runner. The `database-auditor` agent at `${CLAUDE_PLUGIN_ROOT}/agents/database-auditor.md` is the **source of truth** for the database lens (what to look for, severity rubric, output contract). This skill only resolves the target, invokes the agent, and consolidates its output into the deliverable report.

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
if [ -z "$TARGET" ] || [ ! -d "$TARGET" ]; then
  echo "ERROR: could not resolve target path" >&2
  exit 1
fi
mkdir -p "$TARGET/reports"
TIMESTAMP=$(date +%Y-%m-%d-%H%M)
REPORT_PATH="$TARGET/reports/database-audit-$TIMESTAMP.md"
```

If that guard fires, stop and tell the user the target path couldn't be resolved — don't fall back to a default or guess.

Confirm in one line **only if the target wasn't explicit**. If the user said "audit `/exact/path`", just launch.

### 2 · Launch the database-auditor agent

Send **one `Task` tool call** with `subagent_type: "database-auditor"`. The agent already knows its lens, rubric and output format — pass only the inputs it expects.

Prompt:

```
target_path: {{TARGET}}
project_name: {{basename of TARGET}}
language: {{user's conversation language, default English}}

Run a full database audit against target_path and return the report verbatim
in the format your agent file specifies.
```

Set `description` to `"Database audit — <project name>"`. Do NOT override the agent's model/effort/tools — they are fixed in the agent frontmatter for a reason.

If the `Task` call errors, times out, or returns no report, stop and tell the user the audit could not complete — don't fabricate findings or retry silently.

### 3 · Consolidate the final report

Read `${CLAUDE_PLUGIN_ROOT}/skills/g14-database-audit/assets/report-template.md`. Fill every placeholder using the agent's output. If an expected section (e.g. "Notes & caveats") is missing from the agent's output, write "Not reported" in its place — never invent content.

- **Executive summary** — write fresh from the agent's Summary and Overall rating. Highlight the biggest data-integrity or reliability risk in one clear sentence.
- **Top findings table** — pick the top 3 findings by severity × blast radius.
- **Severity counts** — real numbers per severity bucket.
- **Findings section** — paste the agent's findings verbatim, preserving their CRITICAL → HIGH → MEDIUM → LOW → INFO ordering.
- **Prioritized action plan** — build from effort × severity × blast radius. "Do first" = CRITICAL/HIGH with S/M effort + anything risking data loss/corruption/breach. "Do next" = HIGH with L effort + MEDIUM that compounds. "Backlog" = LOW + INFO + opportunistic.
- **Methodology caveats** — copy the agent's "Notes & caveats" section verbatim, or "Not reported" if the agent's output doesn't include it.
- **Output language** — report prose matches the language the user is using in the current conversation. Default to English if unclear. Severity labels (CRITICAL / HIGH / MEDIUM / LOW / INFO) always stay in English — they are greppable constants.

Save with `Write` to `$REPORT_PATH`.

### 4 · Report back

Brief chat message only — the full report is in the file:

```
Database audit complete → <report-path>

Counts: X CRITICAL / Y HIGH / Z MEDIUM / W LOW / V INFO

Top 3 findings:
1. [SEV] Title — category
2. [SEV] Title — category
3. [SEV] Title — category
```

Don't dump the report into chat.

## Hard rules

- **Don't duplicate the agent.** All lens content (what to look for, severity rubric, output contract) lives in `${CLAUDE_PLUGIN_ROOT}/agents/database-auditor.md`. If you find yourself tempted to re-state it here, stop — update the agent instead.
- **One agent, one lens.** No scope creep into security, scalability, architecture, or clean-code — those have their own agents.
- **Read-only.** Never modify target code, never run migrations, never connect to a live database. The agent's tools are constrained to read-only; keep this skill aligned.
- **Template is the contract.** Don't renegotiate mid-run.
- **Severity labels stay English** — they are greppable across reports.
