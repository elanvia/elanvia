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

## Tests

```bash
bash tests/run_tests.sh
```

Trois vérifications enchaînées : validation du YAML (`data/services.yaml`), build Hugo + comptage des cartes de services, assertions sur la structure HTML générée.

## Formatage du code

```bash
npm install          # une seule fois
npm run format       # reformater tous les fichiers
npm run format:check # vérifier sans modifier (utilisé en CI)
```

Prettier formate CSS, JS et YAML. Les templates Hugo (`layouts/`) sont exclus (syntaxe Go non supportée).

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
