---
date: {{YYYY-MM-DD}}
sector: {{sector slug}}
sector_label: {{human-readable sector name}}
window: "{{since}} → {{today}}"
sources_used: [{{adapters actually used}}]
items_scraped: {{n}}
items_ranked: {{1-N, default 5}}
generated_at: {{ISO 8601 UTC}}
---

# Daily news — {{sector_label}} ({{YYYY-MM-DD}})

## TL;DR

- {{Bullet 1 — what happened, ≤25 words}}
- {{Bullet 2}}
- {{Bullet 3}}
- {{Bullet 4 optional}}

## Today's focus

{{2-4 sentences about story #1: what happened, why it matters for the caller's `audience`, what changes. Don't copy the feed summary — synthesize from the full dossier (WebFetch + WebSearch).}}

## Top stories

### 1. {{Title}}

- **Source:** {{source}} · [{{domain}}]({{url}})
- **Published:** {{ISO date}}
- **What happened:** {{3-6 sentences. Concrete facts from the full article and triangulation: what launched/was announced, dates, figures, integrations, availability (GA/beta/waitlist/region), benchmarks or quoted metrics, proper nouns, prices. No opinion.}}
- **Additional context:** {{1-3 sentences with what other channels add: official statement, relevant technical reactions, community debates, third-party benchmarks, nuances the original article misses. Omit if no signal.}}
- **Additional sources:**
  - [{{Short title / domain}}]({{url}}) — {{what it adds, in one sentence}}
  - [{{Short title / domain}}]({{url}}) — {{what it adds}}
  {{0-4 entries; omit the whole block if nothing adds value}}
- **Why it matters:** {{2-3 sentences. Implication through the caller's `audience` lens — what would that audience actually do with this?}}

### 2. {{Title}}

{{same structure}}

{{Repeat up to `top_n` (default 5; more only if the user explicitly asks). If only 1 story is relevant, keep only 1 — don't pad.}}

## Rest of the day (optional)

{{Flat list of 0-10 remaining headlines with link, no commentary, ordered by source. Omit this section if no signal.}}

---

**Localization:** if the caller sets `output_lang` to a non-English language, translate every section heading and field label above (`TL;DR`, `Today's focus`, `Top stories`, `Source`, `Published`, `What happened`, `Additional context`, `Additional sources`, `Why it matters`, `Rest of the day`) and write the body in that language. Keep YAML keys in English.
