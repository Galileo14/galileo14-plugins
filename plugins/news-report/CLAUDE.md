# CLAUDE.md — news-report plugin

Orientation for Claude when editing **inside this plugin directory**. The
user-facing overview lives in `README.md`; this file captures conventions,
load-bearing constraints and "don't touch" rules that are not obvious from
the file tree.

## What this plugin is

A Claude Code plugin that produces daily ranked news reports. Three layers:

1. **Engine** — `agents/news-pipeline.md` + `references/*` + `scripts/rss-scraper/`. Sector- and audience-agnostic.
2. **Sector skills** — `skills/generate-<sector>-report/`. User-invocable. Each carries the editorial opinion for one sector.
3. **Scaffolders** — `skills/new-report-skill/` (creates sector skills) and `skills/new-rss-source/` (adds RSS adapters).

Sector skills delegate to the engine via `Agent(subagent_type=news-pipeline)`. They never run the pipeline inline — keep that boundary intact.

## File naming

- Skills: `skills/<kebab-case-name>/SKILL.md`. Always exactly `SKILL.md`, never `skill.md` or `index.md`.
- Sector skills: `skills/generate-<sector>-report/SKILL.md`, where `<sector>` matches `^[a-z0-9-]{1,20}$`.
- RSS adapters: `scripts/rss-scraper/adapters/<snake_case>.ts`. The exported variable is **camelCase** of the same slug. The `name` field inside is the snake_case slug exactly — that's what `--source` filters on.
- References: lowercase descriptive filenames (`workflow.md`, `editorial-rules.md`, `report-template.md`). No `REFERENCE.md` / `TEMPLATE.md` shouting.

## Language conventions

- **Plugin artifacts in English**: SKILL.md bodies, agent system prompts, references, README, CLAUDE.md, plugin.json descriptions.
- **Exception** — the user-facing output language is per-skill. The skill's `Localization` block tells the engine to translate the produced `report.md` (e.g. `generate-ai-report` outputs Spanish). The skill body itself remains English; only the *report it produces* gets localized.
- Inside a localized report, proper nouns / URLs / ISO dates / YAML keys stay verbatim; everything else translates.

## Path conventions

- Inside SKILL.md and agent prompts, refer to plugin-internal files with `${CLAUDE_PLUGIN_ROOT}/...`. Claude Code expands the variable at runtime. The IDE will flag those links as broken — false positive, ignore.
- Inside references and scripts (relative to each other), use plain relative paths.
- Output paths (the scraper's `--output`, the report's `output_dir`) are relative to the **caller's CWD** (the repo where the user invoked Claude Code), not to the plugin root. Default is `content/news/<today>-<sector>/`.

## Adding things

| What | Use this |
|------|----------|
| New sector report | `/new-report-skill` (or copy `generate-ai-report/SKILL.md`) |
| New RSS source | `/new-rss-source` (or follow `scripts/rss-scraper/README.md`) |
| New rule that applies to every sector | Edit `references/editorial-rules.md` |
| New step in the pipeline | Edit `references/workflow.md` + `agents/news-pipeline.md` together |
| New template block in the report | Edit `references/report-template.md` + the heading translation table in every sector skill |

## Engine vs sector — which file gets the change

If a change makes sense for **every** sector (e.g. "always also write a JSON sidecar with rankings", "always run a final dedupe pass") → engine (`workflow.md` + `news-pipeline.md`).

If a change only makes sense for **one** sector (e.g. "the AI report should also surface model benchmarks separately") → that sector's SKILL.md.

When unsure, ask the user. Crossing the line accidentally turns the engine opinionated again.

## Scraper changes

The scraper (`scripts/rss-scraper/`) is the most fragile part of this plugin because external feeds change shape.

- **Adapters** (`adapters/*.ts`): safe to add via `/new-rss-source`. Safe to edit if a feed's URL changes.
- **`registry.ts`**: append-only in practice. Alphabetical imports, sector-order array.
- **`parser.ts`**: RSS 2.0 only. **Adding Atom support is a non-trivial change**; do not silently extend the parser. If a publication only ships Atom, escalate to the user.
- **`fetcher.ts` / `scrape.ts` / `types.ts`**: engine-level. Changes here affect every adapter and every sector skill. Treat them like API changes — propose, get a yes, then change.
- The scraper is **zero-dep on purpose**. Only `node:*` builtins. Adding an npm dep means losing portability across Bun / Node / tsx. Don't.
- Imports use explicit `.ts` extensions (required by stock Node ≥ 23.6 ESM resolver).

## Subagent contract

`agents/news-pipeline.md` declares the engine's input contract: sector, since, today, keywords, sources, top_n, output_dir, output_lang, audience (and an optional `focus` for skills that narrow the editorial scope further).

When you change any input field — adding, renaming, removing — you must:

1. Update `agents/news-pipeline.md` (the "What the caller sends you" table).
2. Update `references/workflow.md` (the "Inputs the caller must provide" table).
3. Update **every** existing sector skill's `Config` table and prompt block.
4. Update `skills/new-report-skill/SKILL.md` (the interview and the template).

Skipping step 3 or 4 silently breaks sector skills. There is no test suite; treat the inputs table as the source of truth and grep before claiming you're done.

## Things to NEVER do

- Reintroduce a slash command at the engine level (e.g. a default `/news-report`). The plugin design routes invocation through sector skills.
- Bake a specific audience or lens into the engine, references or template. That is the sector skill's job.
- Edit `routeTree.gen.ts` or anything else outside this directory from a plugin-internal change.
- Add npm dependencies to the scraper.
- Mutate files outside `skills/` from `/new-report-skill`, or outside `scripts/rss-scraper/adapters/` and `registry.ts` from `/new-rss-source`.
- Translate plugin artifacts to Spanish. Only the *reports* that sector skills generate get localized.

## When stuck

Re-read `references/workflow.md` first — the contract for the engine. Then the existing sector skill (`generate-ai-report/SKILL.md`) — it is the canonical example for any new sector skill. If still stuck, ask the user. Don't paper over a contradiction between layers; surface it.
