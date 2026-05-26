import { parseFeed } from './parser.ts'
import type { Adapter, FeedConfig, NewsItem, RawRssItem } from './types.ts'

/**
 * Fetch every feed declared by an adapter and return the mapped, homogeneous
 * `NewsItem` list. Per-feed failures are logged and skipped so one broken
 * feed doesn't take down the whole run.
 */
export async function fetchAdapter(adapter: Adapter): Promise<NewsItem[]> {
  const mapItem = adapter.mapItem ?? defaultMapItem(adapter.name)

  const results = await Promise.all(
    adapter.feeds.map(async (feed) => {
      try {
        const res = await fetch(feed.url, {
          headers: { 'user-agent': 'g14-rss-scraper/0.1' },
        })
        if (!res.ok) {
          console.error(`[${adapter.name}] ${feed.url} → HTTP ${res.status}`)
          return []
        }
        const xml = await res.text()
        return parseFeed(xml).map((raw) => mapItem(raw, feed))
      } catch (err) {
        console.error(`[${adapter.name}] ${feed.url} → ${(err as Error).message}`)
        return []
      }
    }),
  )

  return results.flat()
}

function defaultMapItem(source: string) {
  return (raw: RawRssItem, feed: FeedConfig): NewsItem => ({
    source,
    feedUrl: feed.url,
    title: raw.title ?? '',
    url: raw.link ?? '',
    publishedAt: raw.pubDate ? new Date(raw.pubDate) : null,
    summary: raw.description ?? null,
    author: raw.creator ?? null,
    tags: [...(feed.tags ?? [])],
    categories: raw.categories ?? [],
  })
}
