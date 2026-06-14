# Decision table — which controls does this skill need?

Use this in Step 3 of the workflow. Start the skill at **zero controls**. For
each row below, ask the user: "does this failure apply to the skill we're
building?" Add a control only when the answer is yes. Adding scaffolding a skill
doesn't need just makes it brittle and slow.

| If you notice this… | Add this control | But skip it when… |
|---|---|---|
| Sources or facts vary between runs, or come from places you don't trust | **1 — Input** (`references/`) | The skill should explore freely — open-ended research, discovery — or the input is the user's own uploaded file (already pinned) |
| Claude solves the same task a different way each run; tokens burned re-reasoning the "how" | **2 — Process** (`scripts/`) | The task is genuinely novel each run, or inputs are hostile/unstable and need live improvising |
| The deliverable's structure, headings or format drift between runs | **3 — Output** (`assets/`) | The output format is meant to adapt to each request |
| Runs are slow, or the main context fills with raw intermediate noise | **4 — Speed** (`agents/`) | The work is small, sequential, or each step depends on the previous one |
| Output looks right structurally but you can't trust it's correct, fresh, on-topic, or hallucination-free — needs an LLM-as-judge to verify | **5 — Tests** (`tests/`) | The output is mechanical (no claims to verify, no tone to judge), or a human reviews every run anyway |

## How to read the result

- **Most skills need 1–3 controls, not 5.** A clean answer of "only Output" is a
  perfectly good skill. Don't pad it.
- **Control 5 (Tests) earns its place when correctness is a judgement call.**
  Tests cost a grader subagent every run, so they're worth it when shipping a
  wrong-but-plausible deliverable would actually hurt — sources, claims, tone,
  PII. If a human reads every output before it ships, the human IS the grader
  and a subagent gate is overhead.
- **Control 4 depends on Control 2 or the work being parallelisable.** There's
  nothing to fan out if the skill does one small thing.
- **Write down the verdict.** Before building, state explicitly: "Adding
  controls X and Y because [observed failure]. Skipping Z because [reason]."
  That list is the build plan.

## The diagnosis loop

If you're unsure whether a control is needed, **run the plain skill a few times
first** (Step 2's draft) and watch what changes between runs:

- Different sources cited → Control 1
- Different sequence of steps in the transcript → Control 2
- Different layout/sections in the output → Control 3
- Long serial transcript, slow → Control 4
- Output that's plausible but you had to g14-fact-check by hand → **Control 5 — Tests**

The drift you actually observe is the only reliable signal. Don't guess controls
from the skill's description alone.
