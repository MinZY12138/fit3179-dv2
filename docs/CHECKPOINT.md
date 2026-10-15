# Development checkpoint — intentional pause

**Historical record. Work resumed and the website implementation is now complete with 16 charts, three maps, linked interaction and browser checks. See `validation.md` and `deployment.md` for current status. The original pause notes below describe the earlier eight-chart checkpoint.**

Paused at the user's requested intermediate checkpoint to preserve usage allowance. Account quota cannot be read by this agent; this checkpoint is a conservative work-stage estimate, not a measured 50% quota reading.

## Saved work

- Original index backed up; static page redesigned with cream/teal/coral palette, serif headings, four chapters, caveats, source links and AI acknowledgement.
- Downloaded original ABS 51a, 53a and 43a workbooks from official 2025 release. AITSL June 2026 HTML snapshot retained; 27 official tables extracted exactly.
- Standard-library XLSX reader and repeatable pipeline; original workbooks are not edited.
- Eight standalone chart specifications; matching CSV files and exact values used in prose.
- 720 workforce aggregate rows, 2,700 published ratio rows. Teaching staff is selected case-insensitively because source label capitalisation changes across years.
- All eight charts compile and render to nonempty SVG with real data. JavaScript syntax check passed. QA SVGs are in ignored `.qa/`; reports in `docs/`.

## Next work, in order

1. Locate the official assignment PDF, critique PDF and template. They were absent from this project and the searched nearby `D:/MONASH/FIT3179` folder. No authoritative rubric classification has yet been verified.
2. Inspect all three reference sites visually and review their repositories. Direct web access to their GitHub Pages URLs failed. No assessment content or code was copied.
3. Acquire attributed Australian state/territory boundaries, ideally ABS ASGS; simplify without losing ACT, NT or Tasmania. Implement three genuinely distinct map idioms. Third map qualification must be checked against the actual rubric/tutor; a tile grid must not be assumed sufficient.
4. Add supported, non-redundant composition/experience/contract analysis, aiming at 12+ charts and enough distinct advanced idioms. AITSL Tables 7–9 are extracted but not yet charted. Do not derive precise values from report chart images.
5. Add useful sector/year/state controls and linked selections. Current interaction is tooltips/export only; controls are not yet implemented.
6. Review colour accessibility, story findings, source population definitions and complete notes. Inspect AITSL methodology/weighting and subgroup qualifications in depth before final copy.
7. Browser QA at 1440, 1280, 1024 and mobile widths: chart marks, clipped axes, SVG resizing, console/network errors, keyboard access, tooltips, page overflow and repository-subdirectory paths. No browser or Live Server verification has been performed yet.
8. Reconcile Git safely: local `main` has no commits; `origin/main` contains initial commit `2d5fd0a` with README. Local index was untracked initially. No reset, merge, commit or push performed. Preserve remote history; choose a safe initial-branch reconciliation when implementation is ready.
9. Commit/push and verify actual GitHub Pages deployment, only after local completion.
10. Hand-drawn sketch and final submission template remain the student's separate tasks.

## Reproducibility

Run the commands in README. `scripts/build_charts.py` owns specifications; `scripts/build_page.py` owns current generated HTML. Edit these sources if regenerating, or deliberately stop regeneration after editing outputs. The CSS and browser JS are authored directly.

No local preview server is left running by this stage. No credentials, repository history or deployment settings changed.
