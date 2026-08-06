<!-- Writing style: this report is long and dense, so keep it easy to read in
     one pass without dumbing it down. Verdict = plain-language bottom line.
     Each finding = a plain sentence, then the full technical specifics
     (file:line, scan field, exact fix). Clear, not simplified.
     Sound human, not AI: vary sentence length; plain is/are/has; no em/en
     dashes; no signposting, rule-of-three padding, "-ing" fake-depth, or
     significance inflation; sentence-case headings; straight quotes. Neutral
     technical voice, no injected personality. -->
# Skill audit: {{SKILL_NAME}}

**Target:** `{{SKILL_PATH}}`
**Audited:** {{DATE}} · by g14-skill-audit
**Conformance:** {{BAND}} ({{P1_COUNT}} gap(s), {{P2_COUNT}} correctness issue(s), {{P3_COUNT}} polish item(s))

## Verdict

{{ONE_PARAGRAPH_VERDICT. The plain-language bottom line: in 3 to 5 sentences a
busy reader gets on one pass, say whether the skill is sound, the single most
important thing to fix, and why. No jargon here; the detail comes below.}}

## Skill profile

What it does: {{WHAT_IT_DOES}}
Nature (drives which controls are needed):
- Input variability: {{INPUT_NATURE}}
- Process: {{PROCESS_NATURE}}  (fixed method vs novel each run)
- Output: {{OUTPUT_NATURE}}  (fixed shape vs adaptive)
- Parallelisable work: {{PARALLEL_NATURE}}
- Correctness risk: {{CORRECTNESS_NATURE}}  (claims to verify? human in loop?)
- Runtime and scaling: {{RUNTIME_ESTIMATE}}  (wall-clock estimate; serial vs parallel; large fan-out?)
- Length and resumability: {{LENGTH_NATURE}}  (step count; needs checkpointing?)

## Controls scorecard

| Control | Present + wired | Needed | Verdict |
|---------|-----------------|--------|---------|
| 1. Input (`references/`)  | {{C1_PRESENT}} | {{C1_NEEDED}} | {{C1_VERDICT}} |
| 2. Process (`scripts/`)   | {{C2_PRESENT}} | {{C2_NEEDED}} | {{C2_VERDICT}} |
| 3. Output (`assets/`)     | {{C3_PRESENT}} | {{C3_NEEDED}} | {{C3_VERDICT}} |
| 4. Speed (`agents/`)      | {{C4_PRESENT}} | {{C4_NEEDED}} | {{C4_VERDICT}} |
| 5. Tests (`tests/`)       | {{C5_PRESENT}} | {{C5_NEEDED}} | {{C5_VERDICT}} |

Verdict legend: ✅ correct · ❌ GAP (needed but absent/unwired) · ⚠️ over-engineered · 🔧 present-but-weak
(A control present but serving a *different* control's purpose, for example an
`agents/` folder holding a grader for Tests rather than a Speed worker, is ✅ with
a one-line parenthetical, not a gap.)

## Per-control findings

<!-- Repeat this block for each control 1 to 5, in order. -->
### Control {{N}}: {{CONTROL_NAME}}
- **Status:** {{QUADRANT}}  (use exactly one: PRESENT+WIRED+NEEDED · ABSENT+NEEDED → GAP · PRESENT+NOT-NEEDED → OVER-ENGINEERED · ABSENT+NOT-NEEDED → CORRECT SKIP · ORPHAN (present, unwired); it must match the scorecard row)
- **Evidence:** {{EVIDENCE: file:line, scan field, or quoted SKILL.md line}}
- **Needed because / Skip is correct because:** {{REQUIRED whenever Status is a GAP or a CORRECT SKIP. Argue from the skill's nature or a decision-table trigger. A GAP with no "needed because" is not allowed.}}
- **Assessment:** {{If present+needed: how well is it done? If absent: gap vs justified skip, per the line above.}}
- **Recommendation:** {{Concrete, specific next action (name the file/edit/value), or "none, correct as is".}}

## Cross-cutting findings

<!-- Address each area. Use "✓ fine" or "N/A (why)" if there's no finding; do
     not silently drop an area. Cite evidence for every finding.
     Do NOT cover security, parallelisation, or cost here: they each have their
     own dedicated section below (security vulnerabilities, parallelisation
     opportunities, cost-saving opportunities). This list is the remaining areas
     only, so nothing is reported twice. -->
- **Triggering / description:** {{...}}
- **Authoring (instructions, WHY, failure modes, magic values):** {{...}}
- **Preflight / fail-fast (verifies dependencies as an early step):** {{...}}
- **Error handling (retries / fallbacks / stop-steps):** {{...}}
- **Process artifacts (scripts pre-stored, not generated on the fly):** {{...}}
- **Output storage (deterministic destination + naming, or DB):** {{...}}
- **Intermediate state / checkpointing (for long skills):** {{...}}
- **Packaging (plugin/routine):** {{...}}

## Prioritised improvements

| # | Priority | Area | Finding | Concrete fix |
|---|----------|------|---------|--------------|
| 1 | P1 | {{...}} | {{...}} | {{...}} |
| 2 | P2 | {{...}} | {{...}} | {{...}} |
| 3 | P3 | {{...}} | {{...}} | {{...}} |

Priority key: **P1** = a NEEDED control is a gap, or a run would break or leak; fix
first. **P2** = a present control done weakly, or a real best-practice violation.
**P3** = polish.

## Potential security vulnerabilities

<!-- Security risks in the skill itself. One entry per risk, with where it is and
     the fix. If none found, say "None found" in one line. Genuine leaks/dangerous
     defaults are P1 and also belong in the prioritised table above. -->
- **{{RISK}}:** {{where it is, e.g. "SKILL.md:42 embeds an API key"}}.
  - Fix: {{the specific change}}.

<!-- Things to check for: secrets (API keys, tokens, secret file contents) in any
     skill file; over-granted agent tools (a read-only worker with Write/Edit/Bash,
     or blank tools = all tools); dangerous defaults (delete/overwrite outside a
     boundary with no confirmation); prompt-injection exposure (reads untrusted
     web/user content and may follow embedded instructions); the bash side-door
     (blocks Read of a secret file but allows Bash cat/grep of it); unvetted
     MCP/connector dependencies. -->

## Potential parallelisation opportunities

<!-- Forward-looking: work that could move onto subagents to run in parallel,
     even if it works today. One entry per opportunity. If there is genuinely
     nothing to parallelise (work is inherently sequential, or already fanned
     out), say so in one line and stop. -->
- **{{WORK / STEP}}:** {{why it's independent or repeated, e.g. "Step 3 scrapes each source one after another"}}.
  - Becomes: {{the subagent to add, e.g. "a per-source scraper subagent"}}.
  - Dispatch: {{how to fan it out, e.g. "one per source, all in parallel"; for a large or unbounded fan-out, recommend a dynamic Workflow instead}}.
  - Benefit: {{faster wall-clock and cleaner orchestrator context; rough scale if known}}.

## Potential cost-saving opportunities

<!-- Forward-looking: changes that cut token usage or external API usage without
     losing quality. Cover both buckets below. If already lean, say so in one
     line. -->
Token / compute:
- {{the change}}: {{mechanism and rough benefit}}. Candidates: pin a mechanical subagent to `model: haiku`; lower `effort` for rote work; batch many tiny units per subagent; pass only the relevant context slice; have workers return only clean results; trim a bloated SKILL.md; cache-friendly read ordering; a cheaper model/effort on a `/loop` or routine repeated path.

External API usage:
- {{the change}}: {{mechanism and rough benefit}}. Candidates: cache or memoise API/MCP responses; dedupe repeated calls; batch requests; fetch incrementally (only changed data); don't re-fetch the same resource across steps; respect rate limits.

## What the skill does well

- {{STRENGTH_1}}
- {{STRENGTH_2}}

## Grounding

All findings above are traced to evidence in the target skill's files (scan
output plus quoted lines). Verified by fresh-context graders before delivery.
Paste their actual summary JSON here, not a free-text claim:

```json
{{GRADER_SUMMARY_JSON}}
```
(per rubric: grounding, calibration, completeness, actionability; passed/failed/total)
