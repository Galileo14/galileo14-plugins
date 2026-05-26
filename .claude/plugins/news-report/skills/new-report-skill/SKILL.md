---
name: new-report-skill
description: Scaffold a new sector-specific news report skill (generate-X-report) by interviewing the user about topic, audience, sources, time window, output language and how to organize the final report. Writes a ready-to-use SKILL.md inside the news-report plugin. Trigger with '/new-report-skill', 'crear nueva skill de report', 'añade un sector al news report', 'nueva skill de noticias', 'scaffold report skill'.
user-invocable: true
---

# /new-report-skill

Interactive wizard that creates a new sector-specific news report skill inside this plugin. The output is a ready-to-use `generate-<sector>-report` SKILL.md, modeled after `generate-ai-report`.

Use this when the user wants to add a new sector (fintech, cybersec, devops, climate, biotech…) to the news-report plugin without copying files by hand.

## What you (Claude) must do when invoked

Run the interview, validate the answers, write the file, and report back. Do not skip questions or invent answers — every field becomes part of the final skill.

### Step 1 — Interview the user

Use `AskUserQuestion` to gather these inputs. Batch related questions where possible, but never ask more than 4 questions at once. Open-ended answers (text) go through follow-up turns where AskUserQuestion isn't a fit — ask in plain text.

**Required fields:**

1. **`sector`** — short kebab-case slug used in the skill name and output paths. Examples: `fintech`, `cybersec`, `devops`, `climate`, `biotech`. Validate: lowercase letters, digits and hyphens only, ≤20 chars.

2. **One-sentence topic focus** — what kind of news does this report cover? (Free text.)

3. **In-scope examples (3-6 bullets)** — concrete categories of news that DO belong in this report. (Free text, bulletable.)

4. **Out-of-scope examples (3-6 bullets)** — what to explicitly exclude. (Free text.)

5. **Audience** — one paragraph describing who reads this report and the lens to apply in "Why it matters". This is the most important field — the engine writes the "Por qué importa" block from this. (Free text.)

6. **Default time window** — AskUserQuestion with options: "Yesterday + today (24h)", "Last 3 days", "Last week", "Custom".

7. **Keywords for the scraper filter** — comma-separated list, or "no filter" to pull every item from every adapter. (Free text.)

8. **Sources restriction** — AskUserQuestion: "All registered adapters" / "Specific subset (you'll list them)". If subset: ask for the list. The current registered adapters can be read from `${CLAUDE_PLUGIN_ROOT}/scripts/rss-scraper/registry.ts`; quote them as options when relevant.

9. **`top_n` default** — AskUserQuestion: "3", "5", "8", "Other".

10. **Output language** — AskUserQuestion: "English (en)", "Spanish (es)", "Other (specify ISO code)".

11. **Trigger phrases** — 3-6 short phrases that should auto-activate this skill by keyword matching (e.g. "report fintech de hoy", "novedades cybersec"). (Free text.) Always include `/<skill-slug>` as one trigger.

### Step 2 — Compute the skill slug

`slug = generate-<sector>-report` (e.g. `generate-fintech-report`).

Check that `${CLAUDE_PLUGIN_ROOT}/skills/<slug>/` does not exist. If it does, ask the user before overwriting.

### Step 3 — Write the SKILL.md

Write the file at `${CLAUDE_PLUGIN_ROOT}/skills/<slug>/SKILL.md` using the template below. Substitute every `{{placeholder}}` with the interview answers. Keep the file structure and headings identical so the engine and the user can navigate consistently.

The body of the SKILL.md must be in English (plugin artifact convention). Only the **Localization** block — and only when `output_lang != en` — describes how to translate the final report; that block can name target-language headings as needed.

### Step 4 — Report back

Short confirmation, nothing more:

```
created: .claude/plugins/news-report/skills/<slug>/SKILL.md
invoke:  /<slug>     or one of the trigger phrases
```

Tell the user to restart Claude Code (or reload the plugin) so the new slash command becomes visible.

---

## SKILL.md template

Substitute every `{{...}}` placeholder with the interview answers. Remove the comment lines starting with `<!--` after writing.

````markdown
---
name: {{slug}}
description: {{One-sentence topic focus, expanded to include 'Covers <in-scope categories>. Excludes <out-of-scope>.' Append: 'Trigger with <comma-separated trigger phrases>.'}}
user-invocable: true
---

# /{{slug}}

{{One-sentence topic focus.}}

## Editorial focus

The report answers one question: **{{rephrase the focus as a question, e.g. "what new fintech product or API deserves the attention of someone who builds, runs or invests in financial software?"}}**

In scope:

{{Bullet list of in-scope examples, one per line, prefixed with `- `.}}

Out of scope:

{{Bullet list of out-of-scope examples, one per line, prefixed with `- `.}}

## Config

| Field          | Value                                                                                     |
| -------------- | ----------------------------------------------------------------------------------------- |
| `sector`       | `{{sector}}`                                                                              |
| `window`       | {{Default window in plain English, e.g. "yesterday + today (UTC). `since = today − 1`. Override if the user asks."}} |
| `keywords`     | {{Comma-separated keyword list, or `(empty — no keyword filter)`}}                       |
| `sources`      | {{`Empty → all registered adapters.` OR `Subset: <comma-separated adapter names>`}}      |
| `top_n`        | `{{top_n}}` by default.                                                                   |
| `output_dir`   | `content/news/<today>-{{sector}}/`                                                        |
| `output_lang`  | `{{output_lang}}`                                                                         |
| `audience`     | {{Audience paragraph, verbatim from the interview.}}                                     |

## What to do when invoked

Delegate execution to the `news-pipeline` subagent with the config above.

```
Agent(
  subagent_type: news-pipeline,
  prompt: """
    sector: {{sector}}
    since: <computed from window>
    today: <UTC YYYY-MM-DD>
    keywords: {{keywords or '(none)'}}
    sources: {{'(all)' or comma-separated list}}
    top_n: {{top_n}}
    output_dir: content/news/<today>-{{sector}}/
    output_lang: {{output_lang}}
    focus: |
      {{One-sentence focus + the in-scope / out-of-scope summary, condensed
      to 2-4 lines.}}
    audience: |
      {{Audience paragraph from the interview.}}
  """
)
```

{{If output_lang != en, include the Localization block below. Otherwise omit it entirely.}}

## Localization

**Write the final `report.md` fully in {{language name}} (`{{output_lang}}`).** The source articles come mostly in English from the RSS feeds — translate every piece of content before writing it into the report. That includes:

- TL;DR bullets.
- "{{translated 'Today's focus'}}" paragraph.
- Each story's "{{translated 'What happened'}}", "{{translated 'Additional context'}}" and "{{translated 'Why it matters'}}" prose.
- Story titles (translate the headline; keep the original in parentheses only if the translation loses meaning, e.g. product names).
- One-sentence descriptors next to each link in "{{translated 'Additional sources'}}".
- Headlines listed in "{{translated 'Rest of the day'}}".

What stays in the original language: proper nouns (companies, products, models, people), verbatim quotes (translate but keep the original between quotation marks if it carries weight), URLs, source identifiers, ISO dates, YAML frontmatter keys.

Section heading translations:

| English (template)   | {{language name}} (output) |
| -------------------- | -------------------------- |
| TL;DR                | {{translation or 'TL;DR'}} |
| Today's focus        | {{translation}}            |
| Top stories          | {{translation}}            |
| Source               | {{translation}}            |
| Published            | {{translation}}            |
| What happened        | {{translation}}            |
| Additional context   | {{translation}}            |
| Additional sources   | {{translation}}            |
| Why it matters       | {{translation}}            |
| Rest of the day      | {{translation}}            |

Tone: {{e.g. "Spain Spanish, technical-pragmatic, no anglicism overuse"}}. Keep terms of art untranslated when there is no idiomatic equivalent ({{list of terms, e.g. LLM, embedding, fine-tuning, MCP}}).

## Common overrides

- `/{{slug}} --since YYYY-MM-DD` → wider window.
- `/{{slug}} --top N` → more stories.
- `/{{slug}} --sources adapter1,adapter2` → restrict adapters.

When the user passes overrides, substitute them in the subagent prompt.
````

---

## Validation rules

Before writing the SKILL.md, sanity-check the answers:

- `sector` matches `^[a-z0-9-]{1,20}$`.
- `audience` is at least one full sentence (≥ 60 chars).
- `keywords` is either empty or a comma-separated list.
- `top_n` is a positive integer.
- `output_lang` is an ISO 639-1 code (`en`, `es`, `fr`, `de`, `pt`, …).
- `trigger phrases` include `/<slug>` and at least 2 natural-language phrases.

If any field fails validation, ask the user to fix it before writing.

## What you must NOT do

- Don't invent answers. Every placeholder must come from the user.
- Don't write the file outside `${CLAUDE_PLUGIN_ROOT}/skills/`.
- Don't add Galileo14-specific or company-specific language unless the user puts it in the `audience` field.
- Don't edit other files in the plugin (engine, references, scraper). This skill only creates new sector skills.
