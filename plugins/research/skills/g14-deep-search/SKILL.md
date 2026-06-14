---
name: g14-deep-search
description: "Exhaustive research on any topic via 50 parallel web searches (10 gatherers × 5 queries each), synthesized into a single markdown document saved to `research/{slug}/{slug}.md` in the CWD. Use it when the user wants a complete report, a deep dive, in-depth research, to compile all possible information about a topic, or phrases like 'deep research on X', 'exhaustive research about Y', 'compile everything about Z', 'write a report on X', 'in-depth analysis of Y', 'complete overview of Z', 'research X thoroughly', 'investigación exhaustiva sobre X', 'informe completo sobre Y'. Also triggers with /g14-deep-search. Designed for speed: all gatherers run in parallel via the `web-searcher` agent."
---

# g14-deep-search

Exhaustive research: 50 parallel web searches via 10 `web-searcher` invocations, consolidated by `research-synthesizer` into a single markdown document, optionally quality-gated by `hallucination-grader` + `source-validator`.

## Architecture

This skill is a thin orchestrator. The agents own the work.

| Component | Owner | Role |
|---|---|---|
| Main agent (you) | this skill | Capture topic, plan 50 queries in 10 thematic groups, orchestrate, present |
| 10 × `web-searcher` | plugin agent | Each runs 5 queries from one angle, writes 1 findings file |
| `research-synthesizer` | plugin agent | Reads the 10 findings, writes the final markdown document |
| `hallucination-grader` + `source-validator` | plugin agents | Optional quality gate (recommended for high-stakes research) |

## Flow (6 phases)

### 1. Capture the topic and create the structure

- If the user didn't provide a topic, ask in a single line. Don't do anything else until you have it.
- Generate a `slug` in kebab-case, max 5 words, no accents or punctuation. Drop obvious stopwords. Example: "State of the art of multimodal agents in 2026" → `multimodal-agents-2026`.
- Detect the user's language for the output document (see Language Rule below).
- Create in the CWD:

```
research/{slug}/
  findings/             # 10 files written by web-searcher invocations
  _grader-reports/      # JSON from quality gates (if run)
  _progress.md          # optional operational log
```

If the folder already exists (resume after interruption), see "Resume" at the end.

### 2. Generate 50 queries in 10 thematic angles

**You do this directly in the skill — not in a subagent.** Query planning is the skill's essence; it's not reusable cross-skill knowledge.

Structure: 10 angles × 5 queries each. Use one of the `web-searcher` canonical angle names when it fits (`fundamentals`, `current-state`, `actors-and-leaders`, `implementation`, `use-cases`, `criticism-limitations`, `comparisons`, `economics-pricing`, `future-predictions`, `learning`) or a free-form description for topic-specific angles.

Base template (adapt to topic — don't copy literally):

| #  | Angle (canonical name)            | Query types                                                    |
|----|-----------------------------------|----------------------------------------------------------------|
| 1  | `fundamentals`                    | "what is X", "how X works", glossary, fundamentals             |
| 2  | `current-state`                   | "X 2026", "X latest news", roadmap, recent updates             |
| 3  | `actors-and-leaders`              | "top X companies", "main players in X", "X market leaders"     |
| 4  | `implementation`                  | "how to implement X", "X tutorial", "X best practices"         |
| 5  | `use-cases`                       | "X case study", "X enterprise adoption", production examples   |
| 6  | `criticism-limitations`           | "X limitations", "problems with X", "X criticism", "X failures"|
| 7  | `comparisons`                     | "X vs Y", "alternatives to X", "X comparison"                  |
| 8  | `economics-pricing`               | "X pricing", "X business model", "X cost", ROI                 |
| 9  | `future-predictions`              | "X future", "X predictions 2027", "X roadmap"                  |
| 10 | `learning`                        | "learn X", "X course", "X hands-on", official docs             |

Adapt the angles to the topic:
- **Specific product/company** (e.g., "Notion"): "features", "reviews", "competitors", "success stories", "pricing", "integrations".
- **Public figure**: "biography", "career", "work", "recent interviews", "controversies".
- **Event/news**: "what happened", "causes", "consequences", "reactions", "background".
- **Abstract technical concept**: keep the base template.

**Principles for quality queries:**
- **Real diversity, not reformulations.** "what is X" and "X explained" are the same query.
- **Mix languages.** If the topic is international, ~50-60% English queries yield denser technical results; the rest in the user's language give local context.
- **Mix breadth.** Combine broad queries ("ai agents") with specific ones ("LLM context caching pricing Anthropic 2026") within the same angle.

Before launching, mentally check: any literal duplicates across angles? Any angle covering the same ground in its 5 queries? If so, rewrite.

### 3. Launch 10 × `web-searcher` IN PARALLEL (single message)

**Critical:** the 10 `Task` calls must be emitted in the **same assistant turn**, in a single block. Splitting them across messages serializes execution.

For each of the 10 angles, invoke `Task` with `subagent_type: web-searcher` and prompt that supplies:
- `topic: {topic}`
- `queries: [list of the 5 queries for this angle]`
- `angle: {canonical angle name, e.g. "fundamentals" — or free-form description}`
- `output_mode: file`
- `output_path: research/{slug}/findings/{NN}-{angle-slug}.md` (NN from 01 to 10)
- `language: {detected language}`
- `max_fetches: 2` (cap at ~100 fetches total across the 10 gatherers — default would be 150)

The agent handles the rest: WebSearch per query, deduplication, WebFetch on the substantial sources, structured findings file, anti-hallucination rules.

When all 10 finish, verify the 10 files exist. If any failed, relaunch **only that angle**.

### 4. Synthesize via `research-synthesizer` (1 call)

Invoke `Task` with `subagent_type: research-synthesizer` and prompt that supplies:
- `format: markdown`
- `findings_paths: [absolute paths to all 10 findings files]`
- `output_path: research/{slug}/{slug}.md`
- `topic: {topic}`
- `slug: {slug}`
- `language: {detected language}`

The agent reads all 10 findings and writes a 3000-5000 word coherent document with executive summary, introduction, one section per angle (300-600 words each in flowing prose), conclusions, and a deduplicated sources list.

### 5. Optional quality gate

For high-stakes research (the user explicitly asks for verification, or the document is going somewhere consequential), fire both graders **in parallel in a single message**:

- `Task subagent_type: hallucination-grader` with `output_path: research/{slug}/{slug}.md`, `findings_dir: research/{slug}/findings/`, `verdict_path: research/{slug}/_grader-reports/hallucination.json`
- `Task subagent_type: source-validator` with `output_path: research/{slug}/{slug}.md`, `verdict_path: research/{slug}/_grader-reports/reachability.json`

If `pass < 13/15` on hallucination or `(ok+ok_gated) < 90%` on reachability, flag the weak claims/URLs in the presentation message.

By default (no explicit request), skip this phase — `g14-deep-search` prioritizes speed.

### 6. Present to the user

```
Research complete: **{topic}**

Document: `research/{slug}/{slug}.md` ({words} words)
50 queries run across 10 angles
~{N} unique sources consulted

**Executive summary:**
{first paragraph from the document}

Want me to dig deeper into a specific angle, export to another format, or run more queries in a particular area?
```

## Language rule

**Output language: match the language the user is using in the current conversation. Default to English if unclear.**

Apply the language setting to:
- The `language` parameter in all `web-searcher` invocations
- The `language` parameter in the `research-synthesizer` invocation
- The final presentation message

## Critical rules

- **Parallelism in a single message.** The 10 `web-searcher` `Task` calls in Phase 3 must go together. The 2 graders in Phase 5 (if run) also together.
- **Agents own knowledge.** Do not repeat the search methodology, source tiers, or output format inside this skill — those live in `web-searcher` and `research-synthesizer`.
- **Default output path:** `research/{slug}/{slug}.md` in the CWD.
- **No bootstrap, no installation, no auxiliary files.** This skill is self-contained.
- **Do not read findings in the main agent.** The synthesizer does that. You only verify the 10 files exist.

## Quick troubleshooting

- **A `web-searcher` didn't write its file:** relaunch only that angle with the same prompt.
- **Several `web-searcher` invocations fail at once:** likely rate limit. Wait 1-2 min, relaunch only failed ones.
- **Synthesizer produces a short/collage document:** retry with "minimum 3500 words, minimum 350 per section, convert bullets to prose". If it keeps failing, escalate that single call to `sonnet`.
- **A query returns 0 useful results:** acceptable. The `web-searcher` notes it as "no useful results" and continues.
- **Results saturated with SEO/spam:** add operators to the queries (`site:arxiv.org`, specific year, technical terms).

## Resume after interruption

1. List `research/{slug}/findings/`. If fewer than 10 files, missing angles are identified by the absent numeric prefix (`01-`, `02-`, ...).
2. Relaunch only the `web-searcher` calls for the missing angles.
3. If all 10 findings exist but `{slug}.md` is missing, launch only the synthesizer (Phase 4).
4. If the document exists but graders weren't run and the user wants them, launch Phase 5.
