---
name: g14-fact-check
description: "Verifies whether a specific claim is true by launching 10 parallel `web-searcher` invocations, each from a different evidence angle (primary sources, established media, dedicated fact-checkers, counter-evidence, etc.), then emits a structured verdict via `research-synthesizer`: True / False / Misleading / Partially True / Insufficient Data. Use when the user asks 'fact-check', 'verify', 'check if this is true', 'is it true that...', 'debunk', 'confirm', 'is this accurate', or says things like 'I heard that...', 'someone told me...', 'is it a myth that...' and wants to confirm/refute the claim. Also triggers for 'comprueba si es cierto', 'verifica esto', 'es verdad que'. If the user says just 'fact-check' or 'verify' without a claim, extract the most recent factual assertion from the conversation."
---

# g14-fact-check

Verifies a factual claim by fanning out 10 `web-searcher` invocations across complementary evidence angles, then emits a structured verdict via `research-synthesizer`. All-inline (no files), optimized for speed.

## Architecture

| Component | Owner | Role |
|---|---|---|
| Main agent (you) | this skill | Reformulate claim, pick 10 evidence angles, orchestrate, optionally validate URLs |
| 10 × `web-searcher` | plugin agent | Each runs 1-3 queries from one evidence angle, returns inline summary |
| `research-synthesizer` | plugin agent | Aggregates the 10 evidence reports into the verdict (format: `verdict`) |

URL-level validation (`source-validator`) is intentionally NOT used here — g14-fact-check is inline-only and the synthesizer already drops fabricated-looking sources during verdict assembly.

## Non-negotiable principles

- **Never fabricate sources, URLs, or data.** The agents enforce this; if one slips through, drop it and say so.
- **Acknowledge uncertainty.** "Insufficient Data" is a valid verdict — use it when appropriate.
- **Separate facts from opinions.** Only factually verifiable parts get verified.
- **Neutrality.** Report what the evidence says, don't advocate.
- **Output language:** match the language the user is using. Default to English if unclear.

## Flow (5 steps)

### 1. Identify and reformulate the claim

- If the user gave the claim explicitly, use it.
- If they only said "g14-fact-check" / "verify", extract the most recent factual assertion from the conversation.
- **Reformulate precisely:** strip opinion, pin down numbers, dates, and actors. An ambiguous claim produces an ambiguous verdict.
- Confirm in one short line before launching: *"Verifying: «{reformulated claim}». Launching 10 searches…"*. This lets the user correct you.

### 2. Pick 10 evidence angles

The strength of fact-checking comes from **convergence (or divergence) across independent angles**, not repeating the same search.

Map each angle to a `web-searcher` canonical angle name when it fits, otherwise use a free-form description.

Base template (adapt to claim type):

| #  | Angle (canonical name)         | What it looks for                                                       |
|----|--------------------------------|-------------------------------------------------------------------------|
| 1  | `verbatim`                     | The claim's phrasing as-is; where it appears and how it's framed        |
| 2  | `counter-evidence`             | "X is not true", "X debunked", refutations                              |
| 3  | `primary-source`               | `.gov`, `.edu`, official statistical agencies                           |
| 4  | `peer-reviewed`                | Nature, Science, PubMed, arXiv (per topic)                              |
| 5  | `fact-checker`                 | Snopes, PolitiFact, FactCheck, Full Fact, Maldita, Newtral, Chequeado   |
| 6  | `established-media`            | Reuters, AP, BBC, NYT, FT, Bloomberg, El País                           |
| 7  | `actors-named`                 | What people/companies/institutions cited actually say (official statements) |
| 8  | `numbers-and-dates`            | Every number/date in the claim verified against original sources        |
| 9  | `historical-baseline`          | Is this new or recurring? Comparable prior data                         |
| 10 | `recent-updates`               | Has anything changed recently that invalidates/reinforces the claim     |

If the claim is on a specific topic, swap generic angles for more specific ones:
- **Health/medicine:** add "current medical consensus", "Cochrane reviews", "medical society guidelines".
- **Economic figures:** add "data from the relevant central bank / regulator".
- **Recent events:** strengthen angle 10 (updates) and angle 6 (immediate media coverage).
- **Controversial scientific claims:** explicitly add "consensus vs. scientific minority".

### 3. Launch 10 × `web-searcher` IN PARALLEL (single message)

**Critical:** the 10 `Task` calls must be emitted in the **same assistant turn**, in a single block.

For each angle, invoke `Task` with `subagent_type: web-searcher` and a prompt that supplies:
- `topic: {reformulated claim}`
- `queries: [1-3 specific queries for this angle — let the agent pick the right number]` (you may pass a single string when one query is enough, or a list)
- `angle: {canonical angle name from the table above, or free-form description}`
- `output_mode: inline` (no file — the agent returns the structured 200-word report as its message)
- `language: {detected language}`
- `source_tier_filter: tier-1-and-2` for the `primary-source`, `peer-reviewed`, `fact-checker`, `established-media` angles (optional but recommended)

The agent runs the searches, fetches the substantial sources, dedupes wire copy, and returns a structured `ANGLE / STANCE / SOURCES / KEY EVIDENCE / NUANCE` block.

### 4. Aggregate into a verdict via `research-synthesizer`

When the 10 inline reports arrive, invoke `research-synthesizer` with:
- `format: verdict`
- `findings_mode: inline`
- `inline_findings` (via `extra_context.inline_findings`) — the 10 reports concatenated as a single string, each block delimited by a line containing only `--- FINDING N ---` (N = 1..10)
- `topic: {reformulated claim}`
- `language: {detected language}`
- (no `output_path` — receive verdict as the agent's message)

The agent applies the decision tree (Partially True / Misleading / False / True / Insufficient Data), respects tie-breakers (recency, tier over count, expert disagreement → Insufficient), and emits the verdict block in the format described below.

### 5. Render the verdict

Render to the user verbatim from the synthesizer's output. Structure (the synthesizer produces this — you do not rebuild it):

```
🔍 **Claim to verify:** {reformulated claim}

⚖️ **Verdict:** {True / False / Misleading / Partially True / Insufficient Data}

📝 **Analysis:**
{2-3 paragraphs}

📚 **Sources consulted ({N}):**
1. {Source name} — {what it contributes, 1 line}
2. ...
```

- The `{N}` in "Sources consulted" is the count of unique, useful sources actually found (drop inconclusives).
- Translate emoji-labels and verdict names to the conversation language (English default).
- No filler. No "it's important to note...". Get to the point.

## Critical rules

- **Parallelism in a single message.** The 10 `web-searcher` `Task` calls go together, not in series.
- **Agents own knowledge.** The angle taxonomy, source tiers, verdict decision tree, and rendering format live in the agents. The skill picks angles and orchestrates.
- **No WebSearch/WebFetch in the main agent.** The `web-searcher` invocations do that. You only orchestrate and aggregate.
- **No files.** This skill creates nothing on disk. All output is inline in the chat.
