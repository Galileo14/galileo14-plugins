import type { Adapter } from './types.ts'

/**
 * Register every adapter here. The CLI uses `--source <name>` to filter
 * against `adapter.name`. To add a source, drop a file under `adapters/`
 * and append it to this list (or use the `/new-rss-source` skill).
 *
 * Empty by default — this plugin ships without preconfigured RSS sources.
 */
export const adapters: Adapter[] = []
