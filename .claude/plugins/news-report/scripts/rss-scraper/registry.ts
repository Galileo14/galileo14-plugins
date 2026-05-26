import { bloomberg } from './adapters/bloomberg.ts'
import { newYorkTimes } from './adapters/new_york_times.ts'
import { openai } from './adapters/openai.ts'
import { techcrunch } from './adapters/techcrunch.ts'
import { theInformation } from './adapters/the_information.ts'
import type { Adapter } from './types.ts'

/**
 * Register every adapter here. The CLI uses `--source <name>` to filter
 * against `adapter.name`. To add a source, drop a file under `adapters/`
 * and append it to this list.
 */
export const adapters: Adapter[] = [
  openai,
  techcrunch,
  bloomberg,
  theInformation,
  newYorkTimes,
]
