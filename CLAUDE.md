# galileo14-plugins — Galileo14 public marketplace

A Claude Code plugin marketplace for public, client-facing use: skills, agents
and workflows for research, code auditing and working with Claude. It's public
(repo `galileo14-plugins`); the private internal marketplace lives in
`g14-plugins`.

## Structure

- `.claude-plugin/marketplace.json` — catalog: registers each plugin with its
  `name` and `source` (`./plugins/<folder>`).
- `plugins/<plugin>/.claude-plugin/plugin.json` — plugin manifest (`name`,
  `description`, `version`).
- `plugins/<plugin>/skills/`, `/agents/` — the plugin's skills and agents.

All plugins, skills and their folders use the `g14-` prefix.

## Plugins

- `g14-research` — research and intelligence gathering (company dossiers, deep
  multi-source research, fact-checking, quick panoramic searches). Fans out
  platform-specific researcher agents in parallel and grades the result before
  delivery.
- `g14-ai` — meta-tooling for working with Claude (prompt engineering with CAR,
  COSTAR & RISEN frameworks; deterministic skill scaffolding; local HTML
  visual plans in `.plans/`).
- `g14-audit` — codebase audits through five focused lenses (security,
  scalability, architecture, clean-code, database), a full-audit orchestrator,
  and a Claude Code skill auditor.

## Versioning rule

After every change to a plugin, bump its `version` in `plugin.json` (SemVer).
Without the bump, Claude Code won't invalidate the cache and won't apply the
update.
