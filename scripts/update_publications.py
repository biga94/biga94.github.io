#!/usr/bin/env python3
"""
Scarica la lista pubblicazioni da ORCID (API pubblica, nessuna auth richiesta)
e genera _data/publications.yml, che Jekyll espone automaticamente come
site.data.publications senza bisogno di plugin.

Usa solo la libreria standard di Python (nessun pip install in CI): per
evitare la dipendenza da PyYAML, sfrutta il fatto che una stringa JSON
valida è anche uno scalare YAML valido (json.dumps produce output YAML-safe
per stringhe, incluse quelle con virgolette o caratteri speciali).

Non modificare _data/publications.yml a mano: viene sovrascritto a ogni
run del workflow update-publications.yml.
"""
import json
import os
import sys
import urllib.request
import urllib.error

ORCID_ID = "0000-0002-6509-6870"
API_URL = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"
OUTPUT_PATH = "_data/publications.yml"


def fetch_works():
    req = urllib.request.Request(API_URL, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def extract(work_summary):
    title = (work_summary.get("title") or {}).get("title", {}).get("value")
    if not title:
        return None

    year_block = (work_summary.get("publication-date") or {}).get("year") or {}
    year_raw = year_block.get("value")
    year = int(year_raw) if year_raw else 0

    journal = (work_summary.get("journal-title") or {}).get("value")

    doi = None
    ext_ids = (work_summary.get("external-ids") or {}).get("external-id", [])
    for ext_id in ext_ids:
        if ext_id.get("external-id-type") == "doi":
            doi = ext_id.get("external-id-value")
            break

    if doi:
        url = f"https://doi.org/{doi}"
    else:
        url = (work_summary.get("url") or {}).get("value")

    return {"title": title, "year": year, "journal": journal, "doi": doi, "url": url}


def yaml_scalar(value):
    """Rappresentazione YAML sicura di una stringa o null, via JSON."""
    if value is None:
        return "null"
    return json.dumps(value, ensure_ascii=False)


def main():
    try:
        data = fetch_works()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        print(f"Errore nel contattare l'API ORCID: {e}", file=sys.stderr)
        sys.exit(1)

    entries = []
    for group in data.get("group", []):
        summaries = group.get("work-summary", [])
        if not summaries:
            continue
        # Un gruppo può avere più fonti per lo stesso lavoro (es. da diversi
        # database); ORCID mette per prima quella che considera preferita.
        entry = extract(summaries[0])
        if entry:
            entries.append(entry)

    entries.sort(key=lambda e: e["year"], reverse=True)

    lines = [
        "# File generato automaticamente da scripts/update_publications.py",
        "# via l'API pubblica di ORCID. NON MODIFICARE A MANO: viene",
        "# sovrascritto a ogni run del workflow update-publications.yml.",
        "",
    ]
    for e in entries:
        lines.append(f"- title: {yaml_scalar(e['title'])}")
        lines.append(f"  year: {e['year']}")
        lines.append(f"  journal: {yaml_scalar(e['journal'])}")
        lines.append(f"  doi: {yaml_scalar(e['doi'])}")
        lines.append(f"  url: {yaml_scalar(e['url'])}")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Scritte {len(entries)} pubblicazioni in {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
