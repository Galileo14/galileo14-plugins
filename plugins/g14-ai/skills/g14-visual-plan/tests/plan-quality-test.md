# Evaluation criteria: Plan quality

Grade the generated plan HTML file (the deliverable under `.plans/`). Grade
globally, plus per plan step where a criterion is per-item.

PASS only if ALL of the following hold:

- **No template residue.** `grep` finds zero `{{` / `}}` placeholders, zero
  `TODO` markers, and zero Lorem Ipsum in the delivered file.
- **Real anchors.** Every file path named in the plan steps and file map exists
  in the repository (verify with Glob/Read), except paths explicitly tagged as
  `new`. Every symbol (function, table, component) the plan claims exists can
  be found in the codebase.
- **Standalone.** The document contains no conversation-relative language:
  no "as discussed", "unlike the previous version", "this revision", "the plan
  above in chat", or equivalents in any language.
- **No single-step plan, no padding.** At least 2 steps, and no step whose
  description adds nothing beyond its title.
- **Reuse before addition.** Each step names what it reuses (or states
  explicitly that nothing existing applies) before what it adds.
- **Hard-to-reverse decisions surfaced.** If the plan touches data models,
  public APIs, wire formats, ids, or auth boundaries, the Decisions section
  addresses them. If it touches none of these, the Decisions section says so
  rather than inventing filler decisions.
- **Open questions have defaults.** Every open question includes a recommended
  default. If there are none, the section states that explicitly.

For each item, return: { id, passed, evidence }. Quote the offending or
supporting text verbatim. Flag failures — do not silently fix them.
