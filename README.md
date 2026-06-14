# galileo14-plugins

Galileo14's public Claude Code plugin marketplace — AI-native tools for research, reporting and knowledge work. Built by [galileo14.com](https://galileo14.com).

> **Naming convention.** `galileo14` = public-facing (this repo). `g14` = private/internal. Public skills are still prefixed `g14-` to keep a single, consistent skill namespace across both marketplaces.

## Plugins

| Plugin | Skills | Purpose |
|---|---|---|
| `research` | `g14-company-analysis`, `g14-deep-search`, `g14-fact-check`, `g14-quick-search` | Research and intelligence gathering — company dossiers, deep research, fact-checking, quick searches. |
| `ai` | `g14-prompt-creator`, `g14-skill-creator` | Meta-tooling for working with Claude — prompt engineering (CAR · COSTAR · RISEN) and deterministic skill scaffolding. |

All skills are written in English so they install cleanly anywhere, but every skill is instructed to **produce its output in the language of the user's current conversation** (defaulting to English when unclear).

## Install

All commands work both inside Claude Code (as slash commands) and from the terminal (`claude plugin ...`). The slash form is shown.

### 1. Add the marketplace

```
/plugin marketplace add Galileo14/galileo14-plugins
```

### 2. Install plugins

```
/plugin install research@galileo14
/plugin install ai@galileo14
```

### 3. Update

```
# Refresh the marketplace catalog
/plugin marketplace update galileo14
```

### 4. Validate (for maintainers)

```
claude plugin validate .
```

## Layout

```
.claude-plugin/
  marketplace.json          # catalog of all plugins
plugins/
  <plugin-name>/
    .claude-plugin/
      plugin.json           # plugin manifest
    agents/                 # plugin-level subagents (optional)
    skills/
      <skill-name>/
        SKILL.md            # entry point Claude reads
        references/         # prose Claude reads at runtime
        assets/             # templates and artifacts
```

Inside any skill, the runtime variable `${CLAUDE_PLUGIN_ROOT}` expands to the plugin's root directory — that's how SKILL.md files reference their own assets and references.

## Skill invocation

Once installed, skills are invokable by their plugin-namespaced name:

```
/research:g14-company-analysis
/ai:g14-prompt-creator
…
```

They also trigger automatically from natural-language requests that match their description's trigger phrases (in English; some skills also accept Spanish triggers).
