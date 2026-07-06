<!--
  g14-security-audit report template.
  Placeholders are in {{double-curly}} format. Fill every placeholder.
  Don't remove sections — if the audit came back clean, write "No findings." inside.
  Severity labels (CRITICAL / HIGH / MEDIUM / LOW / INFO) stay in English — they are
  greppable and must be consistent across reports even when prose is in another language.
-->

# Security Audit Report

- **Project:** {{project_name}}
- **Path:** `{{absolute_path}}`
- **Date:** {{YYYY-MM-DD HH:MM}}
- **Auditor:** Claude Code — `audit:g14-security-audit` skill
- **Lens:** Security
- **Scope:** {{files_analyzed}} files · {{loc_approx}} LOC (approx.)

---

## Executive Summary

**Overall rating:** {{healthy | at-risk | critical}} — {{one-sentence justification}}

{{2-4 sentence narrative: what kind of project is this, what is the threat model, what is the overall security posture, and the single most important thing the reader should walk away knowing.}}

### Top findings

Ordered by severity, then by blast radius.

| #   | Severity | Category     | Finding            |
| --- | -------- | ------------ | ------------------ |
| 1   | {{SEV}}  | {{category}} | {{one-line title}} |
| 2   | {{SEV}}  | {{category}} | {{one-line title}} |
| 3   | {{SEV}}  | {{category}} | {{one-line title}} |
| 4   | {{SEV}}  | {{category}} | {{one-line title}} |
| 5   | {{SEV}}  | {{category}} | {{one-line title}} |

### Severity counts

| CRITICAL | HIGH  | MEDIUM | LOW   | INFO  |
| -------- | ----- | ------ | ----- | ----- |
| {{n}}    | {{n}} | {{n}}  | {{n}} | {{n}} |

---

## Findings

<!--
  Paste the analyst's findings ordered CRITICAL -> HIGH -> MEDIUM -> LOW -> INFO.
  Each finding follows the block below. If zero findings in a severity bucket, skip it.
  If zero findings total, write: "No findings."
-->

### [CRITICAL] {{short title}}

- **Location:** `{{path/to/file.ext:line}}` _(or `project-wide`)_
- **Category:** {{injection | auth | authz | secrets | crypto | session | input-validation | dependency | cors/csrf | file-upload | logging | info-disclosure | client-side | infra}}
- **Description:** {{what's wrong, observed in the code}}
- **Impact:** {{attack scenario / data at risk / blast radius}}
- **Resolution:** {{concrete fix steps}}
- **Effort:** {{S | M | L}}
- **Confidence:** {{high | medium | low}}

_(repeat per finding)_

---

## Prioritized Action Plan

Bucketed by when the team should tackle each item. Weighs severity, effort, and blast radius — not just raw severity.

### Do first (this sprint)

_CRITICAL + HIGH items with S/M effort; anything actively exploitable or imminently dangerous._

- [ ] [{{SEV}}] {{title}} — _effort {{S|M|L}}_
- [ ] ...

### Do next (next 30 days)

_HIGH with L effort + MEDIUM items that compound if ignored._

- [ ] [{{SEV}}] {{title}} — _effort {{S|M|L}}_
- [ ] ...

### Backlog / consider

_LOW / INFO / hardening / opportunistic fixes._

- [ ] [{{SEV}}] {{title}} — _effort {{S|M|L}}_
- [ ] ...

---

## Methodology & caveats

**Analyst:** `${CLAUDE_PLUGIN_ROOT}/agents/security-auditor.md` (source of truth for the security lens).

**Execution:** one `security-auditor` agent invocation doing read-only codebase exploration (Read / Glob / Grep / Bash). No target code was modified.

**Scope skipped:** `node_modules/`, `vendor/`, `dist/`, `build/`, `.next/`, compiled assets, lockfiles, generated code.

**Caveats:**
{{Copy the "Notes & caveats" section from the analyst here. Surface files they couldn't access, sampling decisions, or deployment/threat model assumptions so the reader knows the limits of the audit.}}

**Severity legend:**

- `CRITICAL` — directly exploitable now / live data exposure. Fix immediately.
- `HIGH` — exploitable with preconditions or low-privilege attacker. Fix this sprint.
- `MEDIUM` — weakens posture, not a direct exploit path. Schedule this quarter.
- `LOW` — hardening gap / defense-in-depth. Fix opportunistically.
- `INFO` — observation, not a defect.
