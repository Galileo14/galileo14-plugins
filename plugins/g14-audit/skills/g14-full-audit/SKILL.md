---
name: g14-full-audit
description: >
  Runs multiple codebase-lens audits together, in parallel, and consolidates
  them into one combined report (markdown + HTML). Asks the user which lenses
  to run — security, scalability, architecture, clean-code, database — unless
  they were already named in the request. Fans out to the existing
  security-auditor / scalability-auditor / architecture-auditor /
  clean-code-auditor / database-auditor agents (no new agent of its own) and
  saves both reports under <target>/reports/. Trigger whenever the user asks
  for a "full audit", "complete audit", "run all audits", "audit everything",
  "combined audit report", "run every lens on this project", "give me the
  full picture on this codebase", or wants several audit lenses run together
  instead of one at a time.
---

# audit:g14-full-audit

Orchestrator, not a thin runner. Unlike the five single-lens skills, this one doesn't own or duplicate any lens content — it **fans out to the existing plugin-root agents in parallel** (`security-auditor`, `scalability-auditor`, `architecture-auditor`, `clean-code-auditor`, `database-auditor`) and consolidates their independent reports into one combined deliverable. No new agent is created for this skill; the five lens agents remain the single source of truth for their lenses.

## Pipeline (5 steps)

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
REPORT_MD_PATH="$TARGET/reports/full-audit-$TIMESTAMP.md"
REPORT_HTML_PATH="$TARGET/reports/full-audit-$TIMESTAMP.html"
```

### 2 · Pick the lenses

Five available lenses: **Security, Scalability, Architecture, Clean-Code, Database**.

- If the user's message already names specific lenses (e.g. "full audit with security and database"), use exactly those — don't ask.
- If the user said "full audit", "audit everything", "all lenses", or similar with no lens named, treat that as **all 5** — don't ask.
- Otherwise (ambiguous or the user just invoked this skill with no detail), ask one short question in chat: which of the 5 lenses to run, offering "all 5" as the fast default. Wait for the answer before continuing.

Confirm the resolved target and chosen lenses in one line before launching, unless both were already explicit in the user's message.

### 3 · Launch the chosen lens agents in parallel

Send **one message with one `Task` tool call per chosen lens**, all in the same turn so they run concurrently. Each agent already knows its lens, rubric and output format — pass only the inputs it expects, identical to what each standalone skill sends:

```
target_path: {{TARGET}}
project_name: {{basename of TARGET}}
language: {{user's conversation language, default English}}

Run a full <lens> audit against target_path and return the report verbatim
in the format your agent file specifies.
```

| Lens | `subagent_type` |
|---|---|
| Security | `security-auditor` |
| Scalability | `scalability-auditor` |
| Architecture | `architecture-auditor` |
| Clean-Code | `clean-code-auditor` |
| Database | `database-auditor` |

Set each call's `description` to `"<Lens> audit — <project name>"`. Do NOT override any agent's model/effort/tools — they are fixed in each agent's frontmatter for a reason. Wait for all chosen agents to return before consolidating.

If a lens `Task` errors, times out, or returns no usable report, retry that lens once (same inputs). If it still fails, don't count it as run: move it to "Lenses not run" in step 4 with reason `agent failed` — distinct from a lens the user chose not to run — and call this out explicitly in the step 5 chat summary.

### 4 · Consolidate the combined reports

Read `${CLAUDE_PLUGIN_ROOT}/skills/g14-full-audit/assets/report-template.md` and `${CLAUDE_PLUGIN_ROOT}/skills/g14-full-audit/assets/report-template.html`. Fill every placeholder in both from the same underlying data — they must report identical findings and counts, only the rendering differs:

- **Overall rating** — the worst rating among the lenses actually run (`critical` > `at-risk` > `healthy`).
- **Executive summary** — write fresh, synthesizing across all lenses run: what kind of project this is, the single biggest risk across all lenses, one sentence per lens on its posture.
- **Cross-lens top findings** — pool every CRITICAL/HIGH finding from every lens run, pick the top 5–8 by severity then blast radius, tag each with its lens.
- **Combined severity counts** — sum of CRITICAL/HIGH/MEDIUM/LOW/INFO across all lenses run, plus a per-lens breakdown table.
- **One section per lens run** — paste that lens agent's findings verbatim (preserving CRITICAL → HIGH → MEDIUM → LOW → INFO ordering) under its own heading. Skip sections for lenses that weren't run — do not write placeholder text for them.
- **Prioritized action plan** — build one combined plan from effort × severity × blast radius across every lens run, same bucketing as the single-lens skills ("Do first" / "Do next" / "Backlog").
- **Methodology & caveats** — list which lenses ran, which were skipped and why (user's choice, or `agent failed` if a lens Task still failed after one retry), and copy each ran agent's own "Notes & caveats" verbatim under its lens.
- **Output language** — report prose matches the language the user is using in the current conversation. Default to English if unclear. Severity labels (CRITICAL / HIGH / MEDIUM / LOW / INFO) always stay in English — they are greppable.

Save the markdown with `Write` to `$REPORT_MD_PATH` and the HTML with `Write` to `$REPORT_HTML_PATH`.

Then run a mechanical parity check: count each severity badge (CRITICAL / HIGH / MEDIUM / LOW / INFO) in both saved files and confirm the counts match before reporting back. If they don't, the two files have drifted — fix whichever file is wrong, then re-check before moving to step 5.

### 5 · Report back

Brief chat message only — the full reports are in the files:

```
Full audit complete → <report-md-path>
HTML version → <report-html-path>

Lenses run: Security, Scalability, ... (N of 5)
Lenses not run: {{comma-separated list with reason per lens, e.g. "Database (user's choice)", "Architecture (agent failed after retry)" — omit this line if all chosen lenses ran}}

Combined counts: X CRITICAL / Y HIGH / Z MEDIUM / W LOW / V INFO

Top 3 findings:
1. [SEV] Title — lens
2. [SEV] Title — lens
3. [SEV] Title — lens
```

Don't dump either report into chat.

## Hard rules

- **Don't duplicate any agent.** All lens content (what to look for, severity rubric, output contract) lives in each lens's own agent file under `${CLAUDE_PLUGIN_ROOT}/agents/`. This skill never re-states it — it only launches and consolidates.
- **No new agent.** This skill reuses the five existing lens agents. If a sixth lens is ever needed, add it as its own agent + standalone skill first, then wire it into this orchestrator's lens table.
- **Read-only.** Never modify target code. Every lens agent's tools are constrained to read-only; keep this skill aligned.
- **Both templates are the contract.** Don't renegotiate their structure mid-run, and don't let the `.md` and `.html` versions drift apart in content.
- **Severity labels stay English** — they are greppable across reports.
