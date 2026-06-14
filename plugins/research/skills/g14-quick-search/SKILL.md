---
name: g14-quick-search
description: "Runs 5 parallel web searches via the `web-searcher` agent to give a quick panoramic overview of any topic, then synthesizes them inline via `research-synthesizer` (format: inline-summary, ~250 words). Use it whenever the user asks for a quick search on X, quick overview of Y, what's known about Z, panoramic view of X, give me a quick recap of Y, or any variation implying fast reconnaissance of a topic's state without needing an exhaustive report. Also triggers with /g14-quick-search. If the user doesn't provide an explicit query, extract the most recent topic from the conversation."
---

# g14-quick-search

Quick panoramic overview of a topic: 5 parallel `web-searcher` invocations + inline synthesis via `research-synthesizer`. No files, no long reports — brief and useful, directly in the chat.

## Architecture

| Component | Owner | Role |
|---|---|---|
| Main agent (you) | this skill | Determine query, pick 5 angles, orchestrate, present |
| 5 × `web-searcher` | plugin agent | Each runs 1-2 queries from one panoramic angle, returns inline summary |
| `research-synthesizer` | plugin agent | Aggregates the 5 angle summaries into a ~250-word recap (format: `inline-summary`) |

## Flow

### 1. Determine the query

- **If the user provided an explicit query** → use it as-is.
- **If there's no query** → review recent messages and extract the most recent topic. If unclear, briefly ask.

Confirm to the user in one short sentence before launching: e.g., "Launching 5 searches on **<topic>**…". This lets them correct you.

### 2. Pick 5 distinct angles

The value of 5 parallel searches comes from **covering different angles**, not repeating the same query 5 times. Use `web-searcher` canonical angle names when they fit, otherwise free-form.

Useful starting templates (adapt — don't copy literally):

- `fundamentals` — definition and key concepts
- `current-state` — recent news (last few months)
- `use-cases` — practical examples / applications
- `criticism-limitations` — downsides, debate
- `comparisons` — alternatives / who leads the space

If the topic is very specific (a product, person, event), reformulate the angles: "launch and trajectory", "reviews and public opinion", "direct competitors", "controversies", "pricing and availability".

If the topic is highly technical: "fundamentals", "real implementations", "benchmarks and performance", "known trade-offs", "ecosystem and tooling".

The 5 results combined should give a panoramic view without unnecessary overlap.

### 3. Launch 5 × `web-searcher` IN PARALLEL (single message)

**Critical:** the 5 `Task` calls must go in a single message so they run in parallel. Separate messages serialize them.

For each angle, invoke `Task` with `subagent_type: web-searcher` and prompt:
- `topic: {topic}`
- `queries: [1-2 queries for this angle]`
- `angle: {canonical angle name or free-form}`
- `output_mode: inline`
- `max_fetches: 1` (g14-quick-search prioritizes speed — one fetch per angle is enough)
- `source_tier_filter: any` (panoramic recon — don't restrict tiers)
- `language: {detected language}`

The agent runs the searches and returns a tight 200-word block per angle.

### 4. Synthesize inline via `research-synthesizer`

When the 5 reports arrive, invoke `research-synthesizer` with:
- `format: inline-summary`
- `findings_mode: inline`
- `inline_findings` (via `extra_context.inline_findings`) — the 5 reports concatenated as a single string, each block delimited by a line containing only `--- FINDING N ---` (N = 1..5)
- `topic: {topic}`
- `language: {detected language}`
- (no `output_path` — the synthesizer returns the recap as its message)

The agent produces the ~250-word panoramic recap in the canonical format:

```
**{Topic}** — quick overview

<2-3 lines with the general idea that emerges from joining the 5 angles>

**The essentials:**
- <most important finding 1>
- ...

**Surprises or tensions:**
- <only if any exist>

**Main sources:** domain1.com, domain2.com, …

Want me to dig deeper into any specific angle?
```

Pass the recap to the user verbatim. Hard cap: ~250 words.

## Critical rules

- **Parallelism in a single message.** The 5 `web-searcher` `Task` calls must be emitted together. The synthesizer call comes right after they all return.
- **Agents own knowledge.** Source tiers, angle strategies, output format — all in the agents.
- **Don't save files.** Nothing on disk.
- **Don't run searches in the main agent.** Delegate to `web-searcher`. The main agent only orchestrates.
- **Output language:** match the conversation. Default English.

## What to present at the end

The recap from `research-synthesizer`, and nothing else. No operational stats, no meta-commentary on how many searches you ran. The user wants the content, not the process.
