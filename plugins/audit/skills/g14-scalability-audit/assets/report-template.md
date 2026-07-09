<!--
  g14-scalability-audit report template.
  Placeholders are in {{double-curly}} format. Fill every placeholder.
  Don't remove sections — if the analyst came back clean, write "No findings." inside.
  Keep severity labels in English (CRITICAL / HIGH / MEDIUM / LOW / INFO) so they're
  greppable and consistent across reports, even when the prose is in another language.
-->

# Scalability Audit Report

- **Project:** {{project_name}}
- **Path:** `{{absolute_path}}`
- **Date:** {{YYYY-MM-DD HH:MM}}
- **Auditor:** Claude Code — `audit:g14-scalability-audit` skill
- **Lens:** Scalability
- **Scope:** {{files_analyzed}} files · {{loc_approx}} LOC (approx.)

---

## Executive Summary

**Overall health:** {{healthy | at-risk | critical}}

{{2–4 sentence narrative: what kind of project is this, what's the big-picture scalability posture, what is the single most important thing the reader should walk away knowing.}}

### Top findings

Ordered by severity, then by blast radius. If the audit found fewer than 3 findings total, include only the rows that exist and drop the rest — don't pad the table.

| #   | Severity | Category  | Finding            |
| --- | -------- | --------- | ------------------ |
| 1   | {{SEV}}  | {{cat}}   | {{one-line title}} |
| 2   | {{SEV}}  | {{cat}}   | {{one-line title}} |
| 3   | {{SEV}}  | {{cat}}   | {{one-line title}} |

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
- **Category:** {{database | caching | concurrency | memory | i/o | infrastructure | multi-tenancy | algorithm | background-jobs | observability}}
- **Description:** {{what's wrong, observed in the code}}
- **Impact:** {{what breaks / at what scale / what's the ceiling}}
- **Resolution:** {{concrete fix steps}}
- **Effort:** {{S | M | L}}
- **Confidence:** {{high | medium | low}}

_(repeat per finding)_

---

## Prioritized Action Plan

Bucketed by when the team should tackle each item. Weighs severity, effort, and blast radius — not just raw severity.

### Do first (this sprint)

_CRITICAL + HIGH items with S/M effort; anything that causes imminent production failure._

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

**Analyst:** `${CLAUDE_PLUGIN_ROOT}/agents/scalability-auditor.md` (source of truth for the scalability lens).

**Execution:** one `scalability-auditor` agent invocation doing read-only codebase exploration (Read / Glob / Grep / Bash). No files were modified.

**Scope skipped:** `node_modules/`, `vendor/`, `dist/`, `build/`, `.next/`, compiled assets, lockfiles, generated code.

**Caveats:**
{{Copy the "Notes & caveats" section from the analyst here — files they couldn't access, sampling decisions, assumptions about load, approximate file count analyzed.}}

**Severity legend:**

- `CRITICAL` — falls over at current or near-term load. Fix immediately.
- `HIGH` — clear bottleneck likely to bite within months. Fix this sprint.
- `MEDIUM` — real ceiling, not imminent. Schedule this quarter.
- `LOW` — minor inefficiency. Fix opportunistically.
- `INFO` — observation, not a defect.
