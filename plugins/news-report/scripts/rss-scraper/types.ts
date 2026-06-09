/**
 * Homogeneous shape returned by every adapter.
 *
 * `tags` are adapter/feed-provided (e.g. 'tech', 'ai-relevant') — meant for
 * downstream filtering. `categories` are kept verbatim from the feed.
 */
export type NewsItem = {
  source: string
  feedUrl: string
  title: string
  url: string
  publishedAt: Date | null
  summary: string | null
  author: string | null
  tags: string[]
  categories: string[]
}

export type FeedConfig = {
  url: string
  tags?: string[]
}

export type RawRssItem = {
  title?: string
  link?: string
  description?: string
  pubDate?: string
  creator?: string
  guid?: string
  categories?: string[]
}

export type Adapter = {
  name: string
  feeds: FeedConfig[]
  /** Override for source-specific quirks. Defaults to a straight RSS → NewsItem map. */
  mapItem?: (raw: RawRssItem, feed: FeedConfig) => NewsItem
}
