# Simple Jekyll Docs Template

This repository contains a minimal, simple and customizable Jekyll documentation template.

Features:
- Clean, responsive layout with lightweight CSS
- Navigation configurable via `_data/navigation.yml`
- Example docs in `docs/`
- Ready for GitHub Pages or local preview with Bundler

How to preview locally

1. Install Ruby and Bundler (if you don't have them).
2. From the repo root:

```bash
bundle install
bundle exec jekyll serve --livereload
```

Open http://localhost:4000 in your browser.

Notes:
- If publishing on GitHub Pages under a project site, set `baseurl: "/<repo-name>"` in `_config.yml`.
- Customize styles in `assets/css/styles.css`.
