---
name: visual-explainer
description: >
  Use this when a self-contained HTML page will explain something better than text: an
  architecture or flow diagram, a sequence or ER diagram, a comparison or audit table with many
  rows, a roles × operations grid, a timeline or roadmap, a dashboard of metrics, a plan or
  diff review laid out visually. Trigger on "diagram", "schéma", "show this visually", "draw",
  "flowchart", "make a page for this", or when another skill (solution-design, security-review,
  csdm-assistant) decides a visual would help. Not for slide decks (html-slides) nor for prose
  deliverables (communication).
---

# Visual Explainer

Respond in the user's language; all visible text in the page is in the user's language.

## Mission

Produce one self-contained `.html` file (inline CSS, CDN links only for fonts and optional
libraries) that a developer, a PM or a client can open, understand in a minute and share.
Design it: a deliberate aesthetic, a clear hierarchy, both light and dark themes working. Open
it in the browser and give the path. A page is worth making when the structure matters more
than the words; a four-row table in conversation is often enough, and that is your judgement.

## What you know

**Decide the direction first (seconds, not minutes)**
- Who looks at it and what they need: density for a developer, the big picture for a PM.
- Content type: architecture, flowchart, sequence, data flow, ER, state machine, mind map,
  class, C4, table, timeline, dashboard, prose-first page.
- Aesthetic, one and committed. Constrained ones are safer: Blueprint (grid background, slate
  and blue, monospace labels), Editorial (serif headlines, whitespace, navy and gold or earth
  tones), Paper/ink (warm cream, terracotta and sage), Monochrome terminal. Flexible ones need
  discipline: a real named IDE palette (Nord, Catppuccin, Solarized, Gruvbox, Rosé Pine),
  data-dense. Vary from the last page you made.
- Forbidden: neon cyan-magenta-purple on dark, gradient mesh blobs, Inter or Roboto or Arial as
  body font, violet/indigo accents (`#8b5cf6`, `#7c3aed`, `#a78bfa`, `#d946ef`), gradient text,
  glowing box-shadow animations, pulsing on static content. The swap test: if a generic dark
  theme would look the same, you have not designed anything.

**Rendering approach by content**

| Content | Approach |
|---|---|
| Architecture, text-heavy cards (< 15 elements) | CSS Grid cards + flow arrows |
| Architecture, topology; flowchart; sequence; data flow; ER; state; mind map; class; C4 | Mermaid (C4 via `graph TD` + `subgraph`, not native C4) |
| Complex architecture (15+ elements) | Hybrid: small Mermaid overview + CSS cards per module |
| Data table, comparison, audit, permission grid | Real `<table>`: sticky header, zebra rows, right-aligned numbers, status as styled spans not emoji |
| Timeline, roadmap | CSS central line + cards |
| Dashboard, metrics | CSS Grid + inline SVG sparklines, Chart.js for real charts |
| Plan or spec review | Overview, flow, file structure with one-line descriptions, key snippets only; never full source dumps |

**Mermaid rules that avoid broken pages**
- Always the full `diagram-shell` pattern (shell, wrap, zoom controls, viewport, canvas, JS)
  from `templates/mermaid-flowchart.html`; a bare `<pre class="mermaid">` has no zoom and
  renders unusably small.
- `theme: 'base'` with `themeVariables` matching the page palette; centre the diagram with flex.
- Prefer `flowchart TD`; `LR` only for 3–4 node linear flows. 10–12 nodes: raise `fontSize` to
  18–20px and initial zoom to 1.5. 15+: hybrid pattern, never one giant diagram.
- Line breaks with `<br/>` inside quoted labels, never `\n`. `stateDiagram-v2` labels break on
  colons, parentheses and HTML; use `flowchart TD` with quoted edge labels when labels need them.
- Never define a page-level `.node` class (Mermaid uses it); use `.ve-card` for cards.

**Style that reads as designed**
- Typography is the diagram: a distinctive pairing (DM Sans + Fira Code, Instrument Serif +
  JetBrains Mono, IBM Plex Sans + Mono, Bricolage Grotesque + Fragment Mono, Plus Jakarta Sans
  + Azeret Mono), loaded via Google Fonts with a system fallback.
- Palette as CSS custom properties (`--bg`, `--surface`, `--border`, `--text`, `--text-dim`,
  3–5 semantic accents with dim variants); primary theme in `:root`, the other under
  `prefers-color-scheme`. Good accents: terracotta + sage, teal + slate, rose + cranberry,
  amber + emerald, deep blue + gold.
- Depth through 2–4% lightness shifts and low-opacity borders, not drop shadows everywhere; a
  background with atmosphere (subtle gradient, faint grid, soft glow), not a flat void.
- Visual weight follows importance: hero summary and key numbers dominate on load; reference
  sections compact or collapsible (`<details>`).
- Motion earns its place: staggered fade-in on load, hover feedback, `prefers-reduced-motion`
  respected; nothing runs continuously after load.

**Delivery**
- Write to `~/.agent/diagrams/<descriptive-name>.html` (persists across sessions), open it
  (`open` on macOS, `xdg-open` on Linux), tell the user the path.
- Optional sharing via Vercel: `bash <skill-base-dir>/scripts/share.sh <file>` (needs the
  `vercel` CLI; deployments are public).
- Optional AI illustration when `surf` is installed: generate, base64-embed, keep the page
  standing on its own if it is not available.

## Sources

Read only the file that matches the output, from `knowledge-commons/visual/` (resolve relative
to this skill's base directory, two levels up). Read it each time rather than relying on memory.

| Output | Read |
|---|---|
| Card-based architecture overview | `templates/architecture.html` |
| Any Mermaid diagram | `templates/mermaid-flowchart.html`, then the Mermaid section of `references/libraries.md` |
| Table, comparison, audit, permission grid | `templates/data-table.html` |
| Dashboard with charts | `templates/data-table.html` for layout, Chart.js section of `references/libraries.md` |
| Prose-first page (README, article) | "Prose Page Elements" in `references/css-patterns.md`, "Typography by Content Voice" in `references/libraries.md` |
| Page with 4+ sections needing navigation | `references/responsive-nav.md` in addition |
| Code blocks, overflow protection, collapsibles, KPI cards, connectors | the matching section of `references/css-patterns.md` (use its table of contents) |

Before delivering, skim `references/anti-patterns.md` and check the page against it.

## Your call

- Whether a page is warranted at all, or a table in conversation does the job.
- Content type, aesthetic, density, which sections are hero and which are collapsed.
- Whether a diagram, a table or both; whether to add an illustration.
- File name.

## Guardrails

- One file, self-contained, opens without console errors, no horizontal overflow at any width
  (`min-width: 0` on grid and flex children, `overflow-wrap` on panels).
- Both themes look intentional; squint test shows hierarchy; information is complete, not
  only pretty.
- Every Mermaid container has zoom, pan and click-to-expand.
- Never fall back to ASCII art once a page is the chosen output.
