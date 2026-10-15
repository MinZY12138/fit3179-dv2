# Deployment

Target repository: https://github.com/MinZY12138/fit3179-dv2

Target public URL: https://minzy12138.github.io/fit3179-dv2/

GitHub Pages: main branch, repository root. No backend, package installation or build service is required. The root contains ready-to-serve HTML, CSS, browser JS, readable chart specifications and processed datasets. `.nojekyll` avoids unnecessary Jekyll processing.

Before publication, browser checks passed at 1440, 1280, 1024 and 390 px, including a local `/fit3179-dv2/` URL to verify repository-prefix asset resolution. All 16 charts, map controls, table, linked highlight and reset were exercised. All source hashes and asset requests passed.

The original remote initial README commit `2d5fd0a` was retained as the parent of implementation commit `5c267dd`. No force-push or history overwrite occurred.

## Verified publication

- GitHub Pages build and deployment for `5c267dd` completed successfully on 16 October 2026.
- Public URL: https://minzy12138.github.io/fit3179-dv2/
- The public HTML contains all 16 chart containers. Actual Chrome tests against the public URL passed at 1440, 1280, 1024 and 390 px with all charts rendered, no horizontal page overflow, no chart errors, no console errors and no failed network requests.
- Public interaction tests passed for year, sector, linked selected state, eight-row exact-value table, reset, NSW hover tooltip and a mouse click updating the linked state highlight.
- Public chart/data/asset HTTP checks are recorded in `project_validation.json`; browser checks are recorded in `browser_validation.json`.
- A following documentation-only commit records these live checks. It does not alter the tested website or datasets.
