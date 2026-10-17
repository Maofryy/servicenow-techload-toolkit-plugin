---
name: html-slides
description: >
  Use this when the user wants a slide deck as a self-contained HTML page: a presentation, a
  pitch, a project review, a steering committee (COPIL) deck, a sprint review, a roadmap, an
  estimation summary for a client, or "make slides / un deck / une présentation about X". Also
  the target of future automated decks (ServiceNow watch newsletter). Slides are opt-in: never
  turn a page or a document into slides unless the user asks for slides. Not for scrollable
  explanatory pages or diagrams (visual-explainer) nor for .pptx files.
---

# HTML Slides

Respond in the user's language; all visible text in the deck is in the user's language.

## Mission

Produce a magazine-quality deck as one `.html` file: each slide one viewport tall, a story arc
rather than a paginated document, one committed aesthetic carried through every slide, and
every point of the source material present. Open it in the browser and give the path. The
reader is an audience in a room; the user presents it.

## What you know

**Slides are a different medium**
- Compose a narrative: impact (title), context, deep dive, resolution. Plan the sequence and a
  composition per slide (centered, left-heavy, split, full-bleed) before writing HTML; three
  centred slides in a row means push one off-axis.
- Content completeness: inventory the source, map every item to a slide, verify nothing is
  dropped. Add slides rather than cutting; a 22-slide deck that covers everything beats a 13-slide
  deck missing 40% of the source. Content never scrolls inside a slide; split it.
- Typography 2–3× larger than a page; visual first, text second: SVG accents, sparklines,
  small Mermaid diagrams, per-slide background variation, generated images when `surf` is
  available.

**Detect what kind of deck it is**
- PM slides (project status, sprint review or scorecard, roadmap, kanban, retrospective, flash
  report, project health, timeline, burndown, velocity): use `templates/pm-deck.html` as the
  reference and the "PM Slides" section of `references/slide-patterns.md` for per-slide layouts
  and RAG colours.
- Estimation slides (chiffrage, forfait, work breakdown, jours par profil, plan de charge,
  répartition des charges): include `.slide--estimation` slides built from the
  `<!-- SLIDE: ESTIMATION SYNTHÈSE -->` block at the end of `templates/slide-deck.html`: three
  KPI cards (total days, phases, profiles) and a data table Phase | profiles… | Total | Risk,
  day values with the `j` suffix, risk badges `--confident` / `--uncertain` / `--high`, footer
  totals. A task-level detail slide reuses the same structure with task rows.
- Everything else: `templates/slide-deck.html` (all slide types) and `references/slide-patterns.md`.

**Presets and ELO branding**
- Write one sentence describing the room (who, what screen, what light) and let it force the
  dark/light answer and the preset: Midnight Editorial, Warm Signal, Terminal Mono, Swiss Clean,
  Velvet Editorial, Bauhaus Constructivist, Fog Minimalist, ELO Blue, ELO Light (Calcaire).
- ELO context (client pitch, pre-sales, cadrage, project review): default to ELO Blue, ELO
  Light when a lighter document-like deck is requested. Never ELO presets for non-ELO content.
- With ELO Blue or ELO Light, include the ELO Logo Overlay (CSS + JS block from the "ELO Logo
  Overlay" section of `slide-patterns.md`, copied verbatim): logo bottom-left on all slides,
  top-left on the title slide.
- Vary presets across decks; commit to one within a deck. Pick a colour commitment level
  (restrained, committed, full palette, drenched) and keep it.

**ThemeSwitcher is optional**
- The floating design-system switcher (section "ThemeSwitcher" of `slide-patterns.md`) lets a
  viewer change palette live. Offer it when the user has not fixed a theme and may want to try
  several; skip it for branded client decks or when the user asked for one look. When included,
  copy the script verbatim.

## Sources

From `knowledge-commons/visual/` (resolve relative to this skill's base directory, two levels
up), read for every deck: `references/slide-patterns.md` (engine CSS, slide types, transitions,
navigation chrome, presets, planning process) and the matching template (`slide-deck.html`,
`pm-deck.html`). Then only the sections you need of `references/css-patterns.md` (Mermaid zoom,
overflow protection, depth tiers) and `references/libraries.md` (Mermaid theming, Chart.js,
font pairings). Check `references/anti-patterns.md` before delivering.

## Your call

- Slide count and sequence, compositions, preset, colour commitment, whether to generate
  images, whether to offer the ThemeSwitcher.
- When the source is thin, whether to ask for the missing content or to build the arc with
  visible placeholders.

## Guardrails

- Slides only when asked; never auto-convert.
- Every slide fits 100dvh with no internal scroll; keyboard, touch and wheel navigation work;
  no console errors.
- Nothing from the source is silently dropped.
- Write to `~/.agent/diagrams/<descriptive-name>.html` (and the current directory when the user
  works in a project), open it, give the path.
