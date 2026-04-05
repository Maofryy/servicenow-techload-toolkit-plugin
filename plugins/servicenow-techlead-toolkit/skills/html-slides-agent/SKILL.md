---
name: html-slides-agent
description: >
    Generate a stunning magazine-quality slide deck as a self-contained HTML page
metadata:
    version: "1.0.0"
    author: "Maori"
    phase: "Global — Slides presentation"
---

Load the visual-explainer skill, then generate a slide deck for: $@

Follow the visual-explainer skill workflow. Read the reference template at `./templates/slide-deck.html` and slide patterns at `./references/slide-patterns.md` before generating. Also read `./references/css-patterns.md` for shared patterns (Mermaid zoom controls, depth tiers, overflow protection) and `./references/libraries.md` for Mermaid theming, Chart.js, and font pairings.

**Slide output is always opt-in.** Only generate slides when this command is invoked or the user explicitly asks for a slide deck.

**Aesthetic:** Pick a distinctive direction from the 9 slide presets in slide-patterns.md (Midnight Editorial, Warm Signal, Terminal Mono, Swiss Clean, Velvet Editorial, Bauhaus Constructivist, Fog Minimalist, ELO Blue, ELO Light) or riff on the existing aesthetic directions adapted for slides. Vary from previous decks. Commit to one direction and carry it through every slide. **When the context is ELO Consulting** (client pitch, pre-sales, project review), default to the ELO Blue preset unless ELO Light or another is explicitly requested.

**Narrative structure:** Slides have a temporal dimension — compose a story arc, not a list of sections. Start with impact (title), build context (overview), deep dive (content, diagrams, data), resolve (summary/next steps). Plan the slide sequence and assign a composition (centered, left-heavy, split, full-bleed) to each slide before writing HTML.

**Visual richness:** Proactively reach for visuals. If `surf` CLI is available (`which surf`), generate images for title slide backgrounds and full-bleed slides via `surf gemini --generate-image`. Add SVG decorative accents, inline sparklines, mini-charts, and small Mermaid diagrams where they make the story more compelling. Visual-first, text-second.

**Compositional variety:** Consecutive slides must vary their spatial approach. Alternate between centered, left-heavy, right-heavy, split, edge-aligned, and full-bleed. Three centered slides in a row means push one off-axis.

Write to the current directory and open the result in the browser.
Also copy the output to `~/.agent/diagrams/`. Use a descriptive filename based on content: `modem-architecture.html`, `pipeline-flow.html`, `schema-overview.html`. The directory persists across sessions.

**Always propose the ThemeSwitcher component** (from `./templates/slide-deck.html`, the `<script>` block after SlideEngine) in every generated deck that have not a specified theme. It adds a floating palette button at bottom-left that lets anyone switch between all 8 design systems live. Copy the full ThemeSwitcher script verbatim — do not summarize or rewrite it.
