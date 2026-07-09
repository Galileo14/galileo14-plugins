# Rubric: Grounding (no fabricated findings)

The single most damaging failure of an audit is inventing a defect the skill
doesn't have, or citing a file or line that doesn't exist. This rubric verifies
every claim in the audit report traces to real evidence in the target skill.

Grade **per finding**: every row in "Prioritised improvements" and every bullet
in "Per-control findings" and "Cross-cutting findings". PASS a finding only if:

- Its evidence points to something that **actually exists** in the target skill:
  a quoted line is present verbatim, a `file:line` resolves, or a named scan
  field has the stated value. Open the file and confirm.
- The defect described is **real**. Re-read the cited location and verify the
  problem is actually there and you didn't misread it.
- Any claim that a control is a GAP cites evidence that the control is
  genuinely absent or unwired, and that evidence checks out against the scan.
  Where the finding also argues the control is NEEDED, the evidence cited
  *inside* that argument is real (whether a NEEDED argument was made at all is
  calibration's check, not this one: don't fail a finding here for missing
  one).
- No referenced path, agent name, model value, or quoted text is fabricated.

For each finding return `{ id, passed, evidence }`, where `evidence` quotes what
you found (or didn't find) at the cited location. FAIL with the specific mismatch
if the cited evidence is absent or distorted. If you cannot locate the cited
evidence at all, FAIL. Don't give it the benefit of the doubt.

Also flag as failures any finding with vague evidence ("looks wrong", "seems
off") that cannot be checked against the files.
