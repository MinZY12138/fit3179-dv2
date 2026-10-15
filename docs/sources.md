# Sources and provenance

Retrieved 16 October 2026. Exact download URLs and file SHA-256 hashes: `data/raw/manifest.json`.

- [ABS Schools, 2025](https://www.abs.gov.au/statistics/people/education/schools/2025), released 5 March 2026. Original Tables 51a, 53a, 43a preserved under `data/raw/`. Commonwealth of Australia / ABS attribution retained. Contents sheets and data table headers inspected; full source notes can be reproduced with `python -X utf8 scripts/inspect_workbooks.py`.
- [AITSL National Trends: Teacher Workforce, June 2026](https://www.aitsl.edu.au/resources/national-trends-teacher-workforce). HTML includes exact numerical tables and report edition identification. Snapshot retained. Table references appear in derived CSVs and chart captions. [ATWD portal](https://atwd.aitsl.edu.au/data/) is a further resource, not used to fabricate inaccessible values.

## Reference review

Direct web-tool access initially failed; Python HTTP access subsequently succeeded. All three pages, their CSS, available embedding JavaScript and public repository file trees were inspected. See `reference_study.md`. Downloaded reference material is isolated under ignored `.qa/references/` and is not part of the published project. No reference charts, content, data or code were reused.

- https://emiliakylee.github.io/FIT3179-DV2/ — https://github.com/Emiliakylee/FIT3179-DV2
- https://hzern.github.io/fit3179-dv2/ — https://github.com/HZern/fit3179-dv2
- https://asherdinggg.github.io/3179/ — https://github.com/AsherDinggg/3179

## Missing assessment resources

Official assignment PDF, Critique PDF, submission template and lecturer's advanced/basic idiom classification were not found in the project, nearby course workspace or targeted Downloads/Desktop search. The supplied brief governs implementation; official materials still need to be checked for submission.

## Geographic source

[ABS ASGS Edition 3 data services](https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs/edition-3-july-2021-june-2026/access-and-downloads/data-services-and-apis) identifies the official 2021 state/territory service. Layer 1 supplies generalised polygons; layer 2 supplies representative points. Queries, hashes and CC BY 4.0 attribution are in `data/geo/manifest.json`. Simplification, winding and cartogram transformations are documented in `data_dictionary.md`.
