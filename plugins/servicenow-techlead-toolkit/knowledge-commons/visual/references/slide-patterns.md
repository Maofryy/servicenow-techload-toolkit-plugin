# Slide Deck Patterns

CSS patterns, JS engine, slide type layouts, transitions, navigation chrome, and curated presets for self-contained HTML slide presentations. All slides are viewport-fit (100dvh), single-file, same philosophy as scrollable pages.

**When to use slides:** Only when the user explicitly requests them — `/generate-slides`, `--slides` flag on an existing prompt, or natural language like "as a slide deck." Never auto-select slide format.

**Before generating**, also read `./css-patterns.md` for shared patterns (Mermaid zoom controls, overflow protection, depth tiers, status badges) and `./libraries.md` for Mermaid theming, Chart.js, and font pairings. Those patterns apply to slides too — this file adds slide-specific patterns on top.

## Planning a Deck from a Source Document

When converting a plan, spec, review, or any structured document into slides, follow this process before writing any HTML. Skipping it leads to polished-looking decks that silently drop 30–40% of the source material.

**Step 1 — Inventory the source.** Read the entire source document and enumerate every section, subsection, card, table row, decision, specification, collapsible detail, and footnote. Count them. A plan with 7 sections, 6 decision cards, a 7-row file table, 4 presets, 6 technique guides, and an engine spec with 3 sub-specs and 2 collapsibles is ~25 distinct content items that all need slide real estate.

**Step 2 — Map source to slides.** Assign each inventory item to one or more slides. Every item must appear somewhere. Rules:

- If a section has 6 decisions, all 6 need slides — not the 2 that fit on one split slide.
- If a table has 7 rows, all 7 rows show up.
- Collapsible/expandable details in the source are not optional in the deck — they become their own slides.
- Subsections with multiple cards (e.g., "6 Visual Technique cards") may need 2–3 slides to cover at readable density.
- Each plan section typically needs a divider slide + 1–3 content slides depending on density.

**Step 3 — Choose layouts.** For each planned slide, pick a slide type and spatial composition. Vary across the sequence (see Compositional Variety below). This is where narrative pacing happens — alternate dense slides with sparse ones.

**Step 4 — Plan images.** Run `which surf`. If surf-cli is available, plan 2–4 generated images for the deck. At minimum, target the **title slide** (16:9 background that sets the visual tone) and **one full-bleed slide** (immersive background for a key moment). Content slides with conceptual topics also benefit from a 1:1 illustration in the aside area. Generate these images early — before writing HTML — so you can embed them as base64 data URIs. See the Proactive Imagery section below for the full workflow. If surf isn't available, degrade to CSS gradients and SVG decorations — note the fallback in a comment but don't error.

**Step 5 — Verify before writing HTML.** Scan the inventory from Step 1. Is anything unmapped? Would a reader of the source document notice something missing from the deck? If yes, add slides. A source document with 7 sections typically produces 18–25 slides, not 10–13.

**The test:** After generating the deck, a reader who has never seen the source document should be able to reconstruct every major point from the slides alone. If they'd miss entire sections, the deck is incomplete.

## Slide Engine Base

The deck is a scroll-snap container. Each slide is exactly one viewport tall.

```html
<body>
    <div class="deck">
        <section class="slide slide--title">...</section>
        <section class="slide slide--content">...</section>
        <section class="slide slide--diagram">...</section>
        <!-- one <section> per slide -->
    </div>
</body>
```

```css
/* Scroll-snap container */
.deck {
    height: 100dvh;
    overflow-y: auto;
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;
}

/* Individual slide */
.slide {
    height: 100dvh;
    scroll-snap-align: start;
    overflow: hidden;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: clamp(40px, 6vh, 80px) clamp(40px, 8vw, 120px);
    isolation: isolate; /* contain z-index stacking */
}
```

## Typography Scale

Slide typography is 2–3× larger than scrollable pages. Page-sized text on a viewport-sized canvas looks like a mistake.

```css
.slide__display {
    font-size: clamp(48px, 10vw, 120px);
    font-weight: 800;
    letter-spacing: -3px;
    line-height: 0.95;
    text-wrap: balance;
}

.slide__heading {
    font-size: clamp(28px, 5vw, 48px);
    font-weight: 700;
    letter-spacing: -1px;
    line-height: 1.1;
    text-wrap: balance;
}

.slide__body {
    font-size: clamp(16px, 2.2vw, 24px);
    line-height: 1.6;
    text-wrap: pretty;
}

.slide__label {
    font-family: var(--font-mono);
    font-size: clamp(10px, 1.2vw, 14px);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--text-dim);
}

.slide__subtitle {
    font-family: var(--font-mono);
    font-size: clamp(14px, 1.8vw, 20px);
    color: var(--text-dim);
    letter-spacing: 0.5px;
}
```

| Element                | Size range | Notes                                |
| ---------------------- | ---------- | ------------------------------------ |
| Display (title slides) | 48–120px   | `10vw` preferred, weight 800         |
| Section numbers        | 100–240px  | Ultra-light (weight 200), decorative |
| Headings               | 28–48px    | `5vw` preferred, weight 700          |
| Body / bullets         | 16–24px    | `2.2vw` preferred, 1.6 line-height   |
| Code blocks            | 14–18px    | `1.8vw` preferred, mono              |
| Quotes                 | 24–48px    | `4vw` preferred, serif italic        |
| Labels / captions      | 10–14px    | Mono, uppercase, dimmed              |

## Cinematic Transitions

IntersectionObserver adds `.visible` when a slide enters the viewport. Slides animate in once and stay visible when scrolling back.

```css
/* Slide entrance — fade + lift + subtle scale */
.slide {
    opacity: 0;
    transform: translateY(40px) scale(0.98);
    transition:
        opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1),
        transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide.visible {
    opacity: 1;
    transform: none;
}

/* Staggered child reveals — add .reveal to each content element */
.slide .reveal {
    opacity: 0;
    transform: translateY(20px);
    transition:
        opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1),
        transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide.visible .reveal {
    opacity: 1;
    transform: none;
}

/* Stagger delays — up to 6 children per slide */
.slide.visible .reveal:nth-child(1) {
    transition-delay: 0.1s;
}
.slide.visible .reveal:nth-child(2) {
    transition-delay: 0.2s;
}
.slide.visible .reveal:nth-child(3) {
    transition-delay: 0.3s;
}
.slide.visible .reveal:nth-child(4) {
    transition-delay: 0.4s;
}
.slide.visible .reveal:nth-child(5) {
    transition-delay: 0.5s;
}
.slide.visible .reveal:nth-child(6) {
    transition-delay: 0.6s;
}

@media (prefers-reduced-motion: reduce) {
    .slide,
    .slide .reveal {
        opacity: 1 !important;
        transform: none !important;
        transition: none !important;
    }
}
```

## Navigation Chrome

All navigation is `position: fixed` with high z-index, layered above slides. Styled to be visible on any background.

### Progress Bar

```css
.deck-progress {
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: var(--accent);
    z-index: 100;
    transition: width 0.3s ease;
    pointer-events: none;
}
```

### Nav Dots

```css
.deck-dots {
    position: fixed;
    right: clamp(12px, 2vw, 24px);
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    gap: 8px;
    z-index: 100;
}

.deck-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--text-dim);
    opacity: 0.3;
    border: none;
    padding: 0;
    cursor: pointer;
    transition:
        opacity 0.2s ease,
        transform 0.2s ease;
}

.deck-dot:hover {
    opacity: 0.6;
}

.deck-dot.active {
    opacity: 1;
    transform: scale(1.5);
    background: var(--accent);
}
```

### Slide Counter

```css
.deck-counter {
    position: fixed;
    bottom: clamp(12px, 2vh, 24px);
    right: clamp(12px, 2vw, 24px);
    font-family: var(--font-mono);
    font-size: 12px;
    color: var(--text-dim);
    z-index: 100;
    font-variant-numeric: tabular-nums;
}
```

### Keyboard Hints

Auto-fade after first interaction or after 4 seconds.

```css
.deck-hints {
    position: fixed;
    bottom: clamp(12px, 2vh, 24px);
    left: 50%;
    transform: translateX(-50%);
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-dim);
    opacity: 0.6;
    z-index: 100;
    transition: opacity 0.5s ease;
    white-space: nowrap;
}

.deck-hints.faded {
    opacity: 0;
    pointer-events: none;
}
```

### Chrome Visibility on Mixed Backgrounds

For decks where some slides are light and some dark (especially full-bleed slides), nav chrome needs to remain visible. Two approaches:

```css
/* Approach A: subtle backdrop on chrome elements */
.deck-dots,
.deck-counter {
    background: color-mix(in srgb, var(--bg) 70%, transparent 30%);
    padding: 6px;
    border-radius: 20px;
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
}

/* Approach B: text shadow for legibility on any background */
.deck-counter,
.deck-hints {
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}
```

## ThemeSwitcher — Floating Design System Switcher

A self-contained floating button at the bottom-left of every generated deck. Opens a compact popup with all 8 preset cards (name + bg swatch + accent dot). Clicking a preset swaps all CSS variables on `:root` instantly and loads the matching Google Fonts on demand. Does not interfere with `SlideEngine` keyboard navigation — Escape closes the panel without triggering slide nav.

**Always include this component in every generated slide deck.** It costs zero performance (CSS/JS injected once, fonts loaded lazily) and is invaluable for client presentations where you want to compare visual directions live.

```html
<!-- Add immediately after SlideEngine script, before </body> -->
<script>
    (function () {
        /* --- PRESET MAP ---
     Each entry: id, name, dark flag, bg/accent for swatch,
     fonts (Google Fonts URL), vars (CSS variable map applied to :root).
     Keep in sync with the 8 presets in slide-patterns.md. --- */
        var PRESETS = [
            /* ... copy from slide-deck.html template ... */
        ];

        function ThemeSwitcher() {
            this.current = this._detect();
            this._loaded = {};
            this._build();
            this._apply(this.current, false);
        }

        /* _detect: match current --accent to find active preset index */
        ThemeSwitcher.prototype._detect = function () {
            /* ... */
        };

        /* _build: inject CSS, create .ts-btn toggle + .ts-panel popup */
        ThemeSwitcher.prototype._build = function () {
            /* ... */
        };

        /* _apply(idx, animate): set CSS vars, lazy-load fonts, flash deck */
        ThemeSwitcher.prototype._apply = function (idx, animate) {
            /* ... */
        };

        document.addEventListener("DOMContentLoaded", function () {
            new ThemeSwitcher();
        });
    })();
</script>
```

**Full implementation is in `./templates/slide-deck.html`** — copy the ThemeSwitcher `<script>` block verbatim. Do not rewrite it from scratch; the minified event delegation and variable maps are carefully tuned.

### ThemeSwitcher CSS Classes

| Class                                 | Role                                                     |
| ------------------------------------- | -------------------------------------------------------- |
| `.ts-btn`                             | Fixed 40px circle toggle, bottom-left, `z-index: 200`    |
| `.ts-panel`                           | Popup panel, `280px` wide, `backdrop-filter: blur(20px)` |
| `.ts-panel.ts-off`                    | Hidden state: `opacity:0 + scale(0.88)`                  |
| `.ts-grid`                            | 2-column preset grid inside panel                        |
| `.ts-card`                            | Individual preset card (swatch + name + check)           |
| `.ts-card.ts-on`                      | Active preset indicator                                  |
| `.ts-sw` / `.ts-sw-bg` / `.ts-sw-dot` | Swatch: bg fill + accent dot                             |

### Position Rules

- Toggle button: `bottom-left` — opposite side from nav dots (`bottom-right`/`right-center`)
- Panel: opens upward from the button (`bottom: btn_height + gap`)
- `z-index: 200` — above `SlideEngine` chrome which is `z-index: 100`
- Closes on: outside click, `Escape` key, preset selection

## SlideEngine JavaScript

Add once at the end of the page. Handles navigation, chrome updates, and scroll-triggered reveals. Event delegation ensures slide-internal interactions (Mermaid zoom, scrollable code, overflow tables) don't trigger slide navigation.

```javascript
class SlideEngine {
    constructor() {
        this.deck = document.querySelector(".deck");
        this.slides = [...document.querySelectorAll(".slide")];
        this.current = 0;
        this.total = this.slides.length;
        this.buildChrome();
        this.bindEvents();
        this.observe();
        this.update();
    }

    buildChrome() {
        // Progress bar
        var bar = document.createElement("div");
        bar.className = "deck-progress";
        document.body.appendChild(bar);
        this.bar = bar;

        // Nav dots
        var dots = document.createElement("div");
        dots.className = "deck-dots";
        var self = this;
        this.slides.forEach(function (_, i) {
            var d = document.createElement("button");
            d.className = "deck-dot";
            d.title = "Slide " + (i + 1);
            d.onclick = function () {
                self.goTo(i);
            };
            dots.appendChild(d);
        });
        document.body.appendChild(dots);
        this.dots = [].slice.call(dots.children);

        // Counter
        var ctr = document.createElement("div");
        ctr.className = "deck-counter";
        document.body.appendChild(ctr);
        this.counter = ctr;

        // Keyboard hints
        var hints = document.createElement("div");
        hints.className = "deck-hints";
        hints.textContent = "\u2190 \u2192 or scroll to navigate";
        document.body.appendChild(hints);
        this.hints = hints;
        this.hintTimer = setTimeout(function () {
            hints.classList.add("faded");
        }, 4000);
    }

    bindEvents() {
        var self = this;
        // Keyboard — skip if focus is inside interactive content
        document.addEventListener("keydown", function (e) {
            if (e.target.closest(".mermaid-wrap, .table-scroll, .code-scroll, input, textarea, [contenteditable]")) return;
            if (["ArrowDown", "ArrowRight", " ", "PageDown"].includes(e.key)) {
                e.preventDefault();
                self.next();
            } else if (["ArrowUp", "ArrowLeft", "PageUp"].includes(e.key)) {
                e.preventDefault();
                self.prev();
            } else if (e.key === "Home") {
                e.preventDefault();
                self.goTo(0);
            } else if (e.key === "End") {
                e.preventDefault();
                self.goTo(self.total - 1);
            }
            self.fadeHints();
        });

        // Touch swipe
        var touchY;
        this.deck.addEventListener(
            "touchstart",
            function (e) {
                touchY = e.touches[0].clientY;
            },
            { passive: true },
        );
        this.deck.addEventListener("touchend", function (e) {
            var dy = touchY - e.changedTouches[0].clientY;
            if (Math.abs(dy) > 50) {
                dy > 0 ? self.next() : self.prev();
            }
        });
    }

    observe() {
        var self = this;
        var obs = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("visible");
                        self.current = self.slides.indexOf(entry.target);
                        self.update();
                    }
                });
            },
            { threshold: 0.5 },
        );
        this.slides.forEach(function (s) {
            obs.observe(s);
        });
    }

    goTo(i) {
        this.slides[Math.max(0, Math.min(i, this.total - 1))].scrollIntoView({ behavior: "smooth" });
    }

    next() {
        if (this.current < this.total - 1) this.goTo(this.current + 1);
    }
    prev() {
        if (this.current > 0) this.goTo(this.current - 1);
    }

    update() {
        this.bar.style.width = ((this.current + 1) / this.total) * 100 + "%";
        var self = this;
        this.dots.forEach(function (d, i) {
            d.classList.toggle("active", i === self.current);
        });
        this.counter.textContent = this.current + 1 + " / " + this.total;
    }

    fadeHints() {
        clearTimeout(this.hintTimer);
        this.hints.classList.add("faded");
    }
}
```

**Usage:** Instantiate after the DOM is ready and any libraries (Mermaid, Chart.js) have rendered. Always call `autoFit()` before `new SlideEngine()` so content is sized correctly before intersection observers fire.

```html
<script>
    // After Mermaid/Chart.js initialization (if used), or at end of <body>:
    document.addEventListener("DOMContentLoaded", function () {
        autoFit();
        new SlideEngine();
    });
</script>
```

## Auto-Fit

A single post-render function that handles all known content overflow cases. Agents can't perfectly predict how text reflows at every viewport size, so `autoFit()` is a required safety net. Call it after Mermaid/Chart.js render but before SlideEngine init.

```javascript
function autoFit() {
    // Mermaid SVGs: fill container instead of rendering at intrinsic size
    document.querySelectorAll(".mermaid svg").forEach(function (svg) {
        svg.removeAttribute("height");
        svg.style.width = "100%";
        svg.style.maxWidth = "100%";
        svg.style.height = "auto";
        svg.parentElement.style.width = "100%";
    });

    // KPI values: visually scale down text that overflows card width
    document.querySelectorAll(".slide__kpi-val").forEach(function (el) {
        if (el.scrollWidth > el.clientWidth) {
            var s = el.clientWidth / el.scrollWidth;
            el.style.transform = "scale(" + s + ")";
            el.style.transformOrigin = "left top";
        }
    });

    // Blockquotes: reduce font proportionally for long text
    document.querySelectorAll(".slide--quote blockquote").forEach(function (el) {
        var len = el.textContent.trim().length;
        if (len > 100) {
            var scale = Math.max(0.5, 100 / len);
            var fs = parseFloat(getComputedStyle(el).fontSize);
            el.style.fontSize = Math.max(16, Math.round(fs * scale)) + "px";
        }
    });
}
```

Three cases, one function:

- **Mermaid:** SVGs render with fixed dimensions inside flex containers — force them to fill available width.
- **KPI values:** Long text strings at hero scale overflow card boundaries — `transform: scale()` shrinks visually without reflow.
- **Blockquotes:** Quotes longer than ~100 characters get proportionally smaller font. The 0.5 floor prevents unreadably small text; if it needs more than 50% shrink, it should have been a content slide.

## Slide Type Layouts

Each type has a defined HTML structure and CSS layout. The agent can adapt colors, fonts, and spacing per aesthetic, but the structural patterns stay consistent.

### Title Slide

Full-viewport hero. Background treatment via gradient, texture, or surf-generated image. 80–120px display type.

```html
<section class="slide slide--title">
    <svg class="slide__decor" ...><!-- optional decorative accent --></svg>
    <div class="slide__content reveal">
        <h1 class="slide__display">Deck Title</h1>
        <p class="slide__subtitle reveal">Subtitle or date</p>
    </div>
</section>
```

```css
.slide--title {
    justify-content: center;
    align-items: center;
    text-align: center;
}
```

### Section Divider

Oversized decorative number (200px+, ultra-light weight) with heading. Breathing room between topics. SVG accent marks optional.

```html
<section class="slide slide--divider">
    <span class="slide__number">02</span>
    <div class="slide__content">
        <h2 class="slide__heading reveal">Section Title</h2>
        <p class="slide__subtitle reveal">Optional subheading</p>
    </div>
</section>
```

```css
.slide--divider {
    justify-content: center;
}

.slide--divider .slide__number {
    font-size: clamp(100px, 22vw, 260px);
    font-weight: 200;
    line-height: 0.85;
    opacity: 0.08;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -55%);
    pointer-events: none;
    font-variant-numeric: tabular-nums;
}
```

### Content Slide

Heading + bullets or paragraphs. Asymmetric layout — content offset to one side. Max 5–6 bullets (2 lines each).

```html
<section class="slide slide--content">
    <div class="slide__inner">
        <div class="slide__text">
            <h2 class="slide__heading reveal">Heading</h2>
            <ul class="slide__bullets">
                <li class="reveal">First point</li>
                <li class="reveal">Second point</li>
            </ul>
        </div>
        <div class="slide__aside reveal">
            <!-- optional: illustration, icon, mini-diagram, accent SVG -->
        </div>
    </div>
</section>
```

```css
.slide--content .slide__inner {
    display: grid;
    grid-template-columns: 3fr 2fr;
    gap: clamp(24px, 4vw, 60px);
    align-items: center;
    width: 100%;
}

/* For right-heavy variant: swap to 2fr 3fr */
.slide--content .slide__bullets {
    list-style: none;
    padding: 0;
}

.slide--content .slide__bullets li {
    padding: 8px 0 8px 20px;
    position: relative;
    font-size: clamp(16px, 2vw, 22px);
    line-height: 1.6;
    color: var(--text-dim);
}

.slide--content .slide__bullets li::before {
    content: "";
    position: absolute;
    left: 0;
    top: 18px;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent);
}
```

### Split Slide

Asymmetric two-panel (60/40 or 70/30). Before/after, text+diagram, text+image. Each panel has its own background tier. Zero padding on the slide itself — panels fill edge to edge.

```html
<section class="slide slide--split">
    <div class="slide__panels">
        <div class="slide__panel slide__panel--primary">
            <h2 class="slide__heading reveal">Left Panel</h2>
            <div class="slide__body reveal">Content...</div>
        </div>
        <div class="slide__panel slide__panel--secondary">
            <!-- diagram, image, code block, or contrasting content -->
        </div>
    </div>
</section>
```

```css
.slide--split {
    padding: 0;
}

.slide--split .slide__panels {
    display: grid;
    grid-template-columns: 3fr 2fr;
    height: 100%;
}

.slide--split .slide__panel {
    padding: clamp(40px, 6vh, 80px) clamp(32px, 4vw, 60px);
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.slide--split .slide__panel--primary {
    background: var(--surface);
}

.slide--split .slide__panel--secondary {
    background: var(--surface2);
}
```

### Diagram Slide

Full-viewport Mermaid diagram. Max 8–10 nodes (presentation scale — fewer, larger than page diagrams). Node labels at 18px+, edges at 2px+. Zoom controls from `css-patterns.md` apply here.

**When to use Mermaid vs CSS in slides.** Mermaid renders SVGs at a fixed size the agent can't control — node dimensions are set by the library, not by CSS. This creates a recurring problem: small diagrams (fewer than ~7 nodes, no branching) render as tiny elements floating in a huge viewport with acres of dead space. The rule:

- **Use Mermaid** for complex graphs: 8+ nodes, branching paths, cycles, multiple edge crossings — anything where automatic edge routing saves real effort.
- **Use CSS Pipeline** (below) for simple linear flows: A → B → C → D sequences, build steps, deployment stages. CSS cards give full control over sizing, typography, and fill the viewport naturally.
- **Never leave a small Mermaid diagram alone on a slide.** If the diagram is small, either switch to CSS, or pair it with supporting content (description cards, bullet annotations, a summary panel) in a split layout. A slide with a tiny diagram and empty space is a failed slide.

**Mermaid centering fix.** When you do use Mermaid, add `display: flex; align-items: center; justify-content: center;` to `.mermaid-wrap` so the SVG centers within its container instead of hugging the top-left corner. Change `transform-origin` to `center center` so zoom radiates from the middle.

```html
<section class="slide slide--diagram">
    <h2 class="slide__heading reveal">Diagram Title</h2>
    <div class="mermaid-wrap reveal" style="flex:1; min-height:0;">
        <div class="zoom-controls">
            <button onclick="zoomDiagram(this,1.2)" title="Zoom in">+</button>
            <button onclick="zoomDiagram(this,0.8)" title="Zoom out">&minus;</button>
            <button onclick="resetZoom(this)" title="Reset">&#8634;</button>
            <button onclick="openDiagramFullscreen(this)" title="Open full size in new tab">&#x26F6;</button>
        </div>
        <pre class="mermaid">
      graph TD
        A --> B
    </pre
        >
    </div>
</section>
```

**Click to expand.** Clicking anywhere on the diagram (without dragging) opens it full-size in a new browser tab. The expand button (⛶) provides the same functionality for discoverability.

```css
.slide--diagram {
    padding: clamp(24px, 4vh, 48px) clamp(24px, 4vw, 60px);
}

.slide--diagram .slide__heading {
    margin-bottom: clamp(8px, 1.5vh, 20px);
}

.slide--diagram .mermaid-wrap {
    border-radius: 12px;
    overflow: auto;
    display: flex;
    align-items: center;
    justify-content: center;
}

.slide--diagram .mermaid-wrap .mermaid {
    transform-origin: center center;
}
```

**Auto-fit SVG to container.** Mermaid renders SVGs with fixed dimensions and an inline `max-width` style that keeps diagrams tiny inside large slides. The `autoFit()` function (see above) handles this at runtime. Keep the CSS as a belt-and-suspenders fallback:

```css
.slide--diagram .mermaid svg {
    width: 100% !important;
    height: auto !important;
    max-width: 100% !important;
}
```

**Mermaid overrides for presentation scale** (add alongside the standard Mermaid CSS overrides from `libraries.md`):

```css
.slide--diagram .mermaid .nodeLabel {
    font-size: 18px !important;
}

.slide--diagram .mermaid .edgeLabel {
    font-size: 14px !important;
}

.slide--diagram .mermaid .node rect,
.slide--diagram .mermaid .node circle,
.slide--diagram .mermaid .node polygon {
    stroke-width: 2px;
}

.slide--diagram .mermaid .edge-pattern-solid {
    stroke-width: 2px;
}
```

### CSS Pipeline Slide

For simple linear flows (build steps, deployment stages, data pipelines) where Mermaid would render too small. CSS cards with arrow connectors give full control over sizing and fill the viewport naturally. Each step card expands to fill available space via `flex: 1`.

```html
<section class="slide" style="background-image:radial-gradient(...);">
    <p class="slide__label reveal">Pipeline Label</p>
    <h2 class="slide__heading reveal">Pipeline Title</h2>
    <div class="pipeline reveal">
        <div class="pipeline__step" style="border-top-color:var(--accent);">
            <div class="pipeline__num">01</div>
            <div class="pipeline__name">Step Name</div>
            <div class="pipeline__desc">What this step produces or does</div>
            <div class="pipeline__file">output-file.md</div>
        </div>
        <div class="pipeline__arrow">
            <svg viewBox="0 0 24 24" width="20" height="20"><path d="M5 12h14m-4-4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
        </div>
        <div class="pipeline__step">...</div>
        <!-- repeat step + arrow pairs -->
    </div>
</section>
```

```css
.pipeline {
    display: flex;
    align-items: stretch;
    gap: 0;
    flex: 1;
    min-height: 0;
    margin-top: clamp(12px, 2vh, 24px);
}

.pipeline__step {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-top: 3px solid var(--accent);
    border-radius: 10px;
    padding: clamp(14px, 2.5vh, 28px) clamp(12px, 1.5vw, 22px);
    display: flex;
    flex-direction: column;
    min-width: 0;
    overflow-wrap: break-word;
}

.pipeline__num {
    font-size: clamp(10px, 1.2vw, 13px);
    font-weight: 600;
    color: var(--accent);
    letter-spacing: 1px;
}

.pipeline__name {
    font-size: clamp(16px, 2vw, 24px);
    font-weight: 700;
    margin: clamp(4px, 0.8vh, 8px) 0;
}

.pipeline__desc {
    font-size: clamp(12px, 1.3vw, 16px);
    color: var(--text-dim);
    line-height: 1.5;
    flex: 1;
}

.pipeline__file {
    font-size: clamp(10px, 1.1vw, 12px);
    color: var(--accent);
    background: var(--accent-dim);
    padding: 3px 8px;
    border-radius: 4px;
    margin-top: clamp(8px, 1.5vh, 16px);
    align-self: flex-start;
}

.pipeline__arrow {
    display: flex;
    align-items: center;
    padding: 0 clamp(3px, 0.4vw, 6px);
    color: var(--accent);
    flex-shrink: 0;
    opacity: 0.4;
}

@media (max-width: 768px) {
    .pipeline {
        flex-direction: column;
    }
    .pipeline__arrow {
        justify-content: center;
        padding: 4px 0;
        transform: rotate(90deg);
    }
}
```

Each `.pipeline__step` uses `flex: 1` to fill available width equally, and the pipeline container itself uses `flex: 1` to fill available vertical space in the slide. Step cards stretch to fill, so the content isn't floating in empty space. The `.pipeline__file` badge at the bottom anchors each card and adds a practical detail. Max 5–6 steps — beyond that, split across two slides.

### Dashboard Slide

KPI cards at presentation scale (48–64px hero numbers). Mini-charts via Chart.js or SVG sparklines. Max 6 KPIs.

```html
<section class="slide slide--dashboard">
    <h2 class="slide__heading reveal">Metrics Overview</h2>
    <div class="slide__kpis">
        <div class="slide__kpi reveal">
            <div class="slide__kpi-val" style="color:var(--accent)">247</div>
            <div class="slide__kpi-label">Lines Added</div>
        </div>
        <!-- more KPI cards -->
    </div>
</section>
```

```css
.slide--dashboard .slide__kpis {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(clamp(140px, 20vw, 220px), 1fr));
    gap: clamp(12px, 2vw, 24px);
}

.slide__kpi {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: clamp(16px, 3vh, 32px) clamp(16px, 2vw, 24px);
    min-width: 0;
    overflow: hidden;
}

.slide__kpi-val {
    font-size: clamp(36px, 6vw, 64px);
    font-weight: 800;
    letter-spacing: -1.5px;
    line-height: 1.1;
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
}

.slide__kpi-label {
    font-family: var(--font-mono);
    font-size: clamp(9px, 1.2vw, 13px);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--text-dim);
    margin-top: 8px;
}
```

**KPI hero values should be short** — numbers, percentages, 1–3 word labels. Ideal length is 1–6 characters at hero scale. Longer strings like `store=false` break the layout at 64px. If you must show a longer value, put it in the label or body text instead. The `autoFit()` function (see below) will scale down overflows as a safety net.

### Table Slide

18–20px cell text for projection readability. Max 8 rows per slide — overflow paginates to the next slide. Stronger alternating row contrast than page tables.

```html
<section class="slide slide--table">
    <h2 class="slide__heading reveal">Data Title</h2>
    <div class="table-wrap reveal" style="flex:1; min-height:0;">
        <div class="table-scroll">
            <table class="data-table">
                ...
            </table>
        </div>
    </div>
</section>
```

```css
.slide--table {
    padding: clamp(24px, 4vh, 48px) clamp(24px, 4vw, 60px);
}

.slide--table .data-table {
    font-size: clamp(14px, 1.8vw, 20px);
}

.slide--table .data-table th {
    font-size: clamp(10px, 1.3vw, 14px);
    padding: clamp(8px, 1.5vh, 14px) clamp(12px, 2vw, 20px);
}

.slide--table .data-table td {
    padding: clamp(10px, 1.5vh, 16px) clamp(12px, 2vw, 20px);
}
```

### Code Slide

18px mono on a recessed dark background. Max 10 lines. Floating filename label. Centered on the viewport for focus.

```html
<section class="slide slide--code">
    <h2 class="slide__heading reveal">What Changed</h2>
    <div class="slide__code-block reveal">
        <span class="slide__code-filename">worker.ts</span>
        <pre><code>function processQueue(items) {
  // highlighted code here
}</code></pre>
    </div>
</section>
```

```css
.slide--code {
    align-items: center;
}

.slide__code-block {
    background: var(--code-bg, #1a1a2e);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: clamp(24px, 4vh, 48px) clamp(24px, 4vw, 48px);
    max-width: 900px;
    width: 100%;
    position: relative;
}

.slide__code-filename {
    position: absolute;
    top: -12px;
    left: 24px;
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 4px;
    background: var(--accent);
    color: var(--bg);
}

.slide__code-block pre {
    margin: 0;
    overflow-x: auto;
}

.slide__code-block code {
    font-family: var(--font-mono);
    font-size: clamp(14px, 1.6vw, 18px);
    line-height: 1.7;
    color: var(--code-text, #e6edf3);
}
```

### Quote Slide

36–48px serif with dramatic line-height. Oversized quotation mark as SVG or typographic decoration. Generous whitespace is the design.

```html
<section class="slide slide--quote">
    <div class="slide__quote-mark reveal">&ldquo;</div>
    <blockquote class="reveal">The best code is the code you don't have to write.</blockquote>
    <cite class="reveal">&mdash; Someone Wise</cite>
</section>
```

```css
.slide--quote {
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: clamp(60px, 10vh, 120px) clamp(60px, 12vw, 200px);
}

.slide__quote-mark {
    font-size: clamp(80px, 14vw, 180px);
    line-height: 0.5;
    opacity: 0.08;
    font-family: Georgia, serif;
    pointer-events: none;
    margin-bottom: -20px;
}

.slide--quote blockquote {
    font-size: clamp(24px, 4vw, 48px);
    font-weight: 400;
    line-height: 1.35;
    font-style: italic;
    margin: 0;
}

.slide--quote cite {
    font-family: var(--font-mono);
    font-size: clamp(11px, 1.4vw, 14px);
    font-style: normal;
    margin-top: clamp(16px, 3vh, 32px);
    display: block;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-dim);
}
```

### Full-Bleed Slide

Background image (surf-generated or CSS gradient) dominates the viewport. Text overlay with gradient scrim ensuring contrast. Zero slide padding.

```html
<section class="slide slide--bleed">
    <div class="slide__bg" style="background-image:url('data:image/png;base64,...')"></div>
    <div class="slide__scrim"></div>
    <div class="slide__content">
        <h2 class="slide__heading reveal">Headline Over Image</h2>
        <p class="slide__subtitle reveal">Supporting text</p>
    </div>
</section>
```

```css
.slide--bleed {
    padding: 0;
    justify-content: flex-end;
    color: #ffffff;
}

.slide__bg {
    position: absolute;
    inset: 0;
    background-size: cover;
    background-position: center;
    z-index: 0;
}

.slide__scrim {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.7) 0%, rgba(0, 0, 0, 0.1) 50%, transparent 100%);
    z-index: 1;
}

.slide--bleed .slide__content {
    position: relative;
    z-index: 2;
    padding: clamp(40px, 6vh, 80px) clamp(40px, 8vw, 120px);
}

/* When no generated image, use a bold CSS gradient background */
.slide__bg--gradient {
    background: linear-gradient(135deg, var(--accent) 0%, color-mix(in srgb, var(--accent) 60%, var(--bg) 40%) 100%);
}
```

### Timeline Slide

Horizontal chronological axis with dots, dates, and content cards. CSS-native — do not use Mermaid for timelines. Max 5–6 milestones. Events alternate above/below the axis on wide viewports; collapse to single-column on mobile. Ideal for project roadmaps, delivery phases, and historical context slides.

```html
<section class="slide slide--timeline">
    <p class="slide__label reveal">Timeline</p>
    <h2 class="slide__heading reveal">Project Roadmap</h2>
    <div class="timeline reveal">
        <div class="timeline__track"></div>
        <div class="timeline__item timeline__item--above">
            <div class="timeline__content">
                <div class="timeline__date">Q1 2024</div>
                <div class="timeline__title">Phase Discovery</div>
                <div class="timeline__desc">Cadrage, interviews, architecture initiale</div>
            </div>
            <div class="timeline__dot"></div>
        </div>
        <div class="timeline__item timeline__item--below">
            <div class="timeline__dot"></div>
            <div class="timeline__content">
                <div class="timeline__date">Q2 2024</div>
                <div class="timeline__title">Phase Build</div>
                <div class="timeline__desc">Développement, tests intégration, recette</div>
            </div>
        </div>
        <!-- alternate above/below for each milestone -->
    </div>
</section>
```

```css
.slide--timeline {
    padding: clamp(32px, 5vh, 60px) clamp(40px, 8vw, 120px);
}

.timeline {
    position: relative;
    display: flex;
    align-items: stretch;
    gap: 0;
    flex: 1;
    min-height: 0;
    margin-top: clamp(16px, 2.5vh, 32px);
}

.timeline__track {
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    height: 2px;
    background: var(--border-bright);
    transform: translateY(-50%);
    z-index: 0;
}

.timeline__item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: clamp(8px, 1.5vh, 16px);
    position: relative;
    z-index: 1;
    min-width: 0;
}

.timeline__item--above {
    flex-direction: column-reverse; /* content above, dot below */
}

.timeline__item--below {
    flex-direction: column; /* dot above, content below */
}

.timeline__dot {
    width: clamp(10px, 1.5vw, 16px);
    height: clamp(10px, 1.5vw, 16px);
    border-radius: 50%;
    background: var(--accent);
    border: 3px solid var(--bg);
    box-shadow: 0 0 0 2px var(--accent);
    flex-shrink: 0;
}

.timeline__content {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: clamp(10px, 1.5vh, 18px) clamp(10px, 1.2vw, 16px);
    width: 100%;
    min-width: 0;
    overflow-wrap: break-word;
}

.timeline__date {
    font-family: var(--font-mono);
    font-size: clamp(9px, 1vw, 11px);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--accent);
    margin-bottom: 4px;
}

.timeline__title {
    font-size: clamp(13px, 1.5vw, 18px);
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 4px;
}

.timeline__desc {
    font-size: clamp(10px, 1.1vw, 13px);
    color: var(--text-dim);
    line-height: 1.4;
}

@media (max-width: 768px) {
    .timeline {
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
    }
    .timeline__track {
        top: 0;
        bottom: 0;
        left: 16px;
        width: 2px;
        height: auto;
        transform: none;
    }
    .timeline__item,
    .timeline__item--above,
    .timeline__item--below {
        flex-direction: row;
        align-items: flex-start;
        gap: 16px;
    }
    .timeline__dot {
        margin-top: 4px;
    }
}
```

### Comparison Slide

Two-column grid for before/after, option A vs B, or pros/cons. Each row is a criterion. Winner cells get a visual highlight. Distinct from Split (which is a free-form two-panel) — this is a structured comparison table rendered as CSS cards, not an HTML `<table>`. Max 6–7 rows.

```html
<section class="slide slide--compare">
    <h2 class="slide__heading reveal">Approche Custom vs. Natif ServiceNow</h2>
    <div class="compare reveal">
        <div class="compare__header">
            <div class="compare__criterion-head"></div>
            <div class="compare__col-label">Custom Table</div>
            <div class="compare__col-label compare__col-label--accent">Native ast_contract</div>
        </div>
        <div class="compare__row">
            <div class="compare__criterion">Maintenabilité</div>
            <div class="compare__cell compare__cell--lose">Risque upgrade élevé</div>
            <div class="compare__cell compare__cell--win">Upgrade-safe OOB</div>
        </div>
        <div class="compare__row">
            <div class="compare__criterion">Time-to-value</div>
            <div class="compare__cell">4–6 semaines</div>
            <div class="compare__cell compare__cell--win">2–3 semaines</div>
        </div>
        <!-- up to 6-7 rows -->
    </div>
</section>
```

```css
.slide--compare {
    padding: clamp(28px, 4vh, 52px) clamp(40px, 8vw, 120px);
}

.compare {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 0;
    gap: 0;
    margin-top: clamp(12px, 2vh, 24px);
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border);
}

.compare__header {
    display: grid;
    grid-template-columns: 2fr 3fr 3fr;
    background: var(--surface2);
    border-bottom: 2px solid var(--border-bright);
}

.compare__col-label {
    padding: clamp(10px, 1.5vh, 16px) clamp(12px, 1.5vw, 20px);
    font-family: var(--font-mono);
    font-size: clamp(10px, 1.2vw, 14px);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-dim);
}

.compare__col-label--accent {
    color: var(--accent);
    background: var(--accent-dim);
}

.compare__criterion-head {
    padding: clamp(10px, 1.5vh, 16px) clamp(12px, 1.5vw, 20px);
}

.compare__row {
    display: grid;
    grid-template-columns: 2fr 3fr 3fr;
    border-bottom: 1px solid var(--border);
}

.compare__row:last-child {
    border-bottom: none;
}

.compare__row:nth-child(odd) {
    background: var(--surface);
}

.compare__row:nth-child(even) {
    background: var(--surface2);
}

.compare__criterion {
    padding: clamp(10px, 1.5vh, 14px) clamp(12px, 1.5vw, 20px);
    font-size: clamp(12px, 1.4vw, 16px);
    font-weight: 600;
    color: var(--text-dim);
    display: flex;
    align-items: center;
}

.compare__cell {
    padding: clamp(10px, 1.5vh, 14px) clamp(12px, 1.5vw, 20px);
    font-size: clamp(12px, 1.4vw, 16px);
    line-height: 1.4;
    display: flex;
    align-items: center;
    border-left: 1px solid var(--border);
}

.compare__cell--win {
    color: var(--accent);
    background: var(--accent-dim);
    font-weight: 600;
}

.compare__cell--lose {
    color: var(--text-dim);
    opacity: 0.7;
}

@media (max-width: 768px) {
    .compare__header,
    .compare__row {
        grid-template-columns: 1fr 1fr;
    }
    .compare__criterion,
    .compare__criterion-head {
        display: none;
    }
}
```

### Process Steps Slide

Vertical numbered steps with connecting lines. For human/organizational processes — onboarding, delivery methodologies, escalation paths. Distinct from the CSS Pipeline (which is horizontal and technical). Max 4–5 steps. Steps expand vertically to fill available space via `flex: 1`.

```html
<section class="slide slide--process">
    <p class="slide__label reveal">Méthodologie</p>
    <h2 class="slide__heading reveal">Notre processus de delivery</h2>
    <div class="process reveal">
        <div class="process__step">
            <div class="process__marker">
                <div class="process__num">01</div>
                <div class="process__connector"></div>
            </div>
            <div class="process__content">
                <div class="process__title">Cadrage</div>
                <div class="process__desc">Identification des besoins, qualification du périmètre, estimation forfaitaire</div>
                <div class="process__badge">2–3 jours</div>
            </div>
        </div>
        <div class="process__step">
            <div class="process__marker">
                <div class="process__num">02</div>
                <div class="process__connector"></div>
            </div>
            <div class="process__content">
                <div class="process__title">Architecture</div>
                <div class="process__desc">Design de solution, choix techniques, ADRs, validation client</div>
                <div class="process__badge">1 semaine</div>
            </div>
        </div>
        <!-- repeat process__step, last step omits process__connector -->
    </div>
</section>
```

```css
.slide--process {
    padding: clamp(32px, 5vh, 64px) clamp(40px, 8vw, 120px);
}

.process {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 0;
    gap: 0;
    margin-top: clamp(12px, 2vh, 24px);
}

.process__step {
    display: flex;
    gap: clamp(16px, 2.5vw, 32px);
    flex: 1;
    min-height: 0;
}

.process__marker {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
}

.process__num {
    width: clamp(32px, 4vw, 48px);
    height: clamp(32px, 4vw, 48px);
    border-radius: 50%;
    background: var(--accent-dim);
    border: 2px solid var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-mono);
    font-size: clamp(10px, 1.2vw, 13px);
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 0.5px;
    flex-shrink: 0;
}

.process__connector {
    width: 2px;
    flex: 1;
    background: var(--border-bright);
    margin: 6px 0;
}

.process__content {
    flex: 1;
    padding-bottom: clamp(12px, 2vh, 24px);
    padding-top: clamp(4px, 0.6vh, 8px);
    min-width: 0;
}

.process__title {
    font-size: clamp(16px, 2vw, 24px);
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: clamp(4px, 0.8vh, 8px);
}

.process__desc {
    font-size: clamp(12px, 1.4vw, 16px);
    color: var(--text-dim);
    line-height: 1.55;
    flex: 1;
}

.process__badge {
    display: inline-block;
    margin-top: clamp(6px, 1vh, 12px);
    font-family: var(--font-mono);
    font-size: clamp(9px, 1.1vw, 12px);
    font-weight: 600;
    color: var(--accent);
    background: var(--accent-dim);
    padding: 3px 10px;
    border-radius: 4px;
    letter-spacing: 0.5px;
}

@media (max-width: 768px) {
    .process__connector {
        display: none;
    }
}
```

## Decorative SVG Elements

Inline SVG accents lift slides from functional to editorial. Use sparingly — one or two per slide, never on every slide.

### Corner Accent

```html
<!-- Top-right corner mark -->
<svg class="slide__decor slide__decor--corner" width="120" height="120" viewBox="0 0 120 120">
    <line x1="120" y1="0" x2="120" y2="40" stroke="var(--accent)" stroke-width="2" opacity="0.2" />
    <line x1="80" y1="0" x2="120" y2="0" stroke="var(--accent)" stroke-width="2" opacity="0.2" />
</svg>
```

```css
.slide__decor {
    position: absolute;
    pointer-events: none;
    z-index: 0;
}

.slide__decor--corner {
    top: 0;
    right: 0;
}
```

### Section Divider Mark

```html
<!-- Horizontal rule with diamond -->
<svg class="slide__decor slide__decor--divider" width="200" height="20" viewBox="0 0 200 20">
    <line x1="0" y1="10" x2="85" y2="10" stroke="var(--accent)" stroke-width="1" opacity="0.3" />
    <rect x="92" y="3" width="14" height="14" transform="rotate(45 99 10)" fill="none" stroke="var(--accent)" stroke-width="1" opacity="0.3" />
    <line x1="115" y1="10" x2="200" y2="10" stroke="var(--accent)" stroke-width="1" opacity="0.3" />
</svg>
```

### Geometric Background Pattern

```css
/* Faint grid dots behind a slide */
.slide--with-grid::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image: radial-gradient(circle, var(--border) 1px, transparent 1px);
    background-size: 32px 32px;
    opacity: 0.5;
    pointer-events: none;
    z-index: 0;
}
```

### Per-Slide Background Variation

Vary gradient direction and accent glow position across slides to create visual rhythm. Don't use a uniform background for every slide.

```css
/* Vary these per slide via inline style or nth-child */
.slide:nth-child(odd) {
    background-image: radial-gradient(ellipse at 20% 80%, var(--accent-dim) 0%, transparent 50%);
}

.slide:nth-child(even) {
    background-image: radial-gradient(ellipse at 80% 20%, var(--accent-dim) 0%, transparent 50%);
}
```

## Global Visual Improvements

Cross-cutting patterns that apply to all presets and slide types. These augment the existing patterns without replacing them.

### Secondary Accent — `--accent-2`

Bauhaus Constructivist and ELO Blue define `--accent-2`. All other presets may optionally add it as a lighter/complementary tint of the primary accent. Rule: `--accent-2` is never used for primary emphasis — it's reserved for secondary KPI values, supporting labels, sparklines on non-primary metrics, and subtle highlights that contrast with `--accent` without competing with it.

```css
/* If a preset lacks --accent-2, define a sensible default: */
:root {
    --accent-2: color-mix(in srgb, var(--accent) 60%, var(--text) 40%);
}
```

### Additional Background Patterns

These extend the existing `--with-grid` dot pattern. Apply to individual slides via class or inline style — not globally.

```css
/* Noise / grain texture via SVG filter (subtle paper feel) */
.slide--with-grain::before {
    content: "";
    position: absolute;
    inset: 0;
    opacity: 0.04;
    pointer-events: none;
    z-index: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    background-repeat: repeat;
    background-size: 200px 200px;
}

/* Diagonal hairlines — Bauhaus / technical feel */
.slide--with-diagonals::before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background-image: repeating-linear-gradient(-45deg, var(--border) 0px, var(--border) 1px, transparent 1px, transparent 28px);
    opacity: 0.6;
}

/* Halftone dot grid — denser than --with-grid, more graphic */
.slide--with-halftone::before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background-image: radial-gradient(circle, var(--border-bright) 1.5px, transparent 1.5px);
    background-size: 20px 20px;
    opacity: 0.4;
}
```

**When to use:** `--with-grain` fits Velvet Editorial and Fog Minimalist (paper warmth). `--with-diagonals` fits Bauhaus Constructivist and Swiss Clean (precision). `--with-halftone` fits Terminal Mono and ELO Blue (technical platform). Never use more than one background pattern on the same slide.

### KPI Sparkline Pattern

A standard SVG inline sparkline paired with a KPI value. Add to any `.slide__kpi` card. The sparkline communicates trend without a full Chart.js canvas — zero external dependencies.

```html
<div class="slide__kpi reveal">
    <div class="slide__kpi-header">
        <div class="slide__kpi-val" style="color:var(--accent)">94%</div>
        <!-- Inline sparkline: polyline points are normalized 0–40 height, width per point = 10px -->
        <svg class="slide__kpi-spark" viewBox="0 0 70 40" preserveAspectRatio="none">
            <polyline points="0,35 10,28 20,30 30,18 40,22 50,12 60,8 70,5" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <polyline points="0,35 10,28 20,30 30,18 40,22 50,12 60,8 70,5 70,40 0,40" fill="var(--accent-dim)" stroke="none" />
        </svg>
    </div>
    <div class="slide__kpi-label">SLA Compliance</div>
</div>
```

```css
.slide__kpi-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 8px;
}

.slide__kpi-spark {
    width: clamp(50px, 6vw, 80px);
    height: clamp(24px, 3vh, 36px);
    opacity: 0.9;
    flex-shrink: 0;
}
```

**Generating sparkline points:** Normalize your data series to the 0–40 range (40 = bottom, 0 = top in SVG coords). Width = `(n_points - 1) × 10`. For a secondary (non-accent) metric, use `stroke="var(--accent-2)"`. For a negative trend, use `stroke="var(--text-dim)"`.

## Proactive Imagery

Slides should reach for visuals before defaulting to text alone. If a slide could be more compelling with an image, chart, or diagram, add one.

**surf-cli integration:** Check `which surf` at the start of every slide deck generation. If available, **generate 2–4 images minimum** for any deck over 10 slides. This is not optional when surf is available — a deck with AI-generated imagery is dramatically more compelling than one with only CSS gradients. Target these slides in priority order:

1. **Title slide** (always): background image that sets the deck's visual tone. Match the topic and palette. Use `--aspect-ratio 16:9`. Prompt example: "abstract dark geometric pattern with green accent lines, technical and minimal" for Terminal Mono preset.
2. **Full-bleed slide** (always if deck has one): immersive background for the deck's visual anchor moment. Style should match the preset — photo-realistic for Midnight Editorial, abstract/geometric for Swiss Clean, circuit-board or terminal aesthetic for Terminal Mono.
3. **Content slides with conceptual topics** (1–2 if the deck has room): illustration in the `.slide__aside` area for slides about abstract concepts. Use `--aspect-ratio 1:1`.

**Generate images before writing HTML** so they're ready to embed. The workflow:

```bash
# Check availability
which surf

# Generate (one per target slide)
surf gemini "descriptive prompt matching deck palette" --generate-image /tmp/ve-slide-title.png --aspect-ratio 16:9

# Base64 encode for self-containment (macOS)
TITLE_IMG=$(base64 -i /tmp/ve-slide-title.png)
# Linux: TITLE_IMG=$(base64 -w 0 /tmp/ve-slide-title.png)

# Embed in the slide
# <div class="slide__bg" style="background-image:url('data:image/png;base64,${TITLE_IMG}')"></div>

# Clean up
rm /tmp/ve-slide-title.png
```

**Prompt craft for slides:** Be specific about style, dominant colors, and mood. Pull colors from the preset's CSS variables. Examples:

- Terminal Mono: "dark abstract circuit board pattern, green (#50fa7b) traces on near-black (#0a0e14), minimal, technical"
- Midnight Editorial: "deep navy abstract composition, warm gold accent light, cinematic depth of field, premium editorial feel"
- Warm Signal: "warm cream textured paper with terracotta geometric accents, confident modern design"

**When surf fails or isn't available:** Degrade gracefully to CSS gradients and SVG decorations. Use the `.slide__bg--gradient` pattern with bold `linear-gradient` or `radial-gradient` backgrounds. The deck should stand on its own visually without generated images — they enhance, they don't carry. Note the fallback in an HTML comment (`<!-- surf unavailable, using CSS gradient fallback -->`) so future edits know to retry.

**Inline data visualizations:** Proactively add SVG sparklines next to numbers, mini-charts on dashboard slides, and small Mermaid diagrams on split slides even when not explicitly requested. A number with a sparkline next to it tells a better story than a number alone.

**When to skip images:** If surf isn't available, degrade gracefully — use CSS gradients and SVG decorations instead. Never error on missing surf. Pure structural or data-heavy decks (code reviews, table comparisons) may not need generated images.

## Compositional Variety

Consecutive slides must vary their spatial approach. Three centered slides in a row means push one off-axis.

**Composition patterns to alternate between:**

- Centered (title slides, quotes)
- Left-heavy: content on the left 60%, breathing room on the right
- Right-heavy: content on the right 60%, visual or whitespace on the left
- Edge-aligned: content pushed to bottom or top, large empty space opposite
- Split: two distinct panels filling the viewport
- Full-bleed: background dominates, minimal overlaid text

The agent should plan the slide sequence considering layout rhythm, not just content order. When outlining a deck, assign a composition to each slide before writing HTML.

## Presentation Readability

Slides get projected, screen-shared, viewed at distance. Design accordingly:

- **Minimum body text: 16px.** Nothing smaller except labels and captions.
- **One focal point per slide.** Not three competing elements.
- **Higher contrast than pages.** Dimmed text (`--text-dim`) should still be easily readable at distance — test against the background.
- **Nav chrome opacity.** Dots and progress bar must be visible on any slide background (light or dark) without being distracting. Use the backdrop blur or text-shadow approach from the Nav Chrome section.
- **Simpler Mermaid diagrams.** Max 8–10 nodes, 18px+ labels, 2px+ edges. The diagram should be readable without zoom at presentation distance. Zoom controls remain available for detail inspection.

## Content Density Limits

Each slide must fit in exactly 100dvh. If content exceeds these limits, the agent splits across multiple slides — never scrolls within a slide.

| Slide type      | Max content                                                                                                       |
| --------------- | ----------------------------------------------------------------------------------------------------------------- |
| Title           | 1 heading + 1 subtitle                                                                                            |
| Section Divider | 1 number + 1 heading + optional subhead                                                                           |
| Content         | 1 heading + 5–6 bullets (max 2 lines each)                                                                        |
| Split           | 1 heading + 2 panels, each follows its inner type's limits                                                        |
| Diagram         | 1 heading + 1 Mermaid diagram (max 8–10 nodes)                                                                    |
| Dashboard       | 1 heading + 6 KPI cards. Hero values ≤6 chars (numbers, %, short labels). Longer strings belong in the label row. |
| Table           | 1 heading + 8 rows; overflow paginates to next slide                                                              |
| Code            | 1 heading + 10 lines of code                                                                                      |
| Quote           | 1 short quote (~25 words / ~150 chars max) + 1 attribution. Longer quotes are content slides, not quote slides.   |
| Full-Bleed      | 1 heading + 1 subtitle over background                                                                            |
| Timeline        | 1 heading + 4–6 milestones (date + title + 1-line desc each)                                                      |
| Comparison      | 1 heading + 2 column labels, 5–7 comparison rows                                                                  |
| Process Steps   | 1 heading + 4–5 steps (title + 2-line desc + optional badge each)                                                 |

## Responsive Height Breakpoints

Height-based scaling is more critical for slides than width. Each breakpoint progressively reduces padding, font sizes, and hides decorative elements.

```css
/* Compact viewports */
@media (max-height: 700px) {
    .slide {
        padding: clamp(24px, 4vh, 40px) clamp(32px, 6vw, 80px);
    }
    .slide__display {
        font-size: clamp(36px, 8vw, 72px);
    }
    .slide--divider .slide__number {
        font-size: clamp(80px, 16vw, 160px);
    }
}

/* Small tablets / landscape phones */
@media (max-height: 600px) {
    .slide__decor {
        display: none;
    } /* hide decorative SVGs */
    .slide--quote {
        padding: clamp(32px, 6vh, 60px) clamp(40px, 8vw, 100px);
    }
    .slide__quote-mark {
        display: none;
    }
}

/* Aggressive: landscape phones */
@media (max-height: 500px) {
    .slide {
        padding: clamp(16px, 3vh, 24px) clamp(24px, 5vw, 48px);
    }
    .deck-dots {
        display: none;
    } /* dots clutter tiny viewports */
    .slide__display {
        font-size: clamp(28px, 7vw, 48px);
    }
}

/* Width breakpoint for grids */
@media (max-width: 768px) {
    .slide--content .slide__inner {
        grid-template-columns: 1fr;
    }
    .slide--content .slide__aside {
        display: none;
    }
    .slide--split .slide__panels {
        grid-template-columns: 1fr;
    }
    .slide--dashboard .slide__kpis {
        grid-template-columns: repeat(2, 1fr);
    }
}
```

## Curated Presets

Starting points the agent can riff on. Each defines a font pairing, palette, and background treatment. The agent adapts these to the content — different decks with the same preset should still feel distinct.

### Midnight Editorial

Deep navy, serif display, warm gold accents. Cinematic, premium. Dark-first.

```css
:root {
    --font-body: "Instrument Serif", Georgia, serif;
    --font-mono: "JetBrains Mono", "SF Mono", monospace;
    --bg: #0f1729;
    --surface: #162040;
    --surface2: #1d2b52;
    --surface-elevated: #243362;
    --border: rgba(200, 180, 140, 0.08);
    --border-bright: rgba(200, 180, 140, 0.16);
    --text: #e8e4d8;
    --text-dim: #9a9484;
    --accent: #d4a73a;
    --accent-dim: rgba(212, 167, 58, 0.1);
    --code-bg: #0a0f1e;
    --code-text: #d4d0c4;
}
@media (prefers-color-scheme: light) {
    :root {
        --bg: #faf8f2;
        --surface: #ffffff;
        --surface2: #f5f0e6;
        --surface-elevated: #fffdf5;
        --border: rgba(30, 30, 50, 0.08);
        --border-bright: rgba(30, 30, 50, 0.16);
        --text: #1a1814;
        --text-dim: #7a7468;
        --accent: #b8860b;
        --accent-dim: rgba(184, 134, 11, 0.08);
        --code-bg: #2a2520;
        --code-text: #e8e4d8;
    }
}
```

Background: radial gold glow at top center. Decorative corner marks in gold. Title slides use dramatic serif at max scale.

### Warm Signal

Cream paper, bold sans, terracotta/coral accents. Confident and modern. Light-first.

```css
:root {
    --font-body: "Plus Jakarta Sans", system-ui, sans-serif;
    --font-mono: "Azeret Mono", "SF Mono", monospace;
    --bg: #faf6f0;
    --surface: #ffffff;
    --surface2: #f5ece0;
    --surface-elevated: #fffdf5;
    --border: rgba(60, 40, 20, 0.08);
    --border-bright: rgba(60, 40, 20, 0.16);
    --text: #2c2a25;
    --text-dim: #7c756a;
    --accent: #c2410c;
    --accent-dim: rgba(194, 65, 12, 0.08);
    --code-bg: #2c2520;
    --code-text: #f5ece0;
}
@media (prefers-color-scheme: dark) {
    :root {
        --bg: #1c1916;
        --surface: #262220;
        --surface2: #302b28;
        --surface-elevated: #3a3430;
        --border: rgba(200, 180, 160, 0.08);
        --border-bright: rgba(200, 180, 160, 0.16);
        --text: #f0e8dc;
        --text-dim: #a09888;
        --accent: #e85d2a;
        --accent-dim: rgba(232, 93, 42, 0.1);
        --code-bg: #141210;
        --code-text: #f0e8dc;
    }
}
```

Background: warm radial glow at bottom left. Terracotta accent borders on cards. Section divider numbers in ultra-light coral.

### Terminal Mono

Dark, monospace everything, green/cyan accents, faint grid. Developer-native. Dark-first.

```css
:root {
    --font-body: "Geist Mono", "SF Mono", Consolas, monospace;
    --font-mono: "Geist Mono", "SF Mono", Consolas, monospace;
    --bg: #0a0e14;
    --surface: #12161e;
    --surface2: #1a1f2a;
    --surface-elevated: #222836;
    --border: rgba(80, 250, 123, 0.06);
    --border-bright: rgba(80, 250, 123, 0.12);
    --text: #c8d6e5;
    --text-dim: #5a6a7a;
    --accent: #50fa7b;
    --accent-dim: rgba(80, 250, 123, 0.08);
    --code-bg: #060a10;
    --code-text: #c8d6e5;
}
@media (prefers-color-scheme: light) {
    :root {
        --bg: #f4f6f8;
        --surface: #ffffff;
        --surface2: #eaecf0;
        --surface-elevated: #f8f9fa;
        --border: rgba(0, 80, 40, 0.08);
        --border-bright: rgba(0, 80, 40, 0.16);
        --text: #1a2332;
        --text-dim: #5a6a7a;
        --accent: #0d7a3e;
        --accent-dim: rgba(13, 122, 62, 0.08);
        --code-bg: #1a2332;
        --code-text: #c8d6e5;
    }
}
```

Background: faint dot grid. Everything in mono. Title slides use large weight-400 mono instead of bold display. Code slides feel native.

### Swiss Clean

White, geometric sans, single bold accent, visible grid. Minimal and precise. Light-first.

```css
:root {
    --font-body: "DM Sans", system-ui, sans-serif;
    --font-mono: "Fira Code", "SF Mono", monospace;
    --bg: #ffffff;
    --surface: #f8f8f8;
    --surface2: #f0f0f0;
    --surface-elevated: #ffffff;
    --border: rgba(0, 0, 0, 0.08);
    --border-bright: rgba(0, 0, 0, 0.16);
    --text: #111111;
    --text-dim: #666666;
    --accent: #0055ff;
    --accent-dim: rgba(0, 85, 255, 0.06);
    --code-bg: #18181b;
    --code-text: #e4e4e7;
}
@media (prefers-color-scheme: dark) {
    :root {
        --bg: #111111;
        --surface: #1a1a1a;
        --surface2: #222222;
        --surface-elevated: #2a2a2a;
        --border: rgba(255, 255, 255, 0.08);
        --border-bright: rgba(255, 255, 255, 0.16);
        --text: #f0f0f0;
        --text-dim: #888888;
        --accent: #3b82f6;
        --accent-dim: rgba(59, 130, 246, 0.08);
        --code-bg: #0a0a0a;
        --code-text: #e4e4e7;
    }
}
```

Background: clean white or near-black, no gradients. Visible grid lines (the `--with-grid` pattern). Tight geometric layouts. Single accent color used sparingly for emphasis. Data-heavy and analytical content shines here.

### Velvet Editorial

Deep wine, rose gold accents, serif display. Luxury print aesthetic — Monocle, Kinfolk, high-end annual report. Dark-first.

```css
:root {
    --font-body: "Cormorant Garamond", "Georgia", serif;
    --font-mono: "Fira Code", "SF Mono", monospace;
    --bg: #160810;
    --surface: #211020;
    --surface2: #2c1530;
    --surface-elevated: #371a3c;
    --border: rgba(200, 148, 108, 0.08);
    --border-bright: rgba(200, 148, 108, 0.18);
    --text: #f0e6ea;
    --text-dim: #9a7585;
    --accent: #c9956c;
    --accent-dim: rgba(201, 149, 108, 0.1);
    --accent-2: #e8c4b0;
    --code-bg: #0e0508;
    --code-text: #e8d4dc;
}
@media (prefers-color-scheme: light) {
    :root {
        --bg: #fdf8f5;
        --surface: #ffffff;
        --surface2: #f7ede8;
        --surface-elevated: #fffbf9;
        --border: rgba(80, 30, 50, 0.08);
        --border-bright: rgba(80, 30, 50, 0.16);
        --text: #1a0810;
        --text-dim: #7a5060;
        --accent: #a0623a;
        --accent-dim: rgba(160, 98, 58, 0.08);
        --accent-2: #6e3050;
        --code-bg: #1a0810;
        --code-text: #f0e6ea;
    }
}
```

Background: deep radial glow in wine/burgundy at bottom-right, almost invisible but warm. Title slides use Cormorant Garamond at max display scale — the extreme width contrast (700 weight vs 200) is the visual signature. Section dividers show the rose gold accent number floating like print page numbers. Avoid hard grid lines — spacing alone creates structure.

### Bauhaus Constructivist

White foundation, primary color blocks (red, black, yellow), geometric sans at maximum weight. Functional, bold, zero ornament. Light-first.

```css
:root {
    --font-body: "Space Grotesk", system-ui, sans-serif;
    --font-mono: "Space Mono", "SF Mono", monospace;
    --bg: #f5f4ef;
    --surface: #ffffff;
    --surface2: #ebebe4;
    --surface-elevated: #ffffff;
    --border: rgba(0, 0, 0, 0.12);
    --border-bright: rgba(0, 0, 0, 0.25);
    --text: #111111;
    --text-dim: #555555;
    --accent: #d62828;
    --accent-dim: rgba(214, 40, 40, 0.08);
    --accent-2: #f7b731;
    --code-bg: #111111;
    --code-text: #f5f4ef;
}
@media (prefers-color-scheme: dark) {
    :root {
        --bg: #111111;
        --surface: #1a1a1a;
        --surface2: #222222;
        --surface-elevated: #2a2a2a;
        --border: rgba(255, 255, 255, 0.1);
        --border-bright: rgba(255, 255, 255, 0.22);
        --text: #f5f4ef;
        --text-dim: #999999;
        --accent: #e63946;
        --accent-dim: rgba(230, 57, 70, 0.1);
        --accent-2: #f7b731;
        --code-bg: #0a0a0a;
        --code-text: #f5f4ef;
    }
}
```

Background: solid white or black — no gradients, no glow, no texture. Structure comes from color blocks and thick borders, not lighting effects. Title slides use `--accent` (red) as a full-bleed left panel (20–30% width) with white heading on the right — hard geometric split, not a gradient. Section dividers use `--accent-2` (yellow) as a full-width horizontal stripe. The `--with-grid` pattern is replaced with 4px solid horizontal rules between major sections. Use `--accent-2` sparingly for highlighting secondary information; never both accents on the same element.

### Fog Minimalist

Sand/mist neutrals, zero decoration, hairlines only, maximum breathing room. Japanese editorial sensibility. Light-first.

```css
:root {
    --font-body: "Source Serif 4", "Georgia", serif;
    --font-mono: "Noto Sans Mono", "SF Mono", monospace;
    --bg: #f5f0eb;
    --surface: #faf8f5;
    --surface2: #ede8e3;
    --surface-elevated: #fdfcfa;
    --border: rgba(44, 38, 32, 0.08);
    --border-bright: rgba(44, 38, 32, 0.14);
    --text: #2c2620;
    --text-dim: #8c8078;
    --accent: #7a8c7e;
    --accent-dim: rgba(122, 140, 126, 0.1);
    --code-bg: #1e1c18;
    --code-text: #e8e4de;
}
@media (prefers-color-scheme: dark) {
    :root {
        --bg: #1a1714;
        --surface: #211f1b;
        --surface2: #2a2822;
        --surface-elevated: #32302a;
        --border: rgba(200, 190, 175, 0.08);
        --border-bright: rgba(200, 190, 175, 0.14);
        --text: #e8e0d5;
        --text-dim: #8a8278;
        --accent: #a0b5a4;
        --accent-dim: rgba(160, 181, 164, 0.1);
        --code-bg: #111009;
        --code-text: #ddd8d0;
    }
}
```

Background: warm sand or deep charcoal — never pure white or black. Zero gradients, zero glow, zero decorative SVGs on content slides. Structure is spacing alone: extra-generous padding (`clamp(60px, 10vh, 120px)` vertical), thin 1px borders instead of surfaces, wide margins. Title slides use a single centered heading at modest scale (48–64px max) with a long horizontal hairline below. Section dividers use only a number and heading — no oversized ghost number, no accent marks. The restraint is the design. Reserve the accent (`--accent` sage) for a single element per slide: a bullet color, a thin left border on a quote, a label — never a background.

### ELO Blue

Deep navy, ELO brand cyan electric, platform-precision typography. Colors extracted directly from the ELO logo: sphere navy `#053574`, cyan highlight `#0db2ef`, white wordmark. Built for ELO Consulting's ServiceNow presentations: client pitches, technical architectures, pre-sales cadrage, and project reviews. Dark-first.

```css
:root {
    --font-body: "Bricolage Grotesque", system-ui, sans-serif;
    --font-mono: "IBM Plex Mono", "SF Mono", monospace;
    --bg: #020c1e;
    --surface: #051828;
    --surface2: #091f36;
    --surface-elevated: #0d2544;
    --border: rgba(13, 178, 239, 0.08);
    --border-bright: rgba(13, 178, 239, 0.18);
    --text: #e0eaf8;
    --text-dim: #4d7aaa;
    --accent: #0db2ef; /* ELO cyan — sphere highlight */
    --accent-dim: rgba(13, 178, 239, 0.1);
    --accent-2: #4fc8f4; /* lighter cyan for secondary emphasis */
    --code-bg: #020a16;
    --code-text: #c0d8f0;
}
@media (prefers-color-scheme: light) {
    :root {
        --bg: #f2f7ff;
        --surface: #ffffff;
        --surface2: #e4eef8;
        --surface-elevated: #f8fbff;
        --border: rgba(5, 53, 116, 0.08);
        --border-bright: rgba(5, 53, 116, 0.18);
        --text: #030d1e;
        --text-dim: #3d5a8a;
        --accent: #053574; /* ELO navy — sphere body, readable on white */
        --accent-dim: rgba(5, 53, 116, 0.07);
        --accent-2: #0d90c8; /* mid cyan for secondary use on light bg */
        --code-bg: #030d1e;
        --code-text: #c0d8f0;
    }
}
```

Background: very deep navy `#020c1e` with a tight directional beam at top-left in the ELO cyan (`background: linear-gradient(135deg, rgba(13,178,239,0.12) 0%, transparent 38%)`). Title slides use a 3px cyan border rule at top, the large display text in white, and a ghost "ELO" monogram in `--border-bright` at mega scale (opacity 0.05) as a watermark behind the headline. Section dividers replace the oversized ghost number with a thin horizontal rule in `--accent` + a small filled circle — closer to the ELO sphere motif. KPI cards get a left border in `--accent` (primary metric) or `--accent-2` (secondary). The `--with-grid` dot pattern reads as technical platform feel consistent with the ServiceNow UI aesthetic. Avoid decorative gradients or warm glows — ELO Blue is precise, not atmospheric.

**Usage note:** This preset is purpose-built for ELO Consulting deliverables. The keywords `ELO`, `ELO Blue`, or `pour ELO` in the user prompt should trigger this preset as the default. Title slides may include the ELO logotype as an `<img>` reference. Avoid Velvet Editorial or Bauhaus in an ELO client context.

### ELO Light

White foundation, ELO navy `#053574` as primary accent, ELO yellow `#F5E400` as secondary highlight, ELO cyan `#0db2ef` as tertiary. Same brand, opposite luminosity to ELO Blue. Use when presenting in bright meeting rooms, for printed decks, or when the client context calls for a cleaner, more accessible look. Light-first.

```css
:root {
    --font-body: "Bricolage Grotesque", system-ui, sans-serif;
    --font-mono: "IBM Plex Mono", "SF Mono", monospace;
    --bg: #f6f9ff;
    --surface: #ffffff;
    --surface2: #edf2fc;
    --surface-elevated: #ffffff;
    --border: rgba(5, 53, 116, 0.08);
    --border-bright: rgba(5, 53, 116, 0.16);
    --text: #030d1e;
    --text-dim: #3d5a8a;
    --accent: #053574; /* ELO navy — sphere body */
    --accent-dim: rgba(5, 53, 116, 0.07);
    --accent-2: #f5e400; /* ELO yellow — logo sphere accent */
    --code-bg: #030d1e;
    --code-text: #c0d8f0;
}
@media (prefers-color-scheme: dark) {
    :root {
        --bg: #020c1e;
        --surface: #051828;
        --surface2: #091f36;
        --surface-elevated: #0d2544;
        --border: rgba(13, 178, 239, 0.08);
        --border-bright: rgba(13, 178, 239, 0.18);
        --text: #e0eaf8;
        --text-dim: #4d7aaa;
        --accent: #0db2ef; /* ELO cyan — visible on dark */
        --accent-dim: rgba(13, 178, 239, 0.1);
        --accent-2: #f5e400; /* yellow unchanged — works on dark too */
        --code-bg: #020a16;
        --code-text: #c0d8f0;
    }
}
```

Background: clean white or very light blue-tinted white `#f6f9ff` — no gradients, no glow. Structure comes from `--accent` (navy) borders and text, not from lighting. Title slides use a full-width 4px navy top border (the ELO sphere blue at full opacity) + the display heading in `#030d1e` at max weight. Section dividers use a thin navy horizontal rule with a small filled cyan dot (`#0db2ef`) — the sphere motif in miniature. The yellow `--accent-2` is reserved for high-emphasis badges, alert-like KPI values, and CTA borders — used sparingly (one element per slide maximum) as it reads as urgency or importance on a light background. The `--with-grid` dot pattern is appropriate. Code slides use the dark `--code-bg` creating a strong contrast inset against the white surface.

**Pairing note:** ELO Light and ELO Blue are complementary variants — switching between them in the Design System Switcher lets you compare presentation styles for the same deck content. The same fonts (Bricolage Grotesque + IBM Plex Mono) and `--accent-2` yellow are shared between both presets, maintaining brand consistency across modes.

## Design System Switcher

A floating button (bottom-left) that opens a compact panel listing all 8 presets with color swatches. Clicking a preset applies its CSS variables to `:root` instantly via `element.style.setProperty`. Include in every generated deck by default — it adds negligible weight and makes demos and pre-sales presentations far more useful.

**Positioning:** Bottom-left, does not conflict with existing chrome (progress bar top, nav dots right, counter bottom-right, hints bottom-center).

**Copy this complete block into any deck, before `</body>`:**

```html
<!-- Design System Switcher — paste before </body> -->
<div id="ds-switcher">
    <div id="ds-panel" role="dialog" aria-label="Design system">
        <div class="ds-panel-title">Design System</div>
        <div class="ds-grid" id="ds-grid"></div>
    </div>
    <button id="ds-btn" title="Changer de design system" aria-expanded="false">
        <!-- Palette icon: 4 colored dots -->
        <svg viewBox="0 0 20 20" width="18" height="18" fill="none">
            <circle cx="5" cy="5" r="3" fill="var(--accent)" />
            <circle cx="15" cy="5" r="3" fill="var(--accent-2, var(--text-dim))" />
            <circle cx="5" cy="15" r="3" fill="var(--text-dim)" />
            <circle cx="15" cy="15" r="3" fill="var(--surface-elevated)" />
        </svg>
    </button>
</div>
```

```css
/* Switcher chrome — add to your <style> block */
#ds-switcher {
    position: fixed;
    bottom: clamp(12px, 2vh, 20px);
    left: clamp(12px, 2vw, 22px);
    z-index: 500;
    font-family: system-ui, sans-serif;
}
#ds-btn {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--surface-elevated);
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.35);
    transition:
        transform 0.2s ease,
        background 0.4s ease;
}
#ds-btn:hover {
    transform: scale(1.08);
}
#ds-panel {
    position: absolute;
    bottom: 52px;
    left: 0;
    width: 320px;
    background: var(--surface-elevated);
    border: 1px solid var(--border-bright);
    border-radius: 14px;
    padding: 14px;
    box-shadow: 0 8px 40px rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    opacity: 0;
    transform: translateY(10px) scale(0.96);
    pointer-events: none;
    transition:
        opacity 0.22s ease,
        transform 0.22s cubic-bezier(0.16, 1, 0.3, 1);
}
#ds-panel.open {
    opacity: 1;
    transform: none;
    pointer-events: all;
}
.ds-panel-title {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--text-dim);
    margin-bottom: 10px;
    font-family: var(--font-mono);
}
.ds-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 7px;
}
.ds-preset-btn {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 9px;
    padding: 9px 10px;
    cursor: pointer;
    text-align: left;
    transition:
        border-color 0.15s ease,
        background 0.15s ease,
        transform 0.12s ease;
    position: relative;
}
.ds-preset-btn:hover {
    border-color: var(--border-bright);
    transform: translateY(-1px);
}
.ds-preset-btn.active {
    border-color: var(--accent) !important;
    background: var(--accent-dim) !important;
}
.ds-preset-btn.active::after {
    content: "✓";
    position: absolute;
    top: 6px;
    right: 8px;
    font-size: 10px;
    color: var(--accent);
    font-weight: 700;
}
.ds-preset-name {
    font-size: 11px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 6px;
}
.ds-swatches {
    display: flex;
    gap: 4px;
}
.ds-swatch {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    flex-shrink: 0;
    border: 1px solid rgba(255, 255, 255, 0.1);
}
```

```javascript
/* Preset definitions — keep in sync with slide-patterns.md */
const PRESETS = [
    {
        id: "midnight-editorial",
        name: "Midnight Editorial",
        swatches: ["#0f1729", "#d4a73a", "#e8e4d8", "#162040"],
        vars: {
            "--font-body": "'Instrument Serif', Georgia, serif",
            "--font-mono": "'JetBrains Mono','SF Mono',monospace",
            "--bg": "#0f1729",
            "--surface": "#162040",
            "--surface2": "#1d2b52",
            "--surface-elevated": "#243362",
            "--border": "rgba(200,180,140,0.08)",
            "--border-bright": "rgba(200,180,140,0.16)",
            "--text": "#e8e4d8",
            "--text-dim": "#9a9484",
            "--accent": "#d4a73a",
            "--accent-dim": "rgba(212,167,58,0.1)",
            "--accent-2": "#e8c9a0",
            "--code-bg": "#0a0f1e",
            "--code-text": "#d4d0c4",
        },
    },
    {
        id: "warm-signal",
        name: "Warm Signal",
        swatches: ["#faf6f0", "#c2410c", "#2c2a25", "#ffffff"],
        vars: {
            "--font-body": "'Plus Jakarta Sans',system-ui,sans-serif",
            "--font-mono": "'Azeret Mono','SF Mono',monospace",
            "--bg": "#faf6f0",
            "--surface": "#ffffff",
            "--surface2": "#f5ece0",
            "--surface-elevated": "#fffdf5",
            "--border": "rgba(60,40,20,0.08)",
            "--border-bright": "rgba(60,40,20,0.16)",
            "--text": "#2c2a25",
            "--text-dim": "#7c756a",
            "--accent": "#c2410c",
            "--accent-dim": "rgba(194,65,12,0.08)",
            "--accent-2": "#e07b3a",
            "--code-bg": "#2c2520",
            "--code-text": "#f5ece0",
        },
    },
    {
        id: "terminal-mono",
        name: "Terminal Mono",
        swatches: ["#0a0e14", "#50fa7b", "#c8d6e5", "#12161e"],
        vars: {
            "--font-body": "'Geist Mono','SF Mono',Consolas,monospace",
            "--font-mono": "'Geist Mono','SF Mono',Consolas,monospace",
            "--bg": "#0a0e14",
            "--surface": "#12161e",
            "--surface2": "#1a1f2a",
            "--surface-elevated": "#222836",
            "--border": "rgba(80,250,123,0.06)",
            "--border-bright": "rgba(80,250,123,0.12)",
            "--text": "#c8d6e5",
            "--text-dim": "#5a6a7a",
            "--accent": "#50fa7b",
            "--accent-dim": "rgba(80,250,123,0.08)",
            "--accent-2": "#8be9fd",
            "--code-bg": "#060a10",
            "--code-text": "#c8d6e5",
        },
    },
    {
        id: "swiss-clean",
        name: "Swiss Clean",
        swatches: ["#ffffff", "#0055ff", "#111111", "#f8f8f8"],
        vars: {
            "--font-body": "'DM Sans',system-ui,sans-serif",
            "--font-mono": "'Fira Code','SF Mono',monospace",
            "--bg": "#ffffff",
            "--surface": "#f8f8f8",
            "--surface2": "#f0f0f0",
            "--surface-elevated": "#ffffff",
            "--border": "rgba(0,0,0,0.08)",
            "--border-bright": "rgba(0,0,0,0.16)",
            "--text": "#111111",
            "--text-dim": "#666666",
            "--accent": "#0055ff",
            "--accent-dim": "rgba(0,85,255,0.06)",
            "--accent-2": "#0099ff",
            "--code-bg": "#18181b",
            "--code-text": "#e4e4e7",
        },
    },
    {
        id: "velvet-editorial",
        name: "Velvet Editorial",
        swatches: ["#160810", "#c9956c", "#f0e6ea", "#211020"],
        vars: {
            "--font-body": "'Cormorant Garamond',Georgia,serif",
            "--font-mono": "'Fira Code','SF Mono',monospace",
            "--bg": "#160810",
            "--surface": "#211020",
            "--surface2": "#2c1530",
            "--surface-elevated": "#371a3c",
            "--border": "rgba(200,148,108,0.08)",
            "--border-bright": "rgba(200,148,108,0.18)",
            "--text": "#f0e6ea",
            "--text-dim": "#9a7585",
            "--accent": "#c9956c",
            "--accent-dim": "rgba(201,149,108,0.1)",
            "--accent-2": "#e8c4b0",
            "--code-bg": "#0e0508",
            "--code-text": "#e8d4dc",
        },
    },
    {
        id: "bauhaus",
        name: "Bauhaus",
        swatches: ["#f5f4ef", "#d62828", "#111111", "#ffffff"],
        vars: {
            "--font-body": "'Space Grotesk',system-ui,sans-serif",
            "--font-mono": "'Space Mono','SF Mono',monospace",
            "--bg": "#f5f4ef",
            "--surface": "#ffffff",
            "--surface2": "#ebebE4",
            "--surface-elevated": "#ffffff",
            "--border": "rgba(0,0,0,0.12)",
            "--border-bright": "rgba(0,0,0,0.25)",
            "--text": "#111111",
            "--text-dim": "#555555",
            "--accent": "#d62828",
            "--accent-dim": "rgba(214,40,40,0.08)",
            "--accent-2": "#f7b731",
            "--code-bg": "#111111",
            "--code-text": "#f5f4ef",
        },
    },
    {
        id: "fog-minimalist",
        name: "Fog Minimalist",
        swatches: ["#f5f0eb", "#7a8c7e", "#2c2620", "#faf8f5"],
        vars: {
            "--font-body": "'Source Serif 4',Georgia,serif",
            "--font-mono": "'Noto Sans Mono','SF Mono',monospace",
            "--bg": "#f5f0eb",
            "--surface": "#faf8f5",
            "--surface2": "#ede8e3",
            "--surface-elevated": "#fdfcfa",
            "--border": "rgba(44,38,32,0.08)",
            "--border-bright": "rgba(44,38,32,0.14)",
            "--text": "#2c2620",
            "--text-dim": "#8c8078",
            "--accent": "#7a8c7e",
            "--accent-dim": "rgba(122,140,126,0.1)",
            "--accent-2": "#a0b5a4",
            "--code-bg": "#1e1c18",
            "--code-text": "#e8e4de",
        },
    },
    {
        id: "elo-blue",
        name: "ELO Blue",
        swatches: ["#020c1e", "#0db2ef", "#e0eaf8", "#051828"],
        vars: {
            "--font-body": "'Bricolage Grotesque',system-ui,sans-serif",
            "--font-mono": "'IBM Plex Mono','SF Mono',monospace",
            "--bg": "#020c1e",
            "--surface": "#051828",
            "--surface2": "#091f36",
            "--surface-elevated": "#0d2544",
            "--border": "rgba(13,178,239,0.08)",
            "--border-bright": "rgba(13,178,239,0.18)",
            "--text": "#e0eaf8",
            "--text-dim": "#4d7aaa",
            "--accent": "#0db2ef",
            "--accent-dim": "rgba(13,178,239,0.10)",
            "--accent-2": "#f5e400",
            "--code-bg": "#020a16",
            "--code-text": "#c0d8f0",
        },
    },
    {
        id: "elo-light",
        name: "ELO Light",
        swatches: ["#f6f9ff", "#053574", "#030d1e", "#f5e400"],
        vars: {
            "--font-body": "'Bricolage Grotesque',system-ui,sans-serif",
            "--font-mono": "'IBM Plex Mono','SF Mono',monospace",
            "--bg": "#f6f9ff",
            "--surface": "#ffffff",
            "--surface2": "#edf2fc",
            "--surface-elevated": "#ffffff",
            "--border": "rgba(5,53,116,0.08)",
            "--border-bright": "rgba(5,53,116,0.16)",
            "--text": "#030d1e",
            "--text-dim": "#3d5a8a",
            "--accent": "#053574",
            "--accent-dim": "rgba(5,53,116,0.07)",
            "--accent-2": "#f5e400",
            "--code-bg": "#030d1e",
            "--code-text": "#c0d8f0",
        },
    },
];

function applyPreset(id) {
    const p = PRESETS.find((x) => x.id === id);
    if (!p) return;
    const root = document.documentElement;
    Object.entries(p.vars).forEach(([k, v]) => root.style.setProperty(k, v));
    document.querySelectorAll(".ds-preset-btn").forEach((b) => {
        b.classList.toggle("active", b.dataset.id === id);
    });
    try {
        sessionStorage.setItem("ds-preset", id);
    } catch (e) {}
}

// Build grid
const grid = document.getElementById("ds-grid");
PRESETS.forEach((p) => {
    const btn = document.createElement("button");
    btn.className = "ds-preset-btn";
    btn.dataset.id = p.id;
    btn.innerHTML = `
    <div class="ds-preset-name">${p.name}</div>
    <div class="ds-swatches">${p.swatches.map((c) => `<span class="ds-swatch" style="background:${c}"></span>`).join("")}</div>`;
    btn.addEventListener("click", () => applyPreset(p.id));
    grid.appendChild(btn);
});

// Toggle
const dsBtn = document.getElementById("ds-btn");
const dsPanel = document.getElementById("ds-panel");
let open = false;
dsBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    open = !open;
    dsPanel.classList.toggle("open", open);
    dsBtn.setAttribute("aria-expanded", open);
});
document.addEventListener("click", (e) => {
    if (!document.getElementById("ds-switcher").contains(e.target)) {
        open = false;
        dsPanel.classList.remove("open");
        dsBtn.setAttribute("aria-expanded", "false");
    }
});
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && open) {
        open = false;
        dsPanel.classList.remove("open");
        dsBtn.setAttribute("aria-expanded", "false");
    }
});

// Restore or default
try {
    applyPreset(sessionStorage.getItem("ds-preset") || "elo-blue");
} catch (e) {
    applyPreset("elo-blue");
}
```

**Integration notes:**

- The entire block is self-contained. Paste it as-is before `</body>` in any generated deck.
- Google Fonts for all 8 presets must be preloaded in `<head>` for instant font switching. Add all families to a single `<link>` tag (see the demo file for the full import string).
- The switcher defaults to `'elo-blue'` — change the fallback string to any preset `id` to change the default.
- `sessionStorage` persists the choice across page reloads within the same browser tab.
- **When to include:** Always include in ELO pre-sales and pitch decks. Optionally omit for final deliverables sent to clients where switching is not needed.
