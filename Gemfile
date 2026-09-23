source "https://rubygems.org"

# Uses the exact gem versions GitHub Pages runs in production,
# so a local preview matches what you'll see once it's live.
gem "github-pages", group: :jekyll_plugins

# Non è nella whitelist di plugin del build classico di GitHub Pages —
# per questo il sito ora si compila via GitHub Actions (vedi
# .github/workflows/jekyll.yml) invece che con il build automatico
# integrato, che ignora qualsiasi gem fuori dalla sua lista fissa.
gem "jekyll-scholar", group: :jekyll_plugins

# Windows/JRuby workaround some Jekyll setups still need; harmless elsewhere.
gem "wdm", "~> 0.1.1", :platforms => [:x64_mingw, :mingw]
