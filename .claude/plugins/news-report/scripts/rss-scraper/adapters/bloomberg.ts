import type { Adapter } from '../types.ts'

/**
 * Bloomberg Technology RSS 2.0. Feed is free; the article body on the web
 * is paywalled. Use this for macro / markets / deals signal — title and
 * snippet are usually enough to triage.
 */
export const bloomberg: Adapter = {
  name: 'bloomberg',
  feeds: [
    {
      url: 'https://feeds.bloomberg.com/technology/news.rss',
      tags: ['tech', 'business', 'ai-candidate'],
    },
  ],
}
