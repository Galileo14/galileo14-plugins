# news-report

Sector-agnostic engine for daily news reports. A generic pipeline
(scrape → filter → enrich → rank → write) exposed through per-sector skills
that you author yourself or scaffold interactively.

## Three-layer model

```
┌─ Engine (this plugin) ────────────────────────┐
│  scripts/rss-scraper/    Node-based RSS       │
│  agents/news-pipeline.md Engine subagent      │
│  references/             Workflow + rules     │
└───────────────────────────────────────────────┘
                     ▲ delegates to
                     │
┌─ Sector skills (consumer-facing) ─────────────┐
│  /generate-ai-report                          │
│  /generate-fintech-report     (example)       │
│  /generate-cybersec-report    (example)       │
│                                               │
│  Each declares: sector slug, time window,     │
│  keywords, sources, audience lens, top_n,     │
│  output language.                             │
└───────────────────────────────────────────────┘
                     ▲ scaffolded by
                     │
┌─ Scaffolders (meta) ──────────────────────────┐
│  /new-report-skill   Wizard to add sectors    │
│  /new-rss-source     Wizard to add adapters   │
└───────────────────────────────────────────────┘
```

The engine has no opinion on what counts as news. Each sector skill carries
that opinion (audience lens, in-scope / out-of-scope, output language).

## Layout

```
news-report/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── CLAUDE.md                            # Orientation for Claude when editing the plugin
├── README.md                            # This file
├── agents/
│   └── news-pipeline.md                 # Delegable engine subagent
├── references/
│   ├── workflow.md                      # 5-step pipeline
│   ├── editorial-rules.md               # Filter, ranking, enrichment, hard rules
│   └── report-template.md               # Markdown skeleton with EN headings
├── scripts/
│   └── rss-scraper/                     # Zero-dep Node RSS scraper
└── skills/
    ├── generate-ai-report/SKILL.md      # First sector skill (es output)
    ├── new-report-skill/SKILL.md        # Wizard: add a sector
    └── new-rss-source/SKILL.md          # Wizard: add an RSS adapter
```

## Invocation surfaces

- **Slash command** — every user-invocable skill exposes its own (`/generate-ai-report`, `/new-report-skill`, `/new-rss-source`).
- **Keyword auto-activation** — phrases declared in each skill's `description`.
- **Subagent** — `Agent(subagent_type=news-pipeline)` with a config prompt; useful for parallel multi-sector runs.

## How a sector report is produced

1. User invokes a sector skill (e.g. `/generate-ai-report`).
2. The skill body assembles config (sector, window, keywords, sources, audience, top_n, output_lang) and delegates to `Agent(subagent_type=news-pipeline)`.
3. The subagent reads `references/workflow.md`, `editorial-rules.md` and `report-template.md`, then:
   1. Runs the scraper (`node scripts/rss-scraper/scrape.ts`) for the requested window.
   2. Shortlists candidates (1.5× `top_n`).
   3. Enriches each candidate in parallel with `WebFetch` (article facts) + `WebSearch` (triangulation).
   4. Ranks and writes `report.md` per the template, translating to `output_lang` if needed.
4. The subagent returns a 3-line summary (path, scraped, ranked). The main agent relays it.

Output lives in `content/news/<YYYY-MM-DD>-<sector>/`.

## Add a sector skill

Easy way — run **`/new-report-skill`**. Interactive interview: sector slug,
topic focus, in-scope / out-of-scope examples, audience lens, time window,
keywords, sources, top_n, output language, trigger phrases. Writes a ready
SKILL.md under `skills/generate-<sector>-report/`.

Manual way: copy `skills/generate-ai-report/SKILL.md` and adjust every field.

## Add an RSS source

Easy way — run **`/new-rss-source`**. Asks for the publication, discovers
the feed via `WebSearch` + `WebFetch`, writes the adapter, registers it in
`registry.ts`, smoke-tests `node scrape.ts --source <slug> --since <recent>`.

Manual way: see `scripts/rss-scraper/README.md`.

## Runtime requirements

- Node ≥ 23.6 (native TypeScript stripping). On 22.6+ use `node --experimental-strip-types`. Bun and `tsx` also work — the scraper uses explicit `.ts` import extensions.

## Versioning

- `0.1.0` — initial conversion from skill to plugin.
- `0.2.0` — sector-agnostic engine + `/generate-ai-report` + scaffolders. Breaking: `/news-report` no longer exists, use a sector skill.
