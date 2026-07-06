# Rubric: Actionability (every fix is concrete)

A grounded, calibrated, complete report still fails the user if its
recommendations are vague ("improve the description", "add tests", "make it
faster"). This rubric checks that each finding tells the user exactly what to do.

Grade **per finding**: every row in "Prioritised improvements" and every
P1/P2 item in the per-control and cross-cutting sections. PASS a finding only if
its fix is **specific and executable**:

- It names the concrete target: a file, a section, a frontmatter field, a
  `SKILL.md` step, an agent's `model:` value, a folder/naming scheme, and so on.
- It states the actual change to make (the value, the wording direction, the
  artifact to add), not just a restatement of the problem.
- For the user-requested improvement types, the fix is concrete: for example "set
  `model: haiku` on `agents/scraper.md`" (not "use cheaper models"); "add
  `tests/freshness-test.md` with a 7-day window rule" (not "add more tests");
  "add a Step 1 preflight that checks the X connector and aborts if absent" (not
  "add a preflight").

FAIL any fix that is a generic verb plus noun with no target or value: "improve
X", "enhance Y", "consider tests", "optimise performance", "tighten instructions".

**Also FAIL any recommendation that is concrete but technically wrong-headed.**
Specificity is worthless if the advice is bad. In particular, FAIL:

- recommending Haiku (or any cheap model or low effort) for a grader, judge, or
  other genuine judgement step;
- recommending a dynamic Workflow for a small, bounded fan-out (a handful of
  units), where plain parallel dispatch is correct;
- a wall-clock or runtime estimate not derived from the step count and fan-out;
- recommending a control the skill demonstrably does not need (which contradicts
  the cardinal rule), or removing one it does need.

For each finding return `{ id, passed, evidence }`, quoting the fix text and
stating why it is or isn't executable AND sound. When the recommendation is
"none, correct as is", that PASSES (nothing to action).
