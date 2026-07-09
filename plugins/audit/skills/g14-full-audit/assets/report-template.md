<!--
  g14-full-audit report template — combined, multi-lens.
  Placeholders are in {{double-curly}} format. Fill every placeholder.
  Only include a "## <Lens>" section for lenses that were actually run —
  do not write placeholder text for skipped lenses.
  Keep severity labels in English (CRITICAL / HIGH / MEDIUM / LOW / INFO) so they're
  greppable and consistent across reports, even when the prose is in another language.
-->

# Full Audit Report

- **Project:** {{project_name}}
- **Path:** `{{absolute_path}}`
- **Date:** {{YYYY-MM-DD HH:MM}}
- **Auditor:** Claude Code — `audit:g14-full-audit` skill
- **Lenses run:** {{comma-separated list, e.g. Security, Scalability, Database}}
- **Scope:** {{files_analyzed}} files · {{loc_approx}} LOC (approx.)

---

## Executive Summary

**Overall health:** {{healthy | at-risk | critical}} _(worst rating among lenses run)_

{{3–6 sentence narrative: what kind of project this is, the single biggest risk across all lenses, one sentence per lens run on its posture.}}

### Cross-lens top findings

Pooled from every lens run, ordered by severity then blast radius.

| #   | Severity | Lens        | Category    | Finding            |
| --- | -------- | ----------- | ----------- | ------------------ |
| 1   | {{SEV}}  | {{lens}}    | {{cat}}     | {{one-line title}} |
| 2   | {{SEV}}  | {{lens}}    | {{cat}}     | {{one-line title}} |
| 3   | {{SEV}}  | {{lens}}    | {{cat}}     | {{one-line title}} |
| 4   | {{SEV}}  | {{lens}}    | {{cat}}     | {{one-line title}} |
| 5   | {{SEV}}  | {{lens}}    | {{cat}}     | {{one-line title}} |

### Combined severity counts

| CRITICAL  | HIGH      | MEDIUM    | LOW       | INFO      |
| --------- | --------- | --------- | --------- | --------- |
| {{n}}     | {{n}}     | {{n}}     | {{n}}     | {{n}}     |

### Per-lens breakdown

| Lens         | Rating                       | CRITICAL | HIGH  | MEDIUM | LOW   | INFO  |
| ------------ | ----------------------------- | -------- | ----- | ------ | ----- | ----- |
| {{lens}}     | {{healthy \| at-risk \| critical}} | {{n}}    | {{n}} | {{n}}  | {{n}} | {{n}} |

_(one row per lens run — omit rows for lenses not run)_

---

<!--
  One section per lens run. Delete/omit the sections for lenses that weren't run.
  Paste each lens agent's findings verbatim, preserving CRITICAL → HIGH → MEDIUM → LOW → INFO ordering.
  Each finding follows the block below. If a lens ran clean, write "No findings." under its heading.
-->

## Security

**Rating:** {{healthy | at-risk | critical}} — {{one-sentence justification from the agent's Overall rating}}

### [CRITICAL] {{short title}}

- **Location:** `{{path/to/file.ext:line}}` _(or `project-wide`)_
- **Category:** {{injection | auth | authz | api | business-logic | secrets | crypto | session | input-validation | dependency | cors/csrf | file-upload | logging | info-disclosure | client-side | infra}}
- **Description:** {{what's wrong, observed in the code}}
- **Impact:** {{attack category, data at risk, blast radius}}
- **Resolution:** {{concrete fix steps}}
- **Effort:** {{S | M | L}}
- **Confidence:** {{high | medium | low}}

_(repeat per finding, ordered CRITICAL → HIGH → MEDIUM → LOW → INFO)_

## Scalability

**Rating:** {{healthy | at-risk | critical}} — {{one-sentence justification}}

### [CRITICAL] {{short title}}

- **Location:** `{{path/to/file.ext:line}}` _(or `project-wide`)_
- **Category:** {{database | caching | concurrency | memory | i/o | infrastructure | multi-tenancy | algorithm | background-jobs | observability}}
- **Description:** {{what's wrong, observed in the code}}
- **Impact:** {{concrete failure mode, at what scale / load}}
- **Resolution:** {{concrete fix steps}}
- **Effort:** {{S | M | L}}
- **Confidence:** {{high | medium | low}}

_(repeat per finding)_

## Architecture

**Rating:** {{healthy | at-risk | critical}} — {{one-sentence justification}}

### [CRITICAL] {{short title}}

- **Location:** `{{path/to/file.ext:line}}` _(or `project-wide`)_
- **Category:** {{coupling | cohesion | layering | duplication | dead-code | god-object | abstraction | dependency-direction | testability | naming | documentation | consistency | tech-debt | structure}}
- **Description:** {{what's wrong, observed in the code}}
- **Impact:** {{maintainability cost, onboarding friction, velocity hit, change-risk}}
- **Resolution:** {{concrete fix steps, phased if multi-sprint}}
- **Effort:** {{S | M | L}}
- **Confidence:** {{high | medium | low}}

_(repeat per finding)_

## Clean Code

**Rating:** {{healthy | at-risk | critical}} — {{one-sentence justification}}

### [CRITICAL] {{short title}}

- **Location:** `{{path/to/file.ext:line}}` _(or `project-wide`)_
- **Category:** {{naming | function-length | nesting | duplication | comment-hygiene | dead-code | magic-constants | god-object | domain-modeling | abstraction-leak | style-consistency | complexity-without-tests}}
- **Description:** {{what was observed, with exact file:line}}
- **Why it bites:** {{concrete maintenance cost}}
- **Fix:** {{concrete refactor steps}}
- **Effort:** {{S | M | L}}
- **Confidence:** {{high | medium | low}}

_(repeat per finding)_

## Database

**Rating:** {{healthy | at-risk | critical}} — {{one-sentence justification}}

### [CRITICAL] {{short title}}

- **Location:** `{{path/to/file.ext:line}}` _(or `project-wide`)_
- **Category:** {{schema | referential-integrity | migrations | indexing | query-patterns | transactions | data-access-security | orm | backups-retention}}
- **Description:** {{what's wrong, observed in the code}}
- **Impact:** {{concrete failure mode — data loss, corruption, breach, latency}}
- **Resolution:** {{concrete fix steps}}
- **Effort:** {{S | M | L}}
- **Confidence:** {{high | medium | low}}

_(repeat per finding)_

---

## Prioritized Action Plan

One combined plan across every lens run. Bucketed by when the team should tackle each item. Weighs severity, effort, and blast radius — not just raw severity.

### Do first (this sprint)

_CRITICAL + HIGH items with S/M effort; anything actively dangerous or exploitable across any lens._

- [ ] [{{SEV}}] {{title}} — {{lens}}, effort {{S|M|L}}
- [ ] ...

### Do next (next 30 days)

_HIGH with L effort + MEDIUM items that compound if ignored._

- [ ] [{{SEV}}] {{title}} — {{lens}}, effort {{S|M|L}}
- [ ] ...

### Backlog / consider

_LOW / INFO / opportunistic fixes across every lens run._

- [ ] [{{SEV}}] {{title}} — {{lens}}, effort {{S|M|L}}
- [ ] ...

---

## Methodology & caveats

**Lenses run:** {{comma-separated list}}. **Lenses not run:** {{comma-separated list, or "none"}} — {{user's choice, not a failure}}.

**Analysts:** one agent invocation per lens run, launched in parallel — `security-auditor`, `scalability-auditor`, `architecture-auditor`, `clean-code-auditor`, `database-auditor` at `${CLAUDE_PLUGIN_ROOT}/agents/` (source of truth for each lens). All read-only codebase exploration (Read / Glob / Grep / Bash). No target files were modified.

**Scope skipped:** `node_modules/`, `vendor/`, `dist/`, `build/`, `.next/`, compiled assets, lockfiles, generated code, minified bundles.

**Per-lens caveats:**
{{Copy each ran agent's own "Notes & caveats" section here, one block per lens, labeled with the lens name.}}

**Severity legend:**

- `CRITICAL` — stop-ship across any lens: exploitable now, falls over at current load, active blocker to safe change, or risks data loss/corruption/breach today.
- `HIGH` — clear, near-term risk in at least one lens. Fix this sprint.
- `MEDIUM` — real issue, not urgent. Schedule this quarter.
- `LOW` — minor or opportunistic. Fix when convenient.
- `INFO` — observation, not a defect.
