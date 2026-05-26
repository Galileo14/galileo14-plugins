---
name: new-rss-source
description: Add a new RSS source (adapter) to the news-report scraper. Interviews the user for the publication name, finds its RSS feed(s) via WebSearch/WebFetch, writes an adapter file under scripts/rss-scraper/adapters/, registers it in registry.ts, and verifies it returns items. Trigger with '/new-rss-source', 'añade una fuente RSS', 'add an RSS adapter', 'nueva fuente al scraper', 'añadir source al news report'.
user-invocable: true
---

# /new-rss-source

Interactive wizard that adds a new RSS source to the scraper. You research the feed, write the adapter, register it, and smoke-test it end-to-end.

Use this when the user wants to add coverage from a publication that isn't yet in `scripts/rss-scraper/registry.ts`.

## What you (Claude) must do when invoked

Run the discovery + integration flow below. Do not skip steps. The goal is a registered, working adapter — not just a written file.

### Step 1 — Identify the source

Ask the user, in plain text or with `AskUserQuestion`:

1. **Publication name** — e.g. "The Verge", "Ars Technica", "Anthropic blog", "Hugging Face". (Free text.)
2. **Adapter slug** — propose `<lowercase_snake_case>` (e.g. `the_verge`, `ars_technica`, `anthropic`, `huggingface`). Validate: `^[a-z][a-z0-9_]*$`, ≤30 chars, not already in `registry.ts`. Show your proposal and let the user override.
3. **Topical scope** — does the publication post mostly about AI / tech / general news / a niche? (Used later for `tags`.) Free text or a short list.

Skim `${CLAUDE_PLUGIN_ROOT}/scripts/rss-scraper/registry.ts` and the existing adapters to make sure the slug is unique and to mimic naming conventions (`new_york_times`, `the_information`, etc.).

### Step 2 — Discover the RSS feed(s)

This is the part that requires research. Do it in this order until you find a working feed:

1. **`WebSearch`** for `"<publication name>" rss feed` and `site:<domain> rss`. Capture every candidate URL.
2. **`WebFetch`** the publication's homepage and look for `<link rel="alternate" type="application/rss+xml" ...>` or `application/atom+xml` tags. Also check `/feed`, `/rss`, `/feed.xml`, `/rss.xml`, `/feeds/all.atom.xml`, `/index.xml`, `/atom.xml` — common defaults.
3. For larger publications, look for **per-section feeds** (e.g. `/tech/rss.xml`, `/category/ai/feed/`). Prefer narrower section feeds over a firehose feed if the publication has a clear AI / tech section.
4. If the publication has an **official blog** distinct from a news outlet (e.g. `openai.com/news`, `anthropic.com/news`), prefer the blog feed — it is the primary source.

For each candidate URL, **`WebFetch`** it and confirm:

- HTTP 200 (or 301/302 → follow).
- `Content-Type` includes `xml`, `rss`, or `atom`.
- The body starts with `<?xml` or contains `<rss` / `<feed`.
- It has at least one `<item>` (RSS 2.0) or `<entry>` (Atom) with a `<title>` and `<link>`.

If you only find an Atom feed, note that — the current parser is **RSS 2.0 only** (see `scripts/rss-scraper/parser.ts`). Stop and tell the user: "The publication only ships Atom; the parser would need to grow Atom support before this adapter can ship. Should I leave a stub anyway, or skip?" Do not invent Atom support silently.

If no feed exists, stop and report. Do not write a placeholder adapter.

### Step 3 — Choose tags

Tags are adapter-provided labels attached to every item from a feed, used by downstream filtering (the sector skills). Pick 1-3 short kebab-case-or-lowercase tokens per feed. Patterns from existing adapters:

- A lab's own blog: `['ai', 'lab-primary-source']` (e.g. openai).
- A general tech publication: `['tech', 'ai-candidate']` for sections that might contain AI items.
- A business publication: `['business']` (e.g. bloomberg, the_information).
- A niche feed: a single descriptive tag (`['cybersec']`, `['fintech']`).

If you are unsure, ask the user. Don't invent vague tags like `news` or `general`.

### Step 4 — Write the adapter file

Write `${CLAUDE_PLUGIN_ROOT}/scripts/rss-scraper/adapters/<slug>.ts` following the existing pattern. Single-feed example:

```typescript
import type { Adapter } from '../types.ts'

/**
 * <One-sentence description of what this publication covers and why we
 * keep it: primary source vs aggregator, frequency, signal-to-noise.>
 */
export const <camelCaseSlug>: Adapter = {
  name: '<slug>',
  feeds: [
    {
      url: '<feed url>',
      tags: ['<tag1>', '<tag2>'],
    },
  ],
}
```

Multi-feed example (when the publication ships per-section feeds and we pull more than one):

```typescript
import type { Adapter } from '../types.ts'

/**
 * <Description.>
 */
export const <camelCaseSlug>: Adapter = {
  name: '<slug>',
  feeds: [
    { url: '<feed1>', tags: ['tech', 'ai-candidate'] },
    { url: '<feed2>', tags: ['business'] },
  ],
}
```

Notes:

- The exported variable uses **camelCase** of the slug (e.g. `theVerge` for slug `the_verge`).
- The `name` field is the slug exactly as it goes in `--source` filters and category configs — keep it snake_case.
- Imports use the `.ts` extension explicitly (the scraper runs with Node ≥ 23.6 native TS stripping).
- Only add `mapItem` if the feed has quirks that the default mapping can't handle (rare). Inspect `scripts/rss-scraper/fetcher.ts` for the default behavior before deciding.

### Step 5 — Register the adapter

Edit `${CLAUDE_PLUGIN_ROOT}/scripts/rss-scraper/registry.ts`:

1. Add the import alphabetically with the other adapter imports.
2. Append the camelCase variable to the `adapters` array.

Example after adding `the_verge`:

```typescript
import { bloomberg } from './adapters/bloomberg.ts'
import { newYorkTimes } from './adapters/new_york_times.ts'
import { openai } from './adapters/openai.ts'
import { techcrunch } from './adapters/techcrunch.ts'
import { theInformation } from './adapters/the_information.ts'
import { theVerge } from './adapters/the_verge.ts'
import type { Adapter } from './types.ts'

export const adapters: Adapter[] = [
  openai,
  techcrunch,
  bloomberg,
  theInformation,
  newYorkTimes,
  theVerge,
]
```

### Step 6 — Smoke-test

Run the scraper restricted to the new source and confirm it returns at least one parsed item. Pick a `--since` recent enough that the feed almost certainly has fresh content (last 7 days is safe):

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/rss-scraper/scrape.ts \
  --source <slug> \
  --since <YYYY-MM-DD seven days ago>
```

Verify:

- Exit code 0.
- stdout is valid JSON (parses cleanly).
- At least one item with non-empty `title` and `url`.
- `source` field equals the new slug.
- `publishedAt` parses to a real ISO date (not `null` for every item — that indicates a `pubDate`/`dc:date` format the parser doesn't handle).

If smoke test fails:

- **Empty array**: feed likely returned 0 items in the window — widen `--since`. If still empty, the URL may be stale; redo Step 2.
- **JSON parse error**: the feed is probably Atom (or malformed RSS). Reread Step 2's Atom note.
- **`publishedAt: null` everywhere**: the feed uses a date format the parser doesn't recognize. Tell the user; this needs a parser fix, not an adapter fix.

### Step 7 — Report back

Short confirmation:

```
adapter:  scripts/rss-scraper/adapters/<slug>.ts
registry: scripts/rss-scraper/registry.ts (added <camelCaseSlug>)
feeds:    <n> feed(s)
smoke:    <n> items in last 7 days
```

Mention that the new source is now usable as `--source <slug>` in the scraper and that any sector skill can opt into it by listing `<slug>` in its `sources` field.

## What you must NOT do

- Do not invent feed URLs. Every URL you write to the adapter file must have been fetched and verified in Step 2.
- Do not silently skip the smoke test. If you can't reach the network, tell the user and offer to register the adapter anyway with a flag.
- Do not edit `parser.ts`, `fetcher.ts`, `scrape.ts` or `types.ts` from this skill. Those are engine changes and require their own review. If the new source needs them, stop and report.
- Do not paste the feed contents into the conversation — quote the first item's title at most as evidence.
