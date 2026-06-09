---
name: generate-ai-report
description: Research and generate a daily report on AI tools and products. Covers model releases, APIs, agents, developer tooling, platforms and SDKs that are actionable. Excludes geopolitics, macro, pure regulation and corporate moves with no product. Trigger with '/generate-ai-report', 'today's AI news', 'AI tooling roundup', 'what shipped in AI', 'report IA de hoy', 'novedades IA'.
user-invocable: true
---

# /generate-ai-report

Research today's news on **AI tools and products** and produce a ranked report with TL;DR + top stories.

> **Prerequisite**: this plugin ships with **no RSS adapters registered**. Add at least one AI-relevant source with `/new-rss-source` (e.g. `openai`, `anthropic`, `techcrunch`, `the_verge`, `simon_willison`, …) before invoking this skill. If `adapters` is empty the pipeline returns no items.

## Editorial focus

The report answers one question: **what new AI tool or product deserves the attention of someone who builds, tests, or adopts AI?**

In scope:

- New models (frontier or open-source), versions, variants, notable fine-tunes.
- APIs and SDKs (launches, pricing changes, relevant deprecations).
- Agents, coding agents, AI-native IDEs, copilots.
- Developer tooling: orchestration frameworks, eval, RAG, vector DBs, LLM observability, MCPs.
- Platforms (Anthropic, OpenAI, Google, Meta, Mistral, DeepSeek, xAI…) and their features.
- Benchmarks, papers or techniques with public implementation.
- Enterprise use cases with an identifiable product.

Out of scope:

- AI politics, geopolitics, regulation without a product.
- Market macro, IPOs as financial topic, valuations.
- M&A or earnings without a concrete launch.
- Hype with nothing available to try / read / use.
- Twitter drama / opinion debates.

## Config

| Field          | Value                                                                                     |
| -------------- | ----------------------------------------------------------------------------------------- |
| `sector`       | `ai`                                                                                      |
| `window`       | Default: yesterday + today (UTC). `since = today − 1`. Override if the user asks.         |
| `keywords`     | `AI, A.I., artificial intelligence, machine learning, LLM, large language model, GPT, ChatGPT, Claude, Gemini, OpenAI, Anthropic, DeepMind, Mistral, DeepSeek, xAI, agent, agentic, RAG, embedding, fine-tuning, generative, neural network` |
| `sources`      | `[]` by default → use every adapter registered in `scripts/rss-scraper/registry.ts`. Override with `--sources slug1,slug2` to restrict to a subset. |
| `top_n`        | `5` by default.                                                                           |
| `output_dir`   | `content/news/<today>-ai/`                                                                |
| `output_lang`  | `es` — write the report in Spanish (see localization note below).                        |
| `audience`     | People who build, evaluate or adopt AI tools: developers, builders, technical decision-makers, platform teams, technical founders. The "Why it matters" block answers: what does this change for someone building with AI? Is it something to try today, something to watch, or noise? What concrete problem does it solve or unblock? Pragmatic tone, no hype. |

## What to do when invoked

Delegate execution to the `news-pipeline` subagent with the config above.

```
Agent(
  subagent_type: news-pipeline,
  prompt: """
    sector: ai
    since: <today − 1 in UTC, unless overridden>
    today: <UTC YYYY-MM-DD>
    keywords: AI, A.I., artificial intelligence, machine learning, LLM, large language model, GPT, ChatGPT, Claude, Gemini, OpenAI, Anthropic, DeepMind, Mistral, DeepSeek, xAI, agent, agentic, RAG, embedding, fine-tuning, generative, neural network
    sources: (all)
    top_n: 5
    output_dir: content/news/<today>-ai/
    output_lang: es
    focus: |
      AI tools and products only. Models, APIs, SDKs, agents, developer tooling,
      platforms, frameworks, benchmarks with public implementation. Exclude
      geopolitics, pure regulation, macro, M&A without product, hype without launch.
    audience: |
      Developers, builders, technical decision-makers and technical founders who
      build, evaluate or adopt AI tools.
      In "Why it matters" answer: what does this change for someone building
      with AI? Is it something to try today, something to watch, or noise? What
      concrete problem does it solve or unblock? Pragmatic tone, no hype.
  """
)
```

## Localization

**Write the final `report.md` fully in Spanish (`es`).** The source articles come mostly in English from the RSS feeds — translate every piece of content to Spanish before writing it into the report. That includes:

- TL;DR bullets.
- "Foco del día" paragraph.
- Each story's "Qué pasó", "Contexto adicional" and "Por qué importa" prose.
- Story titles (translate the headline; keep the original in parentheses only if the translation loses meaning, e.g. product names).
- One-sentence descriptors next to each link in "Fuentes adicionales".
- Headlines listed in "Resto del día".

What stays in the original language:

- Proper nouns (company names, product names, model names, people's names).
- Verbatim quotes — translate the quote but keep the original between quotation marks if it carries weight.
- URLs, source identifiers, ISO dates.
- YAML frontmatter keys.

Translate every section heading and field label as follows:

| English (template)   | Spanish (output)    |
| -------------------- | ------------------- |
| TL;DR                | TL;DR               |
| Today's focus        | Foco del día        |
| Top stories          | Top stories         |
| Source               | Fuente principal    |
| Published            | Publicado           |
| What happened        | Qué pasó            |
| Additional context   | Contexto adicional  |
| Additional sources   | Fuentes adicionales |
| Why it matters       | Por qué importa     |
| Rest of the day      | Resto del día       |

Tone: Spain Spanish, technical-pragmatic, no anglicism overuse ("herramienta" not "tool", "lanzamiento" not "release" when natural). Keep terms of art untranslated when there is no idiomatic Spanish equivalent (LLM, embedding, fine-tuning, agent, MCP, etc.).

## Common overrides

- `/generate-ai-report --since 2026-05-20` → wider window.
- `/generate-ai-report --top 8` → more stories.
- `/generate-ai-report --sources slug1,slug2` → restrict to a subset of registered adapters (use the slugs from `scripts/rss-scraper/registry.ts`).

When the user passes overrides, substitute them in the subagent prompt.
