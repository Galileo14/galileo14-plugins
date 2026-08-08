# galileo14-plugins

Public Claude Code plugin marketplace for **Galileo14**. Client-facing skills, agents and workflows for research, code auditing and working with Claude.

> **Naming convention.** `galileo14` = public-facing (this repo). `g14` = private/internal. See the parent workspace's `CLAUDE.md` for context.

## Plugins

| Plugin | Skills | Purpose |
|---|---|---|
| `g14-research` | `g14-company-analysis`, `g14-deep-search`, `g14-fact-check`, `g14-quick-search` | Research and intelligence gathering — company dossiers, deep multi-source research, fact-checking, quick searches. |
| `g14-ai` | `g14-prompt-creator`, `g14-skill-creator`, `g14-visual-plan` | Meta-tooling for working with Claude — prompt engineering (CAR, COSTAR, RISEN), deterministic skill scaffolding, and local HTML visual plans. |
| `g14-audit` | `g14-architecture-audit`, `g14-clean-code-audit`, `g14-database-audit`, `g14-full-audit`, `g14-scalability-audit`, `g14-security-audit`, `g14-skill-audit` | Codebase audits through five focused lenses plus a full-audit orchestrator and a Claude Code skill auditor. |

All skills are written in English so they install cleanly anywhere, but every skill is instructed to **produce its output in the language of the user's current conversation** (defaulting to English when unclear).

## Install

All commands below work both inside Claude Code (as slash commands, e.g. `/plugin marketplace add ...`) and from the terminal (`claude plugin marketplace add ...`). The slash form is shown.

### 1. Add the marketplace

```
/plugin marketplace add Galileo14/galileo14-plugins
```

Alternatives:

```
# Pin to a branch or tag
/plugin marketplace add Galileo14/galileo14-plugins@main

# Full git URL (any host)
/plugin marketplace add https://github.com/Galileo14/galileo14-plugins.git

# Local checkout (for development)
/plugin marketplace add ./galileo14-plugins
```

### 2. Install plugins

```
/plugin install g14-research@galileo14-plugins
/plugin install g14-ai@galileo14-plugins
/plugin install g14-audit@galileo14-plugins
```

### 3. Update

```
# Refresh the marketplace catalog (pulls new plugins / version changes)
/plugin marketplace update galileo14-plugins

# Refresh every configured marketplace
/plugin marketplace update
```

Plugin updates apply automatically once the marketplace is refreshed, as long as the plugin's `version` (in its `plugin.json`) has been bumped or you're tracking commit SHAs.

### 4. List / inspect

```
/plugin marketplace list      # all configured marketplaces
/plugin                       # interactive plugin manager
```

### 5. Disable / enable a plugin (keep installed)

```
/plugin disable g14-research@galileo14-plugins
/plugin enable  g14-research@galileo14-plugins
```

### 6. Uninstall a single plugin

```
/plugin uninstall g14-research@galileo14-plugins
```

### 7. Remove the whole marketplace

> Removing the marketplace **also uninstalls every plugin you installed from it**. To just refresh, use `update` instead.

```
/plugin marketplace remove galileo14-plugins
```

### 8. Validate (for marketplace maintainers)

From the repo root:

```
claude plugin validate .
```

Checks `marketplace.json` schema, duplicate names, path traversal, and version mismatches against each `plugin.json`. To validate an individual plugin's manifest and its SKILL/agent/command files:

```
claude plugin validate ./plugins/<plugin-name>
```

## Layout

```
.claude-plugin/
  marketplace.json          # catalog of all plugins
plugins/
  <plugin-name>/
    .claude-plugin/
      plugin.json           # plugin manifest
    skills/
      <skill-name>/
        SKILL.md            # entry point Claude reads
        references/         # prose Claude reads at runtime
        assets/             # templates and brand artifacts
        scripts/            # python/bash helpers (optional)
        tests/              # rubrics for self-grading (optional)
        evals/              # eval suites (optional)
    agents/                 # subagents the skills delegate to (optional)
```

Inside any skill, the runtime variable `${CLAUDE_PLUGIN_ROOT}` expands to the plugin's root directory — that's how SKILL.md files reference their own assets and references.

## Skill invocation

Once installed, skills are invokable by their plugin-namespaced name:

```
/g14-research:g14-company-analysis
/g14-audit:g14-full-audit
…
```

They also trigger automatically from natural-language requests that match their description's trigger phrases.
