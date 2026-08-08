# Plan quality — the discipline behind a good visual plan

Distilled from Builder.io's `visual-plan` skill, adapted to local HTML plans.
Read this file in full before drafting any plan. It defines what makes the plan
document trustworthy; the template only defines what it looks like.

## Gate thoughtfully

A visual plan is a richer review surface, not a tool reserved for giant
projects. Use it when the user needs to see, compare, comment on, or approve a
direction before code — even for a modest UI, state, or workflow change. Skip
it for trivial, unambiguous work: typos, one-line fixes, a single
well-specified function, anything whose diff you could describe in one
sentence. Never pad a plan with filler and never ship a single-step plan.

## Research before you draft

Read the real files, schema, and patterns first. Name actual files, symbols,
and data shapes — never invent them. Check what already exists before proposing
anything new. Lead with reuse: for each step, name what it reuses (existing
modules, schema, components, helpers) before what it adds, so the plan explains
the genuinely new delta instead of redescribing what already exists. Delegate
wide exploration to a subagent when the surface is large, so the main context
stays clean.

## Decide the hard-to-reverse bets first

For non-trivial backend, data, or API work, sketch where the feature is headed,
then call out the decisions that are expensive to undo once data or callers
depend on them: wire format, public ids, data-model shape, auth and ownership
boundaries. Get those right in the plan even if most of the feature ships
later. Then scope to the smallest first cut that proves the approach without
foreclosing it, stating both what is in and what is explicitly deferred.

## Keep examples at the right altitude

When the user's idea is a broad framework or product change, do not collapse it
into the first concrete example they mention. Separate the core abstraction
from motivating examples. Use examples to make the plan legible, but label them
as examples unless they are the whole requested scope.

## The plan must stand alone

A reader who never saw the chat must understand the plan. If the user pasted or
referenced an earlier plan, treat it as source material but rewrite the
published plan as a clean standalone proposal. No revision language ("unlike
the previous version", "this revision changes..."), no phrases that only make
sense in conversation. State the positive model directly. If the concept is
abstract, lead near the top with one concrete example before architecture or
mode tables.

## Planning is read-only

Make no source edits while building or reviewing the plan. The only file the
skill writes is the plan HTML inside `.plans/`. Start editing source code only
after the user approves the direction.

## Clarify vs. assume

Do not ask the user how to build it — explore and present the approach in the
plan. Ask a clarifying question only when an ambiguity would change the design
and you cannot resolve it from the code; batch 2–4 high-leverage questions at
most. Otherwise state the assumption explicitly and proceed. Anything
unresolved goes in the plan's Open Questions section, each with a recommended
default. Before handoff, do a final pass: any decision that would affect
architecture, scope, UX, data shape, or rollout is either decided in the plan
with rationale, or listed as an open question with a default.

## The plan is the approval gate

After delivering the plan, ask the user to review and approve before writing
code, and name which files/areas the work touches. Presenting the plan and
requesting sign-off IS the approval step — do not ask a separate "does this
look good?" question.

## The document is the source of truth, not the chat

When scope shifts during review, update the plan HTML in place rather than only
changing course in chat, and keep the updated document standalone. Re-read the
approved plan before major implementation steps.

## Visuals earn their place

- Architecture-only, backend-only, or migration plans need no wireframes. One
  inline SVG diagram per genuinely spatial relationship is enough; prefer
  grouped regions, layers, or before/after panels over a single-axis chain
  unless the relationship is truly sequential.
- Any inline SVG uses design-system CSS variables for color
  (`var(--g-primary)`, `var(--text-muted)`, `var(--border-soft)`, the
  `--g-accent-*` set for series) — never hex.
- Keep product sketches and explanatory diagrams separate: a screen sketch
  looks like the app state under discussion; arrows, contracts, and data flow
  live in their own diagram or in prose.

## Self-review before handoff

For high-stakes plans — architecture, data-model, migration, multi-file, or
otherwise risky work — the quality gate in SKILL.md (fresh grader subagents) is
mandatory, not optional. Point of the review: hard-to-reverse decisions made
implicitly or not at all, steps not anchored in real files or symbols, a menu
of options where the plan should commit to one, obvious missing decisions
("what happens when X?"), and padding. Apply clear-cut fixes yourself; route
genuine judgment calls to the Open Questions section.
