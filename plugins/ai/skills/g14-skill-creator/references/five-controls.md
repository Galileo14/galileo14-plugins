# The Five Controls — build instructions

This is the detailed reference for each control. For each one you'll find: the
drift it fixes, the artifact to build, the folder layout, and the exact
`SKILL.md` wiring. Build the artifact first, then add the wiring — an artifact
with no wiring is never read.

## Table of contents

1. [Control 1 — Input (`references/`)](#control-1--input)
2. [Control 2 — Process (`scripts/`)](#control-2--process)
3. [Control 3 — Output (`assets/`)](#control-3--output)
4. [Control 4 — Speed (`agents/`)](#control-4--speed)
5. [Control 5 — Tests (`tests/`) — quality / LLM-as-judge](#control-5--tests)

---

## Control 1 — Input

**Drift it fixes:** the skill never says *where* to look, so Claude picks
sources itself — differently every run. Coverage is unrepeatable, and an
unvetted source is how a fabricated or low-quality fact gets in.

**The fix:** decide the sources once. Put one markdown file per source in
`references/sources/` (or a single whitelist file), then make `SKILL.md` say:
read these, use *only* these. The run now operates in a closed world you
defined.

Each source file carries everything Claude needs to use that source the same
way every time — URL, language, how to navigate it, how deep to go, what to
skip, how to judge recency, why it's trusted.

```
skill-name/
└── references/
    └── sources/
        ├── source-a.md
        └── source-b.md
```

Example source file:

```markdown
# Source: TechCrunch — AI

url: techcrunch.com/category/artificial-intelligence
language: en
pages_to_scrape: 3
follow_into_article: yes
ignore: sponsored posts, event promos, newsletter blocks
recency: each card shows a relative date — keep only items <= 7 days old
trust: tier-1 outlet, primary reporting
```

Wiring in `SKILL.md`:

```markdown
## Step 1 — Load the sources
Read every file in references/sources/. Each defines one approved source and
how to read it. Use ONLY these sources. Do not fall back to open web search.
Do not add a source not in this folder. If a source is unreachable, record it
as skipped — do not substitute another.
```

**Why it's worth it:** a closed world isn't just repeatable, it's *trustworthy*.
With a fixed whitelist, Claude physically cannot wander onto a spoofed or junk
page. Adding a source becomes a reviewed edit, not a silent run-time guess.

**`references/` also holds** any material Claude should read before/during a run
— schemas, frameworks, style guides, fact whitelists. Same rule: it does nothing
until `SKILL.md` points at it.

**Skip this control when** the skill should explore freely (open-ended research,
discovery) or when the input is already pinned — e.g. the skill processes a file
the user themselves uploaded.

---

## Control 2 — Process

**Drift it fixes:** the sources are fixed but the *method* isn't. Claude
reinvents how to do the work each run — plain reasoning this time, a hand-written
script next, an MCP after. Different method means different coverage, different
bugs, and tokens burned re-reasoning the same "how".

**The fix:** write the process down once, as code. Put scripts in `scripts/` and
make `SKILL.md` tell Claude to *run* them rather than improvise.

```
skill-name/
└── scripts/
    ├── fetch_source.py    take a source file, fetch it, emit normalised JSON
    ├── dedupe.py          cluster duplicates
    ├── rank.py            score and keep the top N
    └── validate.py        assert the output shape
```

Wiring — replace vague prose with exact commands:

```markdown
## Step 2 — Process
For each source file, run:  python scripts/fetch_source.py <file>
Then on the combined results: python scripts/dedupe.py
                              python scripts/rank.py --top 50
                              python scripts/validate.py
```

**Two ways to pin a process:**
- **Scripts** — for deterministic work with a right answer (fetching, deduping,
  ranking, validating). Runs identically every time, costs almost no tokens
  because the reasoning happened once at build time.
- **Plain-text steps** — for tool/MCP work that *can't* be scripted ("call this
  MCP", "use this tool"). Name the exact tool and arguments in `SKILL.md` so
  Claude doesn't pick a different one.

**Keep an escape hatch.** Determinism shouldn't mean brittleness. Tell the skill
that if a script fails or an input has changed, Claude may improvise to recover
— and must report it, so the user can update the script. The script is the
default path, not a cage.

**Skip this control when** the task is genuinely novel each run, or inputs are
hostile/unstable and need live improvising.

Write scripts in Python unless there's a specific reason to use another language.

---

## Control 3 — Output

**Drift it fixes:** same sources, same process — but Claude still decides *how
to present* the result. A table one run, prose the next, a bare list after. The
data is stable; the deliverable isn't.

**The fix:** hand Claude the finished shape. Put a literal output template in
`assets/` — an HTML/CSV/JSON file with slots to fill — and make `SKILL.md` say:
populate this file, do not redesign it.

```
skill-name/
└── assets/
    ├── output-template.html   the deliverable shell, with {{SLOT}} placeholders
    ├── output-template.csv    flat export shape
    └── item.json              the schema each item must match
```

Template excerpt:

```html
<!-- header: do not edit -->
<h1>Report — {{WEEK}}</h1>
<!-- repeat this block per item -->
<article>
  <h3>{{HEADLINE}}</h3>
  <p>{{SUMMARY}}</p>
</article>
```

Wiring:

```markdown
## Step 4 — Render
Load assets/output-template.html. Fill every {{SLOT}}. Repeat the <article>
block once per item, in order. Do not change the structure, headings, classes
or styling. The template IS the design — you only supply content.
```

The slots still hold generated text, so wording varies run to run — that's fine
and expected. The template locks everything *around* the text: structure, order,
sections, styling. Make the container deterministic; let only content breathe.

**`assets/` also holds** fixed brand files — logos, fonts, images — dropped into
output unchanged.

**Skip this control when** the output format is meant to adapt to each request.

---

## Control 4 — Speed

**This control raises efficiency, not determinism.** Add it when runs are slow
or the main context fills with noise.

**Drift it fixes:** independent work done serially is N× slower than it needs to
be, and every raw intermediate result piles into the main context window —
expensive, and less accurate as it fills.

**The fix:** split independent work onto parallel subagents. The main thread
becomes an orchestrator: it dispatches one subagent per unit of work, they run
at once, and only their clean results come back.

A subagent runs in its own context window. It does the messy work and returns
*only the result* to the main thread — not the transcript of how it got there.
Two wins: **speed** (N units in parallel take as long as the slowest one) and
**clean context** (the main thread sees N tidy results, not N messy
transcripts).

```
skill-name/
└── agents/
    └── worker.md    one worker definition, reused per unit of work
```

```markdown
---
name: source-scraper
description: Scrape ONE source and return normalised JSON.
model: haiku
tools: Bash, Read, WebFetch
---
You receive ONE source file. Run scripts/fetch_source.py against it.
Return ONLY the normalised JSON array. Do not summarise, rank or comment.
```

Wiring:

```markdown
## Step 2 — Scrape in parallel
Dispatch one worker subagent per source file, all at the same time — do not run
them in sequence. Wait for all to return, concatenate their JSON arrays, pass
the combined set to Step 3.
```

**Match the model to the job.** Mechanical work (scraping, extraction) doesn't
need a frontier model — pin the worker to a cheap, fast model (Haiku) and keep
the expensive model for the orchestrator's judgement work.

**Registration caveat — important.** Claude Code only auto-registers subagents
from `.claude/agents/` (or `~/.claude/agents/`, or a plugin's `agents/`) — *not*
from a folder nested inside a skill. So there are two valid setups:

- Put the real subagent definition in `.claude/agents/` so it can be dispatched
  by name. Best when the agent is shared across skills.
- Keep an `agents/` folder *inside* the skill holding plain instruction files,
  and have `SKILL.md` tell the orchestrator to spawn a **general-purpose**
  subagent that reads that file. Keeps the skill portable in one directory — but
  the nested file's `model`/`tools` frontmatter will *not* apply on its own; set
  the model when dispatching instead.

**Skip this control when** the work is small, sequential, or the steps depend on
each other.

---

## Control 5 — Tests

**Drift it fixes:** the shape is right but the *content* is wrong. A summary
that claims something the source never said. A "fresh" item that's two months
old. An on-topic-looking item that's actually off-topic. A polite tone that's
secretly condescending. A skill can have all of Controls 1–4 wired and still
ship a wrong-but-plausible deliverable — because nothing is checking the
content for truth or fit.

**The fix:** a quality gate that runs **every invocation** of the skill,
graded by a *fresh* subagent (LLM-as-judge) against a written rubric. Rubrics
live in `tests/`, one markdown file per concern.

```
skill-name/
└── tests/
    ├── accuracy-test.md    rubric: does every claim trace to its source?
    ├── relevance-test.md   rubric: is every item on-topic?
    ├── freshness-test.md   rubric: is every item within the recency window?
    └── safety-test.md      rubric: no PII, nothing unsafe
```

Rubric format — the rubric tells the fresh grader exactly what to check, with
hard PASS criteria so the grader can't fudge:

```markdown
# Rubric: Accuracy

Grade every item in the final output. PASS an item only if:
- Every claim in the summary is supported by the linked source — open and verify.
- No number, name or date appears that is not in the source.
- The headline is not editorialised beyond the source.

For each item, return: { id, passed, evidence }.
Quote the supporting source text. Flag failures — do not silently fix them.
```

Wiring (in the skill under test):

```markdown
## Quality gate (before delivering output)
For EACH rubric file in tests/, dispatch a SEPARATE general-purpose subagent
in fresh context — NOT the agent that produced the output.

Dispatch config (mirror the grader's frontmatter — skill-nested agents are not
auto-registered):
  model: sonnet
  tools: Read, Glob, Grep
  subagent_type: general-purpose

Inputs to pass in the prompt:
  1. rubric_path   — the full path to the rubric file.
  2. output        — the deliverable to grade (text or path).
  3. skill_context — one sentence on what the skill does (optional).

Tell the subagent to follow the grader instruction file:
${CLAUDE_PLUGIN_ROOT}/skills/g14-skill-creator/agents/grader.md

The grader returns strict JSON with per-item pass/fail and evidence. Collect
all gradings. If any item fails any rubric, flag it with the grader's evidence
or drop it and note the gap. Never ship a failing item silently.
```

**Why a fresh-context grader is non-negotiable.** A model reviewing its own
work in the same context is primed to agree with itself — it just made those
choices and remembers the trade-offs. A fresh subagent that sees *only* the
rubric and the output has no such attachment. That independence is the test.
Control 4 (parallelism) makes running N fresh graders cheap, which is why this
works in practice.

**One rubric per concern, not one rubric for everything.** A rubric that tries
to check accuracy AND tone AND safety in one pass gives weaker signal than
three focused rubrics graded in parallel. Each rubric is a single question.

**What good rubric criteria look like:**

- ✅ "Every claim is supported by a linked source — open and verify."
- ✅ "No PII appears in the output (names, emails, phone numbers, addresses)."
- ✅ "Every item's date is within 7 days of today."
- ❌ "The summary is comprehensive." (subjective, no PASS criterion)
- ❌ "The tone is appropriate." (appropriate to what? rewrite as a measurable rule)

If a criterion can be passed by reading the output without checking against
anything external (sources, dates, a banned-words list), it's probably too soft.

**Skip Control 5 when** the output is mechanical with no claims to verify
(e.g. translating one sentence), or when a human reviews every run anyway —
the human IS the grader. Adding a subagent gate on top is overhead.
