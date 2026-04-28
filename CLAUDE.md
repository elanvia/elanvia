# Elanvia

One-page static site for **Elanvia — Accompagnement vers l'équilibre**, the wellness practice of Laurie. Built with Hugo, deployed to GitHub Pages.

## Tech Stack

- **Hugo extended** v0.160+ (static site generator)
- **Vanilla CSS** (no framework, ~600 lines) with CSS custom properties
- **Vanilla JS** (no bundler, no deps) — IntersectionObserver, sticky nav
- **Google Fonts**: Fraunces (display), Pinyon Script (cursive accent), Mulish (body)
- **GitHub Actions** → GitHub Pages

No `npm`, no `package.json`, no node modules. The whole site is plain text files + 1 logo PNG.

## Project Structure

| Path | Purpose |
|------|---------|
| `hugo.toml` | Site config + all editable params (phone, email, socials, baseURL) |
| `content/_index.md` | Empty stub — page is rendered entirely by `layouts/index.html` |
| `data/services.yaml` | The 4 services with title/description/duration/price/accent — single source of truth for the offer section |
| `layouts/index.html` | Top-level page assembling 5 section partials |
| `layouts/partials/head.html` | `<head>`, fonts, fingerprinted CSS via `resources.Get` |
| `layouts/partials/nav.html` | Sticky nav with mobile toggle |
| `layouts/partials/section-{hero,about,offer,booking,contact}.html` | The 5 page sections (one per file) |
| `layouts/partials/footer.html` | Footer |
| `assets/css/main.css` | Full design system (variables, sections, responsive, motion) |
| `assets/js/main.js` | Sticky nav, mobile menu, scroll reveal observer |
| `assets/svg/wash-*.svg` | Decorative watercolor backgrounds, inlined into partials |
| `assets/svg/portrait-placeholder.svg` | Stand-in for Laurie's photo until provided |
| `assets/svg/grain.svg` | Paper grain texture overlay (referenced from CSS via `url()`) |
| `static/images/logo.png` | The Elanvia stamp logo (the only raster asset) |
| `.github/workflows/deploy.yml` | Build + publish to GitHub Pages on push to `main` |

## Build & Run

```bash
hugo server          # dev server with live reload → http://localhost:1313
hugo --minify        # production build → ./public/
```

No tests (static site). Verification = visual + Lighthouse + cross-browser smoke check.

## Editing Content (for Laurie, no Hugo knowledge needed)

- **Prices/services** → `data/services.yaml`
- **Phone, email, Instagram, Facebook** → `[params]` block in `hugo.toml`
- **Bio text** → `layouts/partials/section-about.html`
- **Hero baseline** → `layouts/partials/section-hero.html`
- **Replace portrait** → swap `assets/svg/portrait-placeholder.svg` with real image, update partial

## Design Direction

Editorial watercolor notebook. Cream paper backgrounds, high-contrast italic serif headings, cursive purple "Elanvia" accents matching the logo, watercolor SVG washes used sparingly. **Avoid**: generic wellness aesthetics (purple gradients, Inter, stock imagery).

Palette and motion details: `assets/css/main.css:1-30` (CSS variables block).

## Deployment

Push to `main` → GitHub Actions runs Hugo build → publishes to GitHub Pages. Configure once in repo Settings → Pages → Source: GitHub Actions. Update `baseURL` in `hugo.toml` once the final URL is known.

## Additional Documentation

When working on specialized aspects, read the relevant file:

- **[.claude/docs/architectural_patterns.md](.claude/docs/architectural_patterns.md)** — recurring patterns: section-header trio, accent-color theming via modifier classes, reveal-on-scroll, watercolor wash placement, data-driven services loop, asset pipeline conventions. **Read this before adding a new section, new service card variant, or new decorative element.**
