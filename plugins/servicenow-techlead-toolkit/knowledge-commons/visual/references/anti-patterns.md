# Anti-Patterns (AI Slop)

These patterns are explicitly forbidden. They signal "AI-generated template" and undermine the skill's purpose of producing distinctive, high-quality diagrams. Review every generated page against this list.

## Typography

**Forbidden fonts as primary `--font-body`:**

- Inter — the single most overused AI default
- Roboto, Arial, Helvetica — generic system fallbacks promoted to primary
- system-ui, sans-serif alone — no character, no intent

**Required:** Pick from the font pairings in `libraries.md`. Every generation should use a different pairing from the last.

## Color Palette

**Forbidden accent colors:**

- Indigo-500/violet-500 (`#8b5cf6`, `#7c3aed`, `#a78bfa`) — Tailwind's default purple range
- The cyan + magenta + pink neon gradient combination (`#06b6d4` → `#d946ef` → `#f472b6`)
- Any palette that could be described as "Tailwind defaults with purple/pink/cyan accents"

**Forbidden color effects:**

- Gradient text on headings (`background: linear-gradient(...); background-clip: text;`) — this screams AI-generated
- Animated glowing box-shadows on cards (`box-shadow: 0 0 20px var(--glow); animation: glow 2s...`)
- Multiple overlapping radial glows in accent colors creating a "neon haze"

**Required:** Build palettes from the reference templates (terracotta/sage, teal/cyan, rose/cranberry, slate/blue) or derive from real IDE themes (Dracula, Nord, Solarized, Gruvbox, Catppuccin). Accents should feel intentional, not default.

## Section Headers

**Forbidden:**

- Emoji icons in section headers (🏗️, ⚙️, 📁, 💻, 📅, 🔗, ⚡, 🔧, 📦, 🚀, etc.)
- Section headers that all use the same icon-in-rounded-box pattern

**Required:** Use styled monospace labels with colored dot indicators (see `.section-label` in templates), numbered badges (`section__num` pattern), or asymmetric section dividers. If an icon is genuinely needed, use an inline SVG that matches the palette — not emoji.

## Layout & Hierarchy

**Forbidden:**

- Perfectly centered everything with uniform padding
- All cards styled identically with the same border-radius, shadow, and spacing
- Every section getting equal visual treatment — no hero/primary vs. secondary distinction
- Symmetric layouts where left and right halves mirror each other

**Required:** Vary visual weight. Hero sections should dominate (larger type, more padding, accent-tinted background). Reference sections should feel compact. Use the depth tiers (hero → elevated → default → recessed). Asymmetric layouts create interest.

## Template Patterns

**Forbidden:**

- Three-dot window chrome (red/yellow/green dots) on code blocks — this is a cliché
- KPI cards where every metric has identical gradient text treatment
- "Neon Dashboard" as an aesthetic choice — it always produces generic results
- Gradient meshes with pink/purple/cyan blobs in the background

**Required:** Code blocks use a simple header with filename or language label. KPI cards vary by importance — hero numbers for the primary metric, subdued treatment for supporting metrics. Pick aesthetics with natural constraints: Blueprint (must feel technical/precise), Editorial (must have generous whitespace and serif typography), Paper/ink (must feel warm and informal).

## Structural Anti-Patterns (Match and Refuse)

If you are about to write any of the following, stop and rewrite the element with a different structure.

**Side-stripe borders.** `border-left` or `border-right` greater than 1px as a colored accent on cards, callout boxes, list items, or slide columns. Never intentional — it is the most common AI-generated layout tell. Alternatives: full border, background tint (`color-mix(in srgb, var(--accent) 8%, transparent)`), leading icon/number, or nothing.

**The hero-metric template.** Big number + small label + supporting stats + gradient accent background. SaaS dashboard cliché — every metric in a deck cannot be a KPI hero. Reserve for the single most important number per slide; use subdued treatment for supporting metrics.

**Identical card grids.** Same border-radius, same shadow, same padding, repeated endlessly. Cards with no visual hierarchy read as an itemized list that was lazily boxed. Vary: size, depth tier (elevated / default / recessed), typographic treatment, or drop the cards entirely.

**Glassmorphism as default.** Backdrop-filter blur + rgba surface used decoratively. Rare and purposeful only — e.g., a modal over a full-bleed background image. Never a page-level aesthetic.

## The Slop Test

Before delivering, apply this test: **Would a developer looking at this page immediately think "AI generated this"?** The telltale signs:

1. Inter or Roboto font with purple/violet gradient accents
2. Every heading has `background-clip: text` gradient
3. Emoji icons leading every section
4. Glowing cards with animated shadows
5. Cyan-magenta-pink color scheme on dark background
6. Perfectly uniform card grid with no visual hierarchy
7. Three-dot code block chrome
8. Side-stripe border accents (`border-left` > 1px) on more than one element
9. Every metric styled as a hero KPI (big number + gradient accent)

If two or more of these are present, the page is slop. Regenerate with a different aesthetic direction — Editorial, Blueprint, Paper/ink, or a specific IDE theme. These constrained aesthetics are harder to mess up because they have specific visual requirements that prevent defaulting to generic patterns.

### Slide-Specific Slop Test

Before delivering a deck, check:
1. Title slide is not just text on a CSS gradient — it has a real image, a designed typographic composition, or a strong geometric treatment
2. Not every metric slide uses the "big number + small label + gradient behind the number" template
3. Callout boxes do not have colored left-border stripes — use tinted background + icon instead
4. Slide-to-slide rhythm varies — no 5 consecutive content slides with identical split layout
5. The font pairing is not system-ui or Inter — check `--font-body` in the rendered HTML
