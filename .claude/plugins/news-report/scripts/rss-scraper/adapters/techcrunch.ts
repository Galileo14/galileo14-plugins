import type { Adapter } from '../types.ts'

/**
 * TechCrunch ships per-category RSS 2.0 feeds. The AI category covers
 * funding rounds, product launches and deals — full content in feed.
 */
export const techcrunch: Adapter = {
  name: 'techcrunch',
  feeds: [
    {
      url: 'https://techcrunch.com/category/artificial-intelligence/feed/',
      tags: ['ai', 'tech'],
    },
  ],
}
