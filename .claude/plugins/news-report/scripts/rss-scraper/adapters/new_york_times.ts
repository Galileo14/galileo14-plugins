import type { Adapter } from '../types.ts'

/**
 * The New York Times publishes per-section RSS 2.0 feeds at
 * https://rss.nytimes.com. They don't ship a dedicated AI feed, so we pull
 * Technology + Business and tag them — downstream filters do the rest.
 */
export const newYorkTimes: Adapter = {
  name: 'new_york_times',
  feeds: [
    {
      url: 'https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml',
      tags: ['tech', 'ai-candidate'],
    },
    {
      url: 'https://rss.nytimes.com/services/xml/rss/nyt/Business.xml',
      tags: ['business'],
    },
  ],
}
