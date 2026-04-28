# Elanvia

Site one-page de **Elanvia — Accompagnement vers l'équilibre**, par Laurie.

Site statique construit avec [Hugo](https://gohugo.io/) (extended) et déployé sur GitHub Pages.

## Développement local

```bash
hugo server
```

Ouvrir http://localhost:1313/elanvia-site/

## Build de production

```bash
hugo --minify
```

Le site est généré dans `public/`.

## Édition du contenu

- **Tarifs et services** : `data/services.yaml`
- **Coordonnées (téléphone, email, réseaux)** : `hugo.toml` (section `[params]`)
- **Textes** : directement dans `layouts/partials/section-*.html`
- **Photo de Laurie** : remplacer `assets/svg/portrait-placeholder.svg` par une vraie image et ajuster le partial `section-about.html`

## Déploiement

Push sur la branche `main` → GitHub Actions construit et publie automatiquement sur la branche `gh-pages`.

À configurer dans le repo GitHub :
1. Settings → Pages → Source : `gh-pages` branch / `/ (root)`
2. Mettre à jour `baseURL` dans `hugo.toml` avec l'URL finale
