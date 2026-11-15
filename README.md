# Sanita Reinsone

Bilingual static website for Sanita Reinsone. Latvian pages are at the root; matching English pages are in `en/`. No package installation, database or server is required.

## Publish on GitHub Pages

1. Create a GitHub repository with `main` as its default branch.
2. Add the contents of this package to the repository, preserving `.github/workflows/pages.yml`, `src/`, `scripts/` and `dist/`.
3. In **Settings → Pages → Build and deployment → Source**, select **GitHub Actions**.
4. Push to `main`, or run **Deploy website to GitHub Pages** in the Actions tab.

The workflow builds both languages, checks internal links, and publishes only `dist/`. Source data, documentation and build tools are not included in the deployed website. Relative links support both `username.github.io` and `username.github.io/repository/` URLs. A custom domain can be configured later in Settings → Pages; none is preconfigured in this package.

GitHub documentation: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Edit and preview

Run these commands from the repository root using Python 3.10 or newer:

```sh
python3 src/build_full_site.py
python3 scripts/check_site.py
python3 -m http.server 8765 --directory dist
```

Open `http://localhost:8765/` or `http://localhost:8765/en/`.

- `src/data/`: public content, publication records, project information and meeting records.
- `src/english_dictionary.py` and `src/english_extra.py`: English interface and descriptive translations.
- `src/research-graph-template.js`: research graph behaviour and layout logic.
- `dist/style.css`: shared visual styles.
- `dist/main.js` and `dist/publicity.js`: shared interactions; English scripts are generated automatically.
- `dist/assets/`: original photographs, book covers and illustrations used by the site.

Publication titles, names and media headlines remain in their original languages. Update descriptions in the translation dictionaries when changing Latvian copy. The build keeps the two language versions aligned and adds reciprocal language links. The language switch preserves the current research theme and anchor.

Photographs and illustrations retain their existing credits. No general reuse licence is granted for text, photographs, illustrations or book covers.
