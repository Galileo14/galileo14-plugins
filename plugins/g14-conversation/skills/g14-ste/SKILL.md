---
name: g14-ste
description: 'Response transformer: rewrites the answer in simplified technical language — ASD-STE100 (Simplified Technical English) when the conversation is in English, ETS (Español Técnico Simplificado) when it is in Spanish. If the invocation carries input, answer that input directly in STE/ETS; if invoked bare, rewrite the previous response. Trigger on: "/g14-ste", "in STE", "simplified technical english", "en ETS", "español técnico simplificado", "ponlo en ETS", "rewrite this in simplified technical language".'
---

# g14-ste — Simplified Technical Language (STE / ETS)

## Target resolution (shared logic)

1. If the invocation includes input (a question or text after the skill name), produce the answer to that input and deliver it already transformed.
2. If there is no input, take your own most recent response in this conversation and rewrite it transformed. Output only the rewritten version — no preamble about what you are doing.
3. If there is no input AND no previous response of yours, ask the user what to transform.

## Language selection

Detect the conversation language. Spanish → apply **ETS**. English (or anything else) → apply **ASD-STE100**. Do not translate: transform the text within its own language.

## ASD-STE100 rules (English)

- One instruction per sentence. One topic per paragraph, max 6 sentences per paragraph.
- Max 20 words per procedural (instruction) sentence; max 25 per descriptive sentence.
- Active voice. Simple tenses only (present, past, future). No gerund as the main verb.
- Imperative mood for instructions ("Remove the panel", not "The panel should be removed").
- One word = one meaning. Use the simplest common word that is precise; use the same word for the same thing throughout.
- Noun clusters of max 3 words. Always use articles ("the", "a") — do not drop them telegraphically.
- Warnings and cautions go first, as standalone sentences, before the instruction they protect.
- Vertical lists for sequences of more than 3 steps.

## ETS rules (Spanish)

- Frases cortas y directas. Una idea por frase. Una instrucción por frase.
- Máximo ~20 palabras por frase. Párrafos de máximo 6 frases, un solo tema.
- Voz activa. Tiempos verbales simples. Imperativo para instrucciones.
- Vocabulario técnico llano: la palabra común más precisa, siempre la misma palabra para el mismo concepto.
- Sin anglicismos con equivalente español normal. Sin subordinadas encadenadas.
- Avisos y advertencias primero, en frase propia, antes de la instrucción que protegen.
- Listas verticales para secuencias de más de 3 pasos.

## Invariants

- Do not change facts, numbers, commands, code blocks, file paths or URLs. Code stays verbatim.
- Preserve all substantive content — this transform changes sentence mechanics, not coverage.
