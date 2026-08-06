# Rubric: Completeness (all controls + cross-cutting covered)

An audit that silently skips a control or a whole area gives false confidence.
This rubric checks **coverage** of the report, not the correctness of its
judgements (that's calibration's job).

Grade as a **global** judgement. PASS only if ALL hold:

- **All five controls are assessed** in the scorecard AND have a per-control
  findings entry, none silently omitted. Each has a present/wired status, a
  needed judgement, and a verdict.
- **Every cross-cutting area is addressed** (a finding, "✓ fine", or "N/A
  (reason)", never silently dropped): triggering/description; authoring;
  preflight/fail-fast; error handling (retries/fallbacks/stop-steps); process
  artifacts (scripts not generated on the fly); output storage; intermediate
  state/checkpointing; packaging. (Security, parallelisation, and cost are NOT in
  this list; they live in their dedicated sections, checked below. FAIL if the
  Cross-cutting findings section repeats them.)
- **Every improvement type the skill is meant to surface is explicitly
  considered.** Each is recommended with specifics or marked already-fine or N/A:
  cheaper/faster models for mechanical subagents; more/better tests; preflight
  check; pre-stored scripts; runtime and parallelisation (incl. dynamic Workflow
  for large fan-outs); structured output destination; intermediate-state
  checkpointing; error handling.
- **Hard cross-check against the scan, so no obvious win is missed** (note the
  scan nests signal flags under `signals.*`; `summary.*` and
  `broken_referenced_paths` are top-level):
  - If `scan_json.summary.agents_missing_model` is non-empty, or any agent in
    `scan_json.agents` does mechanical work on sonnet/opus, the report MUST
    contain a cheaper-model recommendation naming that agent. FAIL if the scan
    shows such an agent and the report omits it or says models are fine.
  - If `scan_json.summary.agents_missing_effort` is non-empty, or any agent does
    mechanical work at `effort: high`, the report MUST address `effort` matching.
  - If `scan_json.summary.likely_missing_subagent_opportunity` is true
    (independent/repeated work described with no sign of parallel dispatch), the
    report MUST address it under Control 4, either recommending the subagent to
    add or explaining why the work isn't parallelisable or is already delegated.
  - If `scan_json.signals.writes_scripts_on_the_fly` is true, the report MUST
    flag it.
  - If `scan_json.broken_referenced_paths` is non-empty, the report MUST flag
    each as broken wiring.
  - If `scan_json.signals.step_count` is high and
    `scan_json.signals.mentions_state_checkpoint` is false, the report MUST at
    least consider checkpointing.
  - If `scan_json.signals.step_count` is high and
    `scan_json.signals.mentions_error_handling` is false, the report MUST at
    least consider error handling.
- **The report body language matches the user's or request language** (FAIL if it
  defaulted to English when the request was in another language).
- **The report is clear without losing depth.** The Verdict reads as a
  plain-language bottom line that names the top fix, with no unexplained jargon.
  Each P1/P2 finding pairs a plain statement of what's wrong and why with its full
  technical specifics (file:line, scan field, or exact fix); neither is dropped.
  FAIL if the Verdict is impenetrable, or if findings are either vague (no
  specifics) or raw specifics with no plain explanation.
- **The report reads human, not AI.** FAIL on obvious AI tells: any em or en
  dash, signposting ("Let's dive in"), rule-of-three padding, "-ing" fake-depth
  tails, significance inflation, or copula avoidance ("serves as" instead of
  "is"). Headings are sentence case; quotes are straight.
- **The deliverable matches the template** (`assets/report-template.md`): verdict,
  profile (incl. runtime and length lines), scorecard, per-control findings,
  cross-cutting, prioritised improvements, the three dedicated sections
  (Potential security vulnerabilities, Potential parallelisation opportunities,
  Potential cost-saving opportunities), strengths, and grounding note, all
  present, with slots filled (no stray `{{SLOT}}` left). One exception: the
  `{{GRADER_SUMMARY_JSON}}` slot is expected to be empty at grading time, since
  the grader produces that JSON, so do NOT fail on that one slot. The
  orchestrator fills it after grading.
- **The three dedicated sections are each resolved**, not left blank: every one
  is either an explained list of real candidates or an explicit "None" with a
  one-line reason. FAIL if any is empty or still holds template placeholder text.
  Each owns its topic and is the only narrative home for it:
  - **Potential security vulnerabilities** owns secrets, least-privilege/tool
    over-grant, dangerous defaults, prompt-injection exposure, the bash
    side-door, and MCP/connector vetting.
  - **Potential parallelisation opportunities** owns fan-out / missing-subagent
    candidates and dynamic-Workflow recommendations.
  - **Potential cost-saving opportunities** owns model selection (Haiku), effort,
    batching, context slicing, clean-result return, model-tiering, token/context
    hygiene, cache ordering, /compact, memory reuse, /loop cost, and external API
    usage.
  FAIL if any of these topics is instead reported under Cross-cutting findings
  (that would be duplication).
- **A conformance band and P1/P2/P3 counts are stated.**

Return `{ id: "completeness", passed, evidence }`. List any missing control,
area, improvement type, scan-cross-check, or template section as failure evidence.
