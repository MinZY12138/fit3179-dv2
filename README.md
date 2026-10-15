# Who Teaches Australia?

FIT3179 Data Visualisation 2 · Teacher Workforce · 16 October 2026.

A buildless, single-page editorial story using official ABS Schools 2025 workbooks and AITSL National Trends: Teacher Workforce (June 2026). Includes 16 separately accessible Vega/Vega-Lite charts across four chapters, three distinct map idioms, linked state highlights, year and school-sector controls, exact-value tables, source notes and image export.

Public URL: https://minzy12138.github.io/fit3179-dv2/

The website implementation is complete. Academic submission still requires the hand-drawn sketch and submission template, plus confirmation against the official rubric, which was not supplied. An HD result is not guaranteed; see [acceptance checklist](docs/validation.md).

Open the root folder with VS Code Live Server and open `index.html`. Alternatively:

```powershell
python -m http.server 8000
```

Visit `http://localhost:8000/`. Opening HTML directly as `file://` will not reliably load chart/data fetches. Chart libraries load from pinned jsDelivr URLs and need internet access.

## Reproduce

Python 3.10+ and Node.js are sufficient; no Python packages or npm installation are needed.

```powershell
python scripts/download_sources.py
python scripts/prepare_data.py
python scripts/prepare_geography.py
python scripts/build_charts.py
python scripts/build_page.py
python scripts/download_qa_libraries.py
node scripts/check_charts.cjs
node --check js/main.js
python scripts/verify_project.py http://localhost:8000/
```

Original downloaded snapshots remain unchanged. `data/raw/manifest.json` records URLs, retrieval date, bytes and SHA-256 hashes. `docs/original-test-page.html` preserves the original test page. The browser loads only the small processed CSV files, not raw workbooks or the AITSL HTML snapshot.

See [data dictionary](docs/data_dictionary.md), [chart plan](docs/chart_plan.md), [source study](docs/reference_study.md) and [validation](docs/validation.md). Browser QA uses `scripts/browser_qa.cjs`, an installed headless Chrome instance on debugging port 9223, and Node's built-in WebSocket. Screenshots and QA libraries are ignored under `.qa/`.

Web datasets total about 315 KB before compression, including simplified geography. Original source downloads are retained in the repository for reproducibility and are not requested by the page. The browser relies on pinned CDN chart libraries.

AI assistance: OpenAI Codex assisted with extraction, code, chart specifications and editorial copy. The author must review findings, assignment compliance and final submission.
