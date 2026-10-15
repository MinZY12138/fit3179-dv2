# Validation — 16 October 2026

The current implementation has 16 charts and three map idioms. The full academic compliance assessment is in [acceptance.md](acceptance.md). Public deployment results are in [deployment.md](deployment.md).

## Data integrity

- Original ABS/AITSL snapshots are unchanged; SHA-256 hashes pass.
- Unique ABS leaf records, eight jurisdictions and matched year/state/sector keys pass.
- 720 compatible student/teacher aggregates checked against published ratios. Maximum absolute difference ~0.05016; declared tolerance 0.055 allows published one-decimal ratios and student confidentiality adjustment.
- Published Table 53a ratios, not averages of ratios, are used in maps and comparisons.
- AITSL values come from exact HTML tables and explicitly numerical key findings. No chart-image estimates, invented observations, unreported gender complements or individual survey records are introduced.
- All eight cartogram areas divided by their corresponding FTE are equal within numeric tolerance.

## Rendering and geography

All 16 specifications compile/parse in Vega/Vega-Lite, load actual data and render nonempty SVG without NaN or Infinity. `chart_runtime_validation.json` records results. Geometry spherical-area checks reject hemisphere-complement artifacts. This caught a real simplification issue that was corrected before publication. Choropleth joins are checked for all eight states and finite ratio values.

## Actual Chrome browser tests

`browser_validation.json` records runs at 1440, 1280, 1024 and 390 px. All 16 charts rendered at every width; no page horizontal overflow, clipped chart container, chart-load error, console exception or failed network request remained. Desktop and mobile figure screenshots were inspected under ignored `.qa/`.

The geographic explorer was switched to 2006 / Independent / ACT; both map signals, linked cartogram highlighting, eight-row table and status text were checked. Reset returned to 2025 / All sectors / All states. Chrome mouse events hovered NSW, displaying its ratio tooltip, then clicked its label, updating the linked selected state to NSW. The check exercised real rendered browser events rather than only headless specification parsing.

Local tests also ran under `/fit3179-dv2/`, matching GitHub Pages' repository prefix. After publication, the full Chrome suite also passed against the actual public URL, https://minzy12138.github.io/fit3179-dv2/ . `project_validation.json` records successful HTTP requests for all 31 page/chart/data assets and a combined browser-data footprint of about 315 KB before compression. Raw source snapshots are not browser dependencies. CDN libraries are separately loaded, pinned and checked.

## Remaining limitations

- No official assignment PDF, Critique PDF, submission template or lecturer's idiom classification was available. Advanced-idiom classification is therefore provisional, despite ten defensible candidates.
- The student must complete the hand-drawn sketch and final submission/template tasks.
- Automated layout checks and sampled visual review do not certify every possible browser, device, colour-vision condition or assistive technology. Semantic headings, keyboard-accessible controls, visible focus, source/caveat text and a geographic exact-value table are implemented.
- CDN libraries need internet access. Public deployment was independently checked after GitHub Pages reported successful publication.

No assessment grade is guaranteed.
