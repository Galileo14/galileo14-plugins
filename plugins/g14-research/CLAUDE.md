# research plugin — architecture

Research and intelligence gathering for Galileo14. Four user-facing **skills** (quick recon, exhaustive deep-dive, fact verification, company dossier) — all powered by **15 reusable agents** at the plugin root. Skills orchestrate; agents do the work.

## The shape

```
plugins/research/
├── agents/
│   ├── web-searcher.md                 ← generic web research primitive
│   ├── research-synthesizer.md         ← N findings → 1 output (4 formats)
│   ├── hallucination-grader.md         ← fresh-context claim verifier
│   ├── source-validator.md             ← URL reachability + domain coherence
│   ├── website-crawler.md              ← company's own domain
│   ├── google-researcher.md            ← what Google says about a company
│   ├── linkedin-researcher.md          ← corporate LinkedIn footprint
│   ├── reddit-researcher.md            ← Reddit sentiment + threads
│   ├── trustpilot-researcher.md        ← customer reviews aggregate
│   ├── google-maps-researcher.md       ← local reputation + locations
│   ├── glassdoor-researcher.md         ← employee voice on Glassdoor (recommend %, CEO approval)
│   ├── indeed-researcher.md            ← employee voice on Indeed (hourly + operational roles)
│   ├── youtube-researcher.md           ← audiovisual presence
│   ├── news-researcher.md              ← press / Google News
│   └── crunchbase-researcher.md        ← funding + investors + headcount
└── skills/
    ├── g14-quick-search/                   ← 5 angles, panoramic recap (~250 words)
    ├── g14-fact-check/                     ← 10 evidence angles + verdict
    ├── g14-deep-search/                    ← 50 queries → markdown report (3000-5000 words)
    └── g14-company-analysis/               ← 11 platforms → branded HTML dossier
```

## The norm — agents own, skills compose

**Knowledge lives in agents. Skills are thin orchestrators.** A skill captures input, plans the work (which agents, with what inputs), fires them in parallel, and assembles results. Skills never duplicate platform methodology, source taxonomy, anti-hallucination rules, output formats, or verdict logic — that all lives in agents.

| Concept | Owner (single source of truth) | Skills that consume it |
|---|---|---|
| **Generic web research** (queries → findings) | `web-searcher` agent | g14-quick-search (5×), g14-fact-check (10×), g14-deep-search (10×) |
| **Per-platform methodology** (LinkedIn, Reddit, Trustpilot, Glassdoor, Indeed, etc.) | 11 platform-researcher agents | g14-company-analysis (1× each) |
| **Synthesis** (N findings → output) | `research-synthesizer` agent (4 formats) | all 4 skills |
| **Claim-level hallucination check** | `hallucination-grader` agent | g14-company-analysis; g14-deep-search (optional) |
| **URL-level reachability check** | `source-validator` agent | g14-company-analysis; g14-deep-search + g14-fact-check (optional) |
| **Source tier taxonomy** (Tier 1/2/3) | `web-searcher` agent | all 4 skills |
| **Canonical research angles** (verbatim, counter-evidence, primary-source, peer-reviewed, fact-checker, etc.) | `web-searcher` agent | g14-fact-check, g14-deep-search, g14-quick-search |

**Intentional duplication.** The "URL extraction for named entities" pattern (People → LinkedIn; Companies → official domain; Articles → canonical URL; etc.) is repeated verbatim across all 11 platform researchers. This is deliberate: each agent must be self-contained, and the rules are short enough that the cost of duplication is lower than the cost of an extra Read per invocation × 11 parallel calls. If you change the pattern, propagate it to all 11.

Each skill keeps what is genuinely skill-specific: its workflow, how many agents to fire, with what angles, the output destination, the resume logic, the user-facing presentation.

## Skill → agents map

| Skill | Agents invoked |
|---|---|
| **g14-quick-search** | 5× `web-searcher` (panoramic angles, inline) → 1× `research-synthesizer` (format: `inline-summary`) |
| **g14-fact-check** | 10× `web-searcher` (evidence angles, inline) → 1× `research-synthesizer` (format: `verdict`) → optional `source-validator` |
| **g14-deep-search** | 10× `web-searcher` (thematic angles × 5 queries each, file) → 1× `research-synthesizer` (format: `markdown`) → optional `hallucination-grader` + `source-validator` |
| **g14-company-analysis** | 1× of each of the 11 platform-researchers (file) → 1× `research-synthesizer` (format: `html-template`) → `hallucination-grader` + `source-validator` (mandatory) |

## Parallelization

Every skill's "Critical rules" section documents which agent calls fire in parallel. The non-negotiable rule: **independent agent calls go in one message** with multiple `Task` tool uses.

- **g14-quick-search**: 5 `web-searcher` calls in one message → then 1 synthesizer.
- **g14-fact-check**: 10 `web-searcher` calls in one message → then 1 synthesizer.
- **g14-deep-search**: 10 `web-searcher` calls in one message → then 1 synthesizer → optional 2 graders in one message.
- **g14-company-analysis**: 11 platform-researcher calls in one message → then 1 synthesizer → 2 graders in one message.

The difference between parallel and serial here is 30 seconds vs. 5 minutes for the most complex skill.

## Model + effort per agent

| Agent | model | effort | Why |
|---|---|---|---|
| 11 platform researchers | haiku | low | Bounded scope per platform, parallel fan-out |
| `web-searcher` | haiku | low | Same — bounded per-angle work |
| `research-synthesizer` | haiku | medium | Synthesis benefits from a bit more thinking budget |
| `hallucination-grader` | haiku | high | Careful claim-by-claim cross-referencing |
| `source-validator` | haiku | medium | Lots of small fetches + classification |

All agents default to Haiku — the plugin is designed for cost/latency. Skills may escalate a single failing call to `sonnet` as a one-off retry, but never default to it.

## Adding to the plugin

**New platform researcher** if: a new data source becomes important enough that g14-company-analysis (or another skill) needs it as a first-class signal, with platform-specific search syntax / pitfalls / signal taxonomy.

**New utility agent** if: two or more skills duplicate the same cross-cutting concern that isn't already covered by the four utilities.

**New skill** if: a distinct user-facing artifact or workflow that doesn't fit the four existing ones. Reuse the existing agents; do not extract a fork of an agent into a skill.

When adding either, update this file's tree and the ownership table.
