<!--
  g14-database-audit report template.
  Placeholders are in {{double-curly}} format. Fill every placeholder.
  Don't remove sections — if the analyst came back clean, write "No findings." inside.
  Keep severity labels in English (CRITICAL / HIGH / MEDIUM / LOW / INFO) so they're
  greppable and consistent across reports, even when the prose is in another language.
-->

# Database Audit Report

- **Project:** {{project_name}}
- **Path:** `{{absolute_path}}`
- **Date:** {{YYYY-MM-DD HH:MM}}
- **Auditor:** Claude Code — `audit:g14-database-audit` skill
- **Lens:** Database
- **Scope:** {{files_analyzed}} files · {{loc_approx}} LOC (approx.)

---

## Executive Summary

**Overall health:** {{healthy | at-risk | critical}}

{{2–4 sentence narrative: what kind of data layer this project has, what's the big-picture posture, what is the single most important thing the reader should walk away knowing.}}

### Top findings

Ordered by severity, then by blast radius.

| #   | Severity | Category  | Finding            |
| --- | -------- | --------- | ------------------ |
| 1   | {{SEV}}  | {{cat}}   | {{one-line title}} |
| 2   | {{SEV}}  | {{cat}}   | {{one-line title}} |
| 3   | {{SEV}}  | {{cat}}   | {{one-line title}} |
| 4   | {{SEV}}  | {{cat}}   | {{one-line title}} |
| 5   | {{SEV}}  | {{cat}}   | {{one-line title}} |

### Severity counts

| CRITICAL  | HIGH      | MEDIUM    | LOW       | INFO      |
| --------- | --------- | --------- | --------- | --------- |
| {{n}}     | {{n}}     | {{n}}     | {{n}}     | {{n}}     |

---

## Findings

<!--
  Paste the analyst's findings verbatim, ordered CRITICAL → HIGH → MEDIUM → LOW → INFO.
  Each finding follows the block below. Skip severity buckets that have no findings.
  If zero findings total, write: "No findings."
-->

### [CRITICAL] {{short title}}

- **Location:** `{{path/to/file.ext:line}}` _(or `project-wide`)_
- **Category:** {{schema | referential-integrity | migrations | indexing | query-patterns | transactions | data-access-security | orm | backups-retention}}
- **Description:** {{what's wrong, observed in the code}}
- **Impact:** {{what breaks — data loss, corruption, breach, latency — and at what scale}}
- **Resolution:** {{concrete fix steps}}
- **Effort:** {{S | M | L}}
- **Confidence:** {{high | medium | low}}

_(repeat per finding)_

---

## Prioritized Action Plan

Bucketed by when the team should tackle each item. Weighs severity, effort, and blast radius — not just raw severity.

### Do first (this sprint)

_CRITICAL + HIGH items with S/M effort; anything risking data loss, corruption, or a breach._

- [ ] [{{SEV}}] {{title}} — _effort {{S|M|L}}_
- [ ] ...

### Do next (next 30 days)

_HIGH with L effort + MEDIUM items that compound if ignored._

- [ ] [{{SEV}}] {{title}} — _effort {{S|M|L}}_
- [ ] ...

### Backlog / consider

_LOW / INFO / minor inefficiencies / opportunistic fixes._

- [ ] [{{SEV}}] {{title}} — _effort {{S|M|L}}_
- [ ] ...

---

## Methodology & caveats

**Analyst:** `${CLAUDE_PLUGIN_ROOT}/agents/database-auditor.md` (source of truth for the database lens).

**Execution:** one `database-auditor` agent invocation doing read-only codebase exploration (Read / Glob / Grep / Bash). No files were modified, no migrations were run, no live database was accessed.

**Scope skipped:** `node_modules/`, `vendor/`, `dist/`, `build/`, `.next/`, compiled assets, lockfiles, generated code.

**Caveats:**
{{Copy the "Notes & caveats" section from the analyst here — files they couldn't access, sampling decisions, assumptions about data volume, approximate file count analyzed.}}

**Severity legend:**

- `CRITICAL` — data loss, corruption, or breach risk that can happen today. Fix immediately.
- `HIGH` — clear correctness/integrity gap likely to bite under normal operation. Fix this sprint.
- `MEDIUM` — real design smell or inefficiency, not imminent danger. Schedule this quarter.
- `LOW` — minor inefficiency. Fix opportunistically.
- `INFO` — observation, not a defect.
