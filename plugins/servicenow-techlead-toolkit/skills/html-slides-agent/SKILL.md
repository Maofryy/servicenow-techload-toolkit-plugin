---
name: html-slides-agent
description: >
    Generate a stunning magazine-quality slide deck as a self-contained HTML page.
    Use this skill when the user asks for slides, a slide deck, a presentation, a pitch deck,
    a slideshow, or wants to present data visually as slides. Also trigger when the user says
    "make a deck for", "create slides for", "build a presentation about", "I need a slide deck",
    or runs the /html-slides-agent command.
metadata:
    version: "1.0.0"
    author: "Maori"
    phase: "Global — Slides presentation"
---

Load the visual-explainer skill, then generate a slide deck for: $@

Follow the visual-explainer skill workflow. Read the reference template at `../../knowledge-commons/visual/templates/slide-deck.html` and slide patterns at `../../knowledge-commons/visual/references/slide-patterns.md` before generating. Also read `../../knowledge-commons/visual/references/css-patterns.md` for shared patterns (Mermaid zoom controls, depth tiers, overflow protection) and `../../knowledge-commons/visual/references/libraries.md` for Mermaid theming, Chart.js, and font pairings.

**PM Slides detection:** When the request mentions any of — project status, sprint review, sprint scorecard, roadmap, kanban, kanban board, retrospective, retro, flash report, project health, timeline, burndown, phases, carry-over, velocity report — read `../../knowledge-commons/visual/templates/pm-deck.html` as the reference template (instead of or alongside `slide-deck.html`) and follow the `## PM Slides` section of `slide-patterns.md` for per-slide layout guidance.

**Estimation Slides detection:** When the request mentions any of — chiffrage, estimation, forfait, work breakdown, jours par profil, effort estimation, sizing, phases et profils, plan de charge, répartition des charges — include one or more `.slide--estimation` slides in the deck. For each such slide:
- Read the `<!-- SLIDE: ESTIMATION SYNTHÈSE -->` block at the end of `../../knowledge-commons/visual/templates/slide-deck.html` as the canonical reference — copy its HTML structure and CSS classes verbatim, only replace content (phase labels, day values, risk levels).
- Structure: 3 KPI cards (total jours, nb phases, nb profils) + a `data-table` with columns Phase | Chef de Projet | Architecte | Tech Lead | Développeur | Total | Risque.
- Day values always include the unit suffix `j` (e.g. `5j`, `20j`).
- Risk badge per row uses `.est-risk-badge--confident` (green), `.est-risk-badge--uncertain` (orange/gold), or `.est-risk-badge--high` (red) based on confidence level.
- Footer row uses `.est-footer` with totals per profile + grand total, all with `j` suffix.
- For a task-level detail slide, reuse the identical structure — replace phase rows with task rows, no other change needed.

**Slide output is always opt-in.** Only generate slides when this command is invoked or the user explicitly asks for a slide deck.

**Aesthetic:** Pick a distinctive direction from the 9 slide presets in slide-patterns.md (Midnight Editorial, Warm Signal, Terminal Mono, Swiss Clean, Velvet Editorial, Bauhaus Constructivist, Fog Minimalist, ELO Blue, ELO Light / ELO Velvet · Calcaire) or riff on the existing aesthetic directions adapted for slides. Vary from previous decks. Commit to one direction and carry it through every slide. **When the context is ELO Consulting** (client pitch, pre-sales, project review), default to the ELO Blue preset unless ELO Light or another is explicitly requested.

**ELO logo overlay:** When generating a deck in ELO Blue or ELO Light (Calcaire), always include the ELO Logo Overlay (CSS + JS injection block) from the **ELO Logo Overlay** section of slide-patterns.md. The logo appears bottom-left on all slides and top-left on the title slide — copy the full CSS and JS blocks verbatim, do not summarize.

**Narrative structure:** Slides have a temporal dimension — compose a story arc, not a list of sections. Start with impact (title), build context (overview), deep dive (content, diagrams, data), resolve (summary/next steps). Plan the slide sequence and assign a composition (centered, left-heavy, split, full-bleed) to each slide before writing HTML.

**Visual richness:** Proactively reach for visuals. If `surf` CLI is available (`which surf`), generate images for title slide backgrounds and full-bleed slides via `surf gemini --generate-image`. Add SVG decorative accents, inline sparklines, mini-charts, and small Mermaid diagrams where they make the story more compelling. Visual-first, text-second.

**Compositional variety:** Consecutive slides must vary their spatial approach. Alternate between centered, left-heavy, right-heavy, split, edge-aligned, and full-bleed. Three centered slides in a row means push one off-axis.

Write to the current directory and open the result in the browser.
Also copy the output to `~/.agent/diagrams/`. Use a descriptive filename based on content: `modem-architecture.html`, `pipeline-flow.html`, `schema-overview.html`. The directory persists across sessions.

**Always propose the ThemeSwitcher component** (from `../../knowledge-commons/visual/templates/slide-deck.html`, the `<script>` block after SlideEngine) in every generated deck that have not a specified theme. It adds a floating palette button at bottom-left that lets anyone switch between all 8 design systems live. Copy the full ThemeSwitcher script verbatim — do not summarize or rewrite it.
