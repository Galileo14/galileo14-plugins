<!--
  g14-clean-code-audit report template.
  Placeholders are in {{double-curly}} format. Fill every placeholder.
  Don't remove sections — if the analyst came back clean, write "No findings." inside.
  Keep severity labels in English (CRITICAL / HIGH / MEDIUM / LOW / INFO) — they're
  greppable and consistent across reports, even when prose is in another language.
-->

# Clean-Code Audit Report

- **Project:** {{project_name}}
- **Path:** `{{absolute_path}}`
- **Date:** {{YYYY-MM-DD HH:MM}}
- **Auditor:** Claude Code — `audit:g14-clean-code-audit` skill
- **Lens:** Clean-Code (naming · structure · duplication · comment hygiene · dead code · magic constants · god objects · abstraction leaks · style consistency · complexity coverage)
- **Scope:** {{files_analyzed}} files analyzed · {{loc_approx}} LOC (approx.)

---

## Executive Summary

**Overall rating:** {{healthy | at-risk | critical}}

{{2–4 sentence narrative: language/stack, craftsmanship posture, single most important takeaway for the reader.}}

### Top findings

Ordered by severity, then by blast radius (how many people or flows are affected).

| #   | Severity | Category           | Finding            |
| --- | -------- | ------------------ | ------------------ |
| 1   | {{SEV}}  | {{category}}       | {{one-line title}} |
| 2   | {{SEV}}  | {{category}}       | {{one-line title}} |
| 3   | {{SEV}}  | {{category}}       | {{one-line title}} |
| 4   | {{SEV}}  | {{category}}       | {{one-line title}} |
| 5   | {{SEV}}  | {{category}}       | {{one-line title}} |

### Severity counts

| CRITICAL  | HIGH      | MEDIUM    | LOW       | INFO      |
| --------- | --------- | --------- | --------- | --------- |
| {{n}}     | {{n}}     | {{n}}     | {{n}}     | {{n}}     |

---

## Findings

<!--
  Paste the analyst's findings verbatim, ordered CRITICAL → HIGH → MEDIUM → LOW → INFO.
  Each finding follows the block below. Skip severity buckets that have zero findings.
  If zero findings total, write: "No findings."
-->

### [CRITICAL] {{short title}}

- **Location:** `{{path/to/file.ext:line}}` _(or `project-wide`)_
- **Category:** {{naming | function-length | nesting | duplication | comment-hygiene | dead-code | magic-constants | god-object | abstraction-leak | style-consistency | complexity-without-tests}}
- **Description:** {{what was observed, with exact file:line}}
- **Why it bites:** {{concrete maintenance cost — what goes wrong, how often, who gets hurt}}
- **Fix:** {{concrete refactor steps}}
- **Effort:** {{S | M | L}}
- **Confidence:** {{high | medium | low}}

_(repeat per finding, ordered CRITICAL → HIGH → MEDIUM → LOW → INFO)_

---

## Prioritized Action Plan

Bucketed by urgency. Weighs severity, effort, and blast radius — not just raw severity.

### Do first (this sprint)

_CRITICAL items; HIGH items with S/M effort that block safe daily work._

- [ ] [{{SEV}}] {{title}} — `{{file:line}}`, effort {{S|M|L}}
- [ ] ...

### Do next (next 30 days)

_HIGH with L effort + MEDIUM items that compound the longer they sit._

- [ ] [{{SEV}}] {{title}} — `{{file:line}}`, effort {{S|M|L}}
- [ ] ...

### Backlog / consider

_LOW / INFO / purely opportunistic fixes._

- [ ] [{{SEV}}] {{title}} — `{{file:line}}`, effort {{S|M|L}}
- [ ] ...

---

## Methodology & caveats

**Analyst:** one `clean-code-auditor` agent invocation (source of truth at `${CLAUDE_PLUGIN_ROOT}/agents/clean-code-auditor.md`). Read-only exploration (Read / Glob / Grep / Bash) — no target files were modified.

**Scope skipped:** `node_modules/`, `vendor/`, `dist/`, `build/`, `.next/`, `__pycache__/`, `.git/`, lockfiles, generated code, minified bundles, test fixtures with synthetic data.

**Sampling notes:**
{{Copy the "Notes" section from the analyst here. Include file count analyzed, git-log hotspot analysis if run, and any areas the analyst couldn't fully inspect.}}

**Severity legend:**

- `CRITICAL` — active maintenance blocker; the code cannot be safely changed without high risk. Fix now.
- `HIGH` — significant drag; this will keep biting. Fix this sprint.
- `MEDIUM` — real debt, contained. Schedule for next cleanup pass.
- `LOW` — minor or opportunistic. Fix when you're already in the file.
- `INFO` — observation only, not a defect.

**Out of scope for this audit:** correctness bugs, security vulnerabilities, performance bottlenecks, high-level module coupling and dependency direction. Use `audit:g14-security-audit`, `audit:g14-scalability-audit`, or `audit:g14-architecture-audit` for those lenses.
