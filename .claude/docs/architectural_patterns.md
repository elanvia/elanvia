# Architectural Patterns

Patterns that appear in multiple files. Follow these when extending the site so new code stays consistent with what's already there.

## 1. Section-header trio

Every content section (II–V) opens with the same three-element header: roman numeral, italic serif title, cursive script subtitle. The class names and order are identical so the CSS in `assets/css/main.css` (`.section-header`, `.section-roman`, `.section-title`, `.section-script`) styles them uniformly.

Examples:
- `layouts/partials/section-about.html:2-6`
- `layouts/partials/section-offer.html:2-6`
- `layouts/partials/section-booking.html:2-6`
- `layouts/partials/section-contact.html:2-6`

When adding a new section, copy this trio verbatim and only change the roman numeral and text.

## 2. Accent-color theming via BEM modifier classes

Cards reuse a single base class plus a `--<accent>` modifier that flips a `--accent-color` CSS custom property. The base style consumes `var(--accent-color, var(--plum))` so any color-aware element (border, top-bar, price) follows automatically.

- Base + modifiers: `assets/css/main.css:407-410` (`.offer__card--{sage,plum,rose,saffron}`)
- Modifier consumed: `assets/css/main.css:413, 422, 466` (roman, tagline, price)
- Modifier applied from data: `layouts/partials/section-offer.html:9` (`offer__card--{{ $s.accent }}`)
- Accent value source: `data/services.yaml` (`accent:` field per service)

When adding a 5th service variant, add `--<name>` block in CSS next to the others and set `accent: <name>` in YAML — no other change needed.

## 3. Inline SVG via `resources.Get | safeHTML`

Decorative SVGs are embedded inline (not `<img>`) so CSS can target their internals and so `currentColor` works for icon recoloring on hover. Pattern is identical across files:

```go
{{ $x := resources.Get "svg/<file>.svg" }}
{{ $x.Content | safeHTML }}
```

Examples:
- `layouts/partials/section-hero.html:21-22` (rainbow wash)
- `layouts/partials/section-about.html:23-24` (sage wash)
- `layouts/partials/section-booking.html:43-44` (coral wash)
- `layouts/partials/section-about.html:11-12` (portrait placeholder)

Use this any time a decorative SVG needs CSS interaction. For purely static raster imagery (logo), keep `<img src>` from `static/`.

## 4. Watercolor wash placement

Each ambient background wash follows the same recipe: absolutely positioned, partial section coverage, `pointer-events: none`, `z-index: -1`, opacity 0.4–0.55, no width/height attributes on the SVG (controlled by parent).

- Hero (full-bleed bottom): `assets/css/main.css:294-300`
- About (right side): `assets/css/main.css:362-367`
- Booking (left bottom): `assets/css/main.css:546-551`

When adding a new wash, declare a `.<section>__wash` class with `position: absolute; pointer-events: none; z-index: -1`, place the wrapper div *inside* the section (which must be `position: relative`).

## 5. Data-driven content via `site.Data`

The four service cards are rendered by looping over `data/services.yaml`. The HTML template knows nothing about specific services — adding/removing/reordering services means editing YAML only.

- Loop: `layouts/partials/section-offer.html:8` (`range $i, $s := site.Data.services.services`)
- Stagger animation reads loop index: `style="--stagger:{{ mul $i 80 }}ms"`

Use `site.Data` (not the deprecated `.Site.Data`) for any future data-driven section.

## 6. Reveal-on-scroll

Any element that should fade-up on entering the viewport gets the `reveal` class. JS toggles `is-visible` once via IntersectionObserver; CSS transitions opacity + translateY. Honors `prefers-reduced-motion`.

- Class definition: `assets/css/main.css:639-650`
- Observer: `assets/js/main.js:30-43`
- Reduced-motion fallback: both CSS (`@media`) and JS (`matchMedia` check)

For staggered reveals, set `--stagger: <ms>` inline (see services loop above).

## 7. Centralized site params

Phone, email, social URLs live once in `hugo.toml [params]`. Templates read them via `.Site.Params.<key>`. Never hardcode contact info in a partial.

- Source: `hugo.toml` (`[params]` block)
- Consumed: `layouts/partials/section-contact.html:5,15,25,36` and `layouts/partials/head.html:7-13`

When introducing a new contact channel or repeated string, add it to `[params]` first.

## 8. Asset pipeline: fingerprinted CSS/JS

CSS and JS go through Hugo's asset pipeline for cache-busting. Pattern is identical for both:

```go
{{ $x := resources.Get "<path>" | minify | fingerprint }}
<link/script ... src="{{ $x.RelPermalink }}">
```

- CSS: `layouts/partials/head.html:18-19`
- JS: `layouts/index.html:11-12`

Static raster assets (logo, future photos) live in `static/` and are referenced via `relURL` — they bypass the pipeline. Decorative SVGs live in `assets/svg/` and are inlined (pattern 3), not pipelined.

## 9. CSS naming: BEM-ish + utility variables

Block-element classes per section (`.hero`, `.hero__inner`, `.hero__title`), modifiers with `--` (`.btn--primary`, `.offer__card--sage`). Color and spacing tokens are CSS variables defined once in `:root` (`assets/css/main.css:5-25`) — never hardcode hex values in component rules.

When the linter or a reviewer flags a magic value, promote it to `:root` instead of inlining.
