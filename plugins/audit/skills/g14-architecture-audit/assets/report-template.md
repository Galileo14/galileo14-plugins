<!--
  g14-architecture-audit report template — single-lens.
  Placeholders are in {{double-curly}} format. Fill every placeholder.
  Don't remove sections — if the analyst came back clean, write "No findings." inside.
  Keep severity labels in English (CRITICAL / HIGH / MEDIUM / LOW / INFO) — they're
  greppable and consistent across reports, even when the prose is in another language.
-->

# Architecture Audit Report

- **Project:** {{project_name}}
- **Path:** `{{absolute_path}}`
- **Date:** {{YYYY-MM-DD HH:MM}}
- **Auditor:** Claude Code — `audit:g14-architecture-audit` skill
- **Lens:** Architecture
- **Scope:** {{files_analyzed}} files · {{loc_approx}} LOC (approx.)

---

## Executive Summary

**Overall health:** {{healthy | at-risk | critical}}

{{2–4 sentence narrative: what kind of project is this, what's the architectural posture, and the single most important thing the reader should walk away knowing.}}

### Top findings

Ordered by severity, then blast radius.

| #   | Severity | Category | Finding            |
| --- | -------- | -------- | ------------------ |
| 1   | {{SEV}}  | {{cat}}  | {{one-line title}} |
| 2   | {{SEV}}  | {{cat}}  | {{one-line title}} |
| 3   | {{SEV}}  | {{cat}}  | {{one-line title}} |

### Severity counts

| CRITICAL  | HIGH      | MEDIUM    | LOW       | INFO      |
| --------- | --------- | --------- | --------- | --------- |
| {{n}}     | {{n}}     | {{n}}     | {{n}}     | {{n}}     |

---

## Architecture Analysis

**Rating:** {{healthy | at-risk | critical}} — {{one-sentence justification}}

### Summary

{{2–4 sentence overview from the architecture analyst}}

### Findings

<!--
  Paste the architecture analyst's findings verbatim, ordered CRITICAL → HIGH → MEDIUM → LOW → INFO.
  Each finding follows the block below. If zero findings in a severity, skip that bucket.
  If zero findings total, write: "No findings."
-->

#### [CRITICAL] {{short title}}

- **Location:** `{{path/to/file.ext:line}}` _(or `project-wide`)_
- **Category:** {{coupling | cohesion | layering | duplication | dead-code | god-object | abstraction | dependency-direction | testability | naming | documentation | consistency | tech-debt | structure}}
- **Description:** {{what's wrong, observed in the code}}
- **Impact:** {{maintainability cost / onboarding friction / future velocity hit / change-risk}}
- **Resolution:** {{concrete fix steps, phased if multi-sprint}}
- **Effort:** {{S | M | L}}
- **Confidence:** {{high | medium | low}}

_(repeat per finding)_

---

## Prioritized Action Plan

Bucketed by when the team should tackle each item. Weighs severity, effort, and blast radius — not just raw severity.

### Do first (this sprint)

_CRITICAL + HIGH items with S/M effort; anything actively blocking safe changes._

- [ ] [{{SEV}}] {{title}} — _effort {{S|M|L}}_
- [ ] ...

### Do next (next 30 days)

_HIGH with L effort + MEDIUM items that compound if ignored._

- [ ] [{{SEV}}] {{title}} — _effort {{S|M|L}}_
- [ ] ...

### Backlog / consider

_LOW / INFO / stylistic / opportunistic fixes._

- [ ] [{{SEV}}] {{title}} — _effort {{S|M|L}}_
- [ ] ...

---

## Methodology & caveats

**Analyst:** `${CLAUDE_PLUGIN_ROOT}/agents/architecture-auditor.md` (source of truth for the architecture lens).

**Execution:** one `architecture-auditor` agent invocation doing read-only codebase exploration (Read / Glob / Grep / Bash). Findings consolidated by the orchestrating Claude Code session.

**Scope skipped:** `node_modules/`, `vendor/`, `dist/`, `build/`, `.next/`, compiled assets, lockfiles, generated code.

**Caveats:**
{{Copy the "Notes & caveats" section from the analyst here. Surface any files they couldn't access, sampling decisions, or assumptions they made.}}

**Severity legend:**

- `CRITICAL` — active blocker to velocity or correctness. Fix immediately.
- `HIGH` — significant drag; will compound. Fix this sprint.
- `MEDIUM` — real debt, not urgent. Schedule this quarter.
- `LOW` — minor or stylistic. Fix opportunistically.
- `INFO` — observation, not a defect.
