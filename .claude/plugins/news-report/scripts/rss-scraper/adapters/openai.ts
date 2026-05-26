import type { Adapter } from '../types.ts'

/**
 * Primary-source RSS 2.0 from openai.com/news. Low frequency, high signal:
 * product launches, research posts, safety statements.
 */
export const openai: Adapter = {
  name: 'openai',
  feeds: [
    {
      url: 'https://openai.com/news/rss.xml',
      tags: ['ai', 'lab-primary-source'],
    },
  ],
}
