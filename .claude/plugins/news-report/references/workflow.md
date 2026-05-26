# news-report — Pipeline

Generic five-step pipeline shared by every sector skill of this plugin. The
calling skill provides the editorial config (sector slug, time window,
keywords, sources, audience lens, story count, output path, output language).
This file describes only the mechanics.

## Inputs the caller must provide

| Field          | Description                                                                 |
| -------------- | --------------------------------------------------------------------------- |
| `sector`       | Short slug used in output paths (e.g. `ai`, `fintech`, `cybersec`).         |
| `since`        | UTC `YYYY-MM-DD`. Lower bound for items.                                    |
| `today`        | UTC `YYYY-MM-DD`. Used to name the output folder.                           |
| `keywords`     | Comma-separated list passed to the scraper's `--keyword`. Empty → no filter.|
| `sources`      | Optional subset of adapter names. Empty → all registered adapters.          |
| `audience`     | One-paragraph description of who this report is for + the lens to apply.   |
| `top_n`        | Number of ranked stories in the final report. Default `5`.                 |
| `output_dir`   | Where to write `news.json` and `report.md`. Default `content/news/<today>-<sector>/`. |
| `output_lang`  | Language for the generated `report.md` (e.g. `en`, `es`). Default `en`.    |

## Pipeline

### 1. Resolve the window

- `today` = UTC `YYYY-MM-DD`. `since` = caller-provided (or `today` − 1 day).
- If `<output_dir>/report.md` already exists, ask the user before overwriting.

### 2. Scrape

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/rss-scraper/scrape.ts \
  --since <since> \
  --keyword "<keywords>" \
  --output <output_dir>/news.json
```

- Omit `--keyword` if `keywords` is empty.
- If `sources` is set, filter the resulting JSON by `item.source ∈ sources` and rewrite the file (the scraper takes a single `--source`, not a list).

Requires Node ≥ 23.6 (TypeScript stripping enabled by default). On 22.6+ use `node --experimental-strip-types`. Bun and `tsx` also work.

### 3. Shortlist and enrich

Apply the [editorial filter and ranking criteria](editorial-rules.md#filter-and-ranking) over `news.json` and build a shortlist of **1.5× `top_n`** candidates.

For each candidate, **in parallel**:

- **`WebFetch(url, ...)`** on the original article — extract concrete facts (what launched, dates, figures, integrations, availability, benchmarks). [Suggested prompt](editorial-rules.md#enrichment-prompts).
- **`WebSearch(query)`** on the **topic** (not the article) — triangulate with release notes, official blogs, Hacker News, product docs, technical reactions. 1-3 searches per candidate. [Useful queries](editorial-rules.md#triangulation-queries).

Consolidate a dossier per candidate (facts + nuances + extra URLs). Only after that, drop the weak ones and fix the final list. [Failure handling](editorial-rules.md#failure-handling).

### 4. Write the report

Produce `<output_dir>/report.md` following [`report-template.md`](report-template.md), using the dossier (not the RSS snippets).

Hard rules:

- `top_n` stories by default. More only if the user explicitly asks.
- TL;DR: 2-4 bullets, ≤25 words, facts not opinion.
- "What happened": 3-6 sentences with high informational density (figures, names, dates, availability).
- "Why it matters": apply the caller's `audience` lens.
- Write the report in `output_lang`. When `output_lang` is not English, translate **everything** that the report produces — section headings, field labels, TL;DR bullets, narrative prose, story titles, link descriptors, "Rest of the day" headlines. Keep proper nouns (companies, products, models, people), URLs, ISO dates and YAML keys in their original form. The source articles will mostly arrive in English from the RSS feeds; do not paste English fragments into the final report.
- Never invent data. Attribute key figures to their concrete source.

Detailed per-block rules in [editorial-rules.md → Report rules](editorial-rules.md#report-rules).

### 5. Report back

Short output to the user: path to `report.md`, items scraped, items ranked.

## Output structure

```
<output_dir>/
├── news.json       # raw scraper output (NewsItem[])
└── report.md       # final structured report
```
