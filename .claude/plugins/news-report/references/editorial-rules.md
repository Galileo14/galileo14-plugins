# Editorial rules

Generic curation, ranking and writing rules shared by every sector skill.
The calling skill provides:

- **Sector frame** — what counts as "relevant" for this sector (the skill body restates the filter from its angle).
- **Audience lens** — used in the "Why it matters" block. Passed through verbatim to the writer.

This file defines the universal rules. Adjust per-skill via the skill body, not by editing here.

---

## Filter and ranking

The report covers **products, tools, launches and technical updates**, not general news. The calling skill MAY narrow this further (e.g. "AI tooling only", "fintech APIs only").

### Do NOT report

- Geopolitics, conflicts, international politics.
- Pure market macro (oil prices, FX, IPOs as financial topic).
- Abstract regulation with no product component (legal debates, hearings).
- Corporate moves with no product component (IPOs, M&A, isolated earnings).
- Hype with no concrete launch.

### DO report

- Product launches / new features / new APIs.
- New tools (apps, SDKs, models, platforms).
- **Developer tooling**: IDEs, coding agents, frameworks, libraries, SDK releases, platform changes (GitHub, Vercel, Cursor, etc.).
- **Notable hires** in the sector: executive moves, team creation, poaching, notable departures.
- Concrete use cases with an identifiable product.
- Benchmarks, papers or techniques with public implementation.
- Enterprise adoption with identifiable tooling (not just "X bought Y").

### Ranking criteria (highest to lowest weight)

1. **Concrete product / tool** — identifiable and actionable.
2. **Real availability** (shipped > announced > rumored).
3. **Applicability to the caller's audience** — the skill's `audience` field defines this lens.
4. **Technical novelty** — a new capability, not incremental.
5. **Freshness** — more recent, better.
6. **Source diversity** — no 3 versions of the same story.

---

## Enrichment prompts

### WebFetch — original article

> "Extract the concrete facts from this article: what was launched or announced, dates, figures, proper nouns, integrations, prices, availability (GA / beta / waitlist / region), benchmarks or quoted metrics, relevant verbatim statements, and links to documentation or product. Ignore editorial opinion, generic historical context and filler."

### Triangulation queries

Search by **topic**, not the article. Goal:

- Confirm / nuance with independent sources.
- Find the official statement if RSS only carries secondary coverage.
- Capture technical reactions, third-party benchmarks, debates.
- Detect whether the story is a big deal or amplified noise.

Useful query patterns:

- `<product> release notes` / `<product> changelog` / `<product> documentation`
- `<product> review` / `<product> benchmark`
- `<product> hacker news` / `<product> reddit`
- `<event> <technical term>` (e.g. "Google I/O 2026 search Gemini")
- `<company> blog announcement <date>`

Max **1-3 searches per candidate** to keep cost bounded.

---

## Failure handling

- **`WebFetch` fails** (paywall, 403, timeout):
  1. Look in `news.json` for another item covering the same event and `WebFetch` that one.
  2. If still nothing, reconstruct from `WebSearch` and mark the source as `Summary reconstructed from secondary sources (original article inaccessible)`.
- **`WebSearch` returns nothing**: continue with the original `WebFetch` alone; not blocking.
- **Candidate weakens after enrichment**: drop it, promote the next shortlisted item.

---

## Report rules

Each template block has a specific size and purpose.

### TL;DR

- 2-4 bullets, ≤25 words each.
- Facts, not opinion.
- All about products / tools.

### Today's focus

- 2-4 sentences about story #1.
- Synthesize the dossier (don't copy the feed).
- Apply the caller's `audience` lens — what this means specifically for that audience.

### Per top story

- **What happened** — 3-6 sentences with facts from the `WebFetch`. High density: figures, names, dates, integrations, availability, benchmarks.
- **Additional context** — 1-3 sentences with what other channels add (official statement, technical reactions, third-party benchmarks). Omit if no signal.
- **Additional sources** — 0-4 links from triangulation, each with a one-sentence explanation. Omit the block if empty.
- **Why it matters** — through the caller's `audience` lens: what would that audience actually do with this?

### Hard rules

- `top_n` stories by default (skill-provided), more only if user explicitly asks.
- If nothing relevant happened: write the report with a TL;DR saying so and a "Rest of the day" section only.
- Never invent data, dates or figures. If a field isn't in the consulted sources, omit it.
- Attribute key figures or contested data to their concrete source.

---

## Adding a sector skill

Each sector lives as its own skill under `skills/<slug>/SKILL.md`. The skill body declares:

- `sector` slug (used in output paths)
- Default time `window` and how to override
- `keywords` filter passed to the scraper
- `sources` subset (or all)
- `audience` paragraph (the lens for "Why it matters")
- `top_n`
- `output_lang` (if not English)

The skill then tells Claude to invoke `Agent(subagent_type=news-pipeline)` with that config, or runs the pipeline inline following [workflow.md](workflow.md).

## Adding an RSS source

See [`scripts/rss-scraper/README.md`](../scripts/rss-scraper/README.md) for the adapter and registration pattern.
