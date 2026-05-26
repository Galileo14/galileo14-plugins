#!/usr/bin/env bun
/**
 * Scrape RSS feeds from every registered adapter and emit a homogeneous
 * `NewsItem[]` as JSON.
 *
 *   bun run scripts/rss-scraper/scrape.ts
 *   bun run scripts/rss-scraper/scrape.ts --source new_york_times
 *   bun run scripts/rss-scraper/scrape.ts --tag ai-candidate
 *   bun run scripts/rss-scraper/scrape.ts --keyword "AI,artificial intelligence"
 *   bun run scripts/rss-scraper/scrape.ts --output reports/news.json
 */
import { writeFile } from 'node:fs/promises'
import { dirname } from 'node:path'
import { mkdir } from 'node:fs/promises'
import { parseArgs } from 'node:util'
import { fetchAdapter } from './fetcher.ts'
import { adapters } from './registry.ts'
import type { NewsItem } from './types.ts'

const { values } = parseArgs({
  options: {
    source: { type: 'string' },
    tag: { type: 'string' },
    keyword: { type: 'string' },
    since: { type: 'string' },
    output: { type: 'string' },
  },
})

const since = values.since ? parseSince(values.since) : null

const selected = values.source
  ? adapters.filter((a) => a.name === values.source)
  : adapters

if (selected.length === 0) {
  console.error(`unknown source: ${values.source}`)
  console.error(`available: ${adapters.map((a) => a.name).join(', ')}`)
  process.exit(1)
}

const all = (await Promise.all(selected.map(fetchAdapter))).flat()

const filtered = applyFilters(all, {
  tag: values.tag,
  keywords: values.keyword?.split(',').map((s) => s.trim().toLowerCase()).filter(Boolean),
  since,
})

const sorted = filtered.sort((a, b) => {
  const ta = a.publishedAt?.getTime() ?? 0
  const tb = b.publishedAt?.getTime() ?? 0
  return tb - ta
})

const payload = JSON.stringify(sorted)

if (values.output) {
  await mkdir(dirname(values.output), { recursive: true })
  await writeFile(values.output, payload, 'utf8')
  console.error(`wrote ${sorted.length} items → ${values.output}`)
} else {
  console.log(payload)
  console.error(`${sorted.length} items`)
}

function applyFilters(
  items: NewsItem[],
  opts: { tag?: string; keywords?: string[]; since?: Date | null },
): NewsItem[] {
  return items.filter((item) => {
    if (opts.tag && !item.tags.includes(opts.tag)) return false
    if (opts.keywords?.length) {
      const haystack = `${item.title} ${item.summary ?? ''}`.toLowerCase()
      if (!opts.keywords.some((k) => haystack.includes(k))) return false
    }
    if (opts.since) {
      if (!item.publishedAt || item.publishedAt < opts.since) return false
    }
    return true
  })
}

function parseSince(value: string): Date {
  const d = new Date(value.length === 10 ? `${value}T00:00:00Z` : value)
  if (Number.isNaN(d.getTime())) {
    console.error(`invalid --since: ${value}`)
    process.exit(1)
  }
  return d
}
