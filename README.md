# biga94.github.io

Sito personale su Jekyll + tema Minima, pubblicato via GitHub Pages.

## Anteprima locale (opzionale)

Richiede Ruby e Bundler.

```bash
bundle install
bundle exec jekyll serve
```

Poi apri http://localhost:4000

## Struttura

- `_config.yml` — configurazione del sito (titolo, tema, plugin)
- `index.md` — home page (link di contatto + lista post)
- `_posts/` — i post, uno per file, nome `YYYY-MM-DD-titolo.md`

Per scrivere un nuovo post: copia il formato in `_posts/`, cambia data e titolo nel front matter, scrivi in Markdown, fai commit e push su `main`. GitHub Pages ricompila automaticamente.
