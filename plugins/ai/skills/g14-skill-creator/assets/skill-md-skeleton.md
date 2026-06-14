---
name: {{skill-name}}
description: {{One or two sentences. Say WHAT the skill does AND the concrete
  contexts/phrases that should trigger it. Be pushy — Claude tends to
  under-trigger. List real phrases a user would type, file types, and adjacent
  situations where the skill should win. Avoid vague descriptions.}}
---

# {{Skill Title}}

## What this does

{{One concrete sentence on the capability this skill gives Claude.}}

## When to use it

{{Triggering and scope detail — when this applies and when it doesn't. Keep all
"when to use" information here and in the description, never buried in steps.}}

## Workflow

{{The plain instructions. Write in the imperative. Explain the WHY behind each
step — a smart model with reasons outperforms one following rote rules. Start
here with zero controls; this skeleton has no references/, scripts/, assets/,
agents/, or tests/ yet.}}

### Step 1 — {{...}}

### Step 2 — {{...}}

## Output format

{{If the deliverable has a fixed shape, show the exact template here. Once this
section grows or the layout must be byte-stable, that's the signal to promote it
into an assets/ template — Control 3.}}

<!--
  CONTROL WIRING — add these sections only as Step 3's diagnosis justifies them.
  Each control is dead until SKILL.md explicitly references its folder.

  Control 1 (Input):   "Read every file in references/sources/. Use ONLY these."
  Control 2 (Process): "Run: python scripts/<name>.py ..."
  Control 3 (Output):  "Load assets/<template>. Fill every {{SLOT}}. Don't redesign."
  Control 4 (Speed):   "Dispatch one subagent per <unit>, all in parallel."
  Control 5 (Tests):   "For each tests/<rubric>.md, dispatch a fresh grader subagent."

  See references/five-controls.md for full build instructions.
-->
