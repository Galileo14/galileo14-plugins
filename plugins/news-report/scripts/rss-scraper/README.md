# rss-scraper

Standalone, zero-dep Node script. Pulls RSS feeds from registered adapters and
emits a homogeneous `NewsItem[]` as JSON. Designed to feed downstream tagging /
filtering for AI news (or any other segment).

Requires Node ≥ 23.6 for native TypeScript stripping (or `node --experimental-strip-types`
on 22.6+). Bun and `tsx` also work without changes — the imports use explicit
`.ts` extensions so any standard TS runner resolves them.

## Layout

```
scripts/rss-scraper/
├── scrape.ts                 # CLI entry
├── types.ts                  # NewsItem + Adapter shapes
├── parser.ts                 # zero-dep RSS 2.0 parser
├── fetcher.ts                # fetch all feeds of an adapter
├── registry.ts               # list of available adapters
└── adapters/
    └── <your_source>.ts      # add with /new-rss-source (none ship by default)
```

The plugin ships with **no adapters registered**. Add your own with the
`/new-rss-source` skill (or by hand — see "Adding a source" below) before
running the scraper.

## Usage

```bash
# everything
node scrape.ts

# one source only
node scrape.ts --source <source_name>

# filter by adapter-provided tag
node scrape.ts --tag ai-candidate

# filter by keyword in title/summary (comma-separated, case-insensitive)
node scrape.ts --keyword "AI,artificial intelligence,LLM"

# only items published on or after a given date (UTC)
node scrape.ts --since 2026-05-21

# write to file (creates parent dirs)
node scrape.ts --output reports/news.json
```

JSON goes to stdout; status messages go to stderr, so piping to a file is safe.

## Adding a source

The easy way is the **`/new-rss-source`** skill in this plugin — it discovers
the feed via `WebSearch` + `WebFetch`, writes the adapter, registers it and
smoke-tests it.

Manually:

1. Create `adapters/<source_name>.ts`.
2. Export an `Adapter` with `name`, `feeds` (and optionally `mapItem`).
3. Append it to `adapters` in `registry.ts`.

The adapter is free to:

- declare multiple feeds (e.g. one per section).
- attach `tags` per feed for downstream filtering (e.g. `['tech', 'ai-candidate']`).
- override `mapItem` for source-specific quirks (custom date parsing, summary
  cleanup, author extraction from non-standard fields, etc.).

## Output shape

```ts
type NewsItem = {
  source: string         // adapter slug, e.g. 'your_source'
  feedUrl: string        // origin feed
  title: string
  url: string
  publishedAt: Date | null
  summary: string | null
  author: string | null
  tags: string[]         // adapter/feed-provided
  categories: string[]   // verbatim from <category>
}
```
