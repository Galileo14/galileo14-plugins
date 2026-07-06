# Rubric: Calibration (respects "only add what you need")

An audit that flags every missing control as a defect is wrong. It contradicts
the framework's cardinal rule that a skill earns scaffolding one observed failure
at a time. This rubric checks that the audit judged *need*, not mere presence.

So this rubric judges the **correctness of the need-judgement and severity**.
It does not judge coverage (that's completeness) or evidence (that's grounding).

Grade the report as a **global** judgement. PASS only if ALL hold:

- **No skipped control is flagged as a defect without a NEEDED argument.** For
  every control marked as a GAP, the report explicitly argues why that control
  is needed for THIS skill (tying to the skill's nature or a decision-table
  trigger). A control absent because the skill doesn't need it is recorded as a
  ✅ correct skip, not a ❌.
- **Over-engineering is judged too, and honestly.** If the skill carries a
  control it doesn't need (present + NOT needed), the report flags it ⚠️, but
  only when the control is demonstrably unused for a needed purpose. Otherwise it
  belongs in "worth checking", not in the defect list. The rule cuts both ways.
- **Severity matches the canonical definitions** in `references/audit-rubric.md`.
  Use P1 only for genuine gaps in NEEDED controls, broken runs, a late failure
  from a missing dependency, or a secret or grounding failure. Check the opposite
  error too: a best-practice item with its own P1 severity (say a secret leak)
  must not be deflated to P2. The item's own bracketed severity wins.
- **Ambiguous "needed" is handled honestly.** Where need is genuinely unclear,
  the report says so and recommends the diagnostic (run it a few times, watch
  what drifts) instead of asserting a gap.

Return `{ id: "calibration", passed, evidence }`. Quote the specific report lines
that pass or fail each clause. FAIL if any control is marked a gap purely because
the folder is absent, with no need argument, or if a severity contradicts the
canonical definitions.
