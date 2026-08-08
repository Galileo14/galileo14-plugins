# Evaluation criteria: Brand compliance

Grade the generated plan HTML file (the deliverable under `.plans/`) globally.

PASS only if ALL of the following hold:

- **Theme attribute.** `<html>` carries `data-theme="light"` (or
  `data-theme="dark"` only if the user explicitly requested dark).
- **Fonts.** The Google Fonts `<link>` loads Geist, Geist Mono, and Righteous,
  and no other font family is referenced anywhere in the file (search for
  `font-family` declarations outside the system stylesheet block).
- **System CSS inlined.** The `<style>` block in `<head>` contains the fetched
  design-system stylesheet (it defines `--g-primary`), not the placeholder
  comment. If a fallback style block was used because the fetch failed, it is
  marked with the comment `/* fallback — design system unreachable */` and the
  chat handoff reported it.
- **No hardcoded colors.** Zero hex colors (`#xxx`/`#xxxxxx`) or `rgb(...)`
  values in inline `style=` attributes or in any `<style>` block other than
  the system stylesheet — including inside inline SVG diagrams, which must use
  CSS variables.
- **Wordmark.** `<div class="g-logo ...">GALILEO<span>14</span></div>` appears
  in the topbar and footer.
- **Square geometry.** No `border-radius` overrides anywhere outside the system
  stylesheet.
- **Template structure intact.** The seven numbered sections (01–07) and the
  approval callout are present, in order, with their `section-num` markers.
  Repeatable blocks may repeat; sections may not be reordered or renamed
  beyond filling their heading slots.
- **Scripts preserved.** The theme-toggle script and the `<pre>` copy-button
  script from the template are present at the end of `<body>`.

For each item, return: { id, passed, evidence }. Quote the offending or
supporting markup verbatim. Flag failures — do not silently fix them.
