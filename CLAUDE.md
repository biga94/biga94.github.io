# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Personal site for Davide Biganzoli, built with Jekyll (Minima theme), published via GitHub Pages at `https://biga94.github.io`. There is no build step beyond Jekyll itself — no bundler, no JS framework, no package.json.

Some commit messages and code comments are in Italian; matching that when editing comments in those files is fine, but is not required for new work.

## Commands

Local preview (requires Ruby + Bundler):

```bash
bundle install
bundle exec jekyll serve
```

Site is then at http://localhost:4000. There is no separate lint/test/build command — `jekyll serve` (or `jekyll build`) is the only pipeline, and it runs against the exact `github-pages` gem version GitHub Pages uses in production (pinned in `Gemfile`).

## Architecture

- **Deploy**: GitHub Pages builds and deploys directly from `main` on push — there is no custom deploy workflow in `.github/workflows/`. Any content/template change merged to `main` goes live automatically.
- **Data-driven content over hardcoded HTML**: two pages pull from `_data/*.yml` instead of embedding content in the page — `publications.md` reads `site.data.publications`, and `_includes/now-listening.html` reads `site.data.now_listening`. Both files degrade gracefully when the data is empty/null (a "loading" message, or the include rendering nothing).
- **`_data/publications.yml` is machine-generated, never hand-edited.** It's rebuilt by `.github/workflows/update-publications.yml` (weekly cron + manual dispatch), which runs `scripts/update_publications.py` — a stdlib-only Python script that queries the public ORCID API (`ORCID_ID` constant in the script) and writes YAML by hand via `json.dumps` for scalar escaping (to avoid a PyYAML dependency in CI). The workflow commits and pushes only if the file actually changed, and is intentionally decoupled from the Jekyll build/deploy — if ORCID fetching fails, the site stays up unchanged.
- **`_data/now_listening.yml` is also machine-written, by an external iPhone Shortcut** via the GitHub Contents API (not by any code in this repo). Its schema is a single `url:` key — don't change that shape, since the Shortcut expects to find exactly that key when it reads the file's current sha before overwriting it. The include only renders when the URL is an Apple Music link (`music.apple.com` → rewritten to `embed.music.apple.com` for the iframe embed).
- **Minima theme overrides**: `_includes/header.html` and `_includes/footer.html` deliberately override Minima's defaults (documented inline): header excludes `index.md` from nav since it's the home page rendering itself otherwise, and footer drops Minima's redundant `h-card` author line, keeping only the email/contact row. `assets/main.scss` starts with `@import "minima"` and layers site-specific rules (profile header, social icons, now-listening block, publication list, a narrow-viewport breakpoint) on top — it needs Jekyll's Sass front matter (the empty `---` block) to be processed at all, not served as raw text.
- **`_includes/person-schema.html`** emits `Person` JSON-LD (schema.org) and is included on both the home page and publications page for SEO; sameAs links there should stay in sync with the social icons in `index.md`.
