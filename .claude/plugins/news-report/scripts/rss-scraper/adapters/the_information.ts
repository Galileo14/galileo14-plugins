import type { Adapter } from '../types.ts'

/**
 * The Information publishes an Atom feed. Articles are hard-paywalled, so
 * the RSS gives titles + short summaries only — useful for scoop detection,
 * not for full-text analysis.
 */
export const theInformation: Adapter = {
  name: 'the_information',
  feeds: [
    {
      url: 'https://www.theinformation.com/feed',
      tags: ['ai-candidate', 'insider', 'paywalled'],
    },
  ],
}
