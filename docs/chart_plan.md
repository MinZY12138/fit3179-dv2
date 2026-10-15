# Chart plan — What / Why / How

Classification is provisional until the official lecturer rubric is available. Multiple line variants may count as one idiom; this checkpoint does not assert HD compliance.

| Spec | Question / Why | What: population and variables | How: marks and channels | Reading / interaction | Classification and limitations |
| --- | --- | --- | --- | --- | --- |
| 01 | How has sector capacity changed? Compare trends | ABS 51a; national teaching FTE, sector, 2006–2025 | Lines; x year, y FTE, categorical sector colour | Government is the largest workforce; tooltips | Basic multi-line; no causal inference |
| 02 | Has teacher capacity kept pace? Compare relative growth | ABS 51a + 43a; national all-sector FTE, 2006 base | Lines; position encodes calculated index | Teacher growth exceeds student growth; tooltips | Indexed line; advanced status unverified; y starts at 95 explicitly |
| 03 | Has sector composition changed? Compare proportions | ABS 51a; sector FTE by year | Normalised stacked area; y share, colour sector | Composition independent of total growth; tooltips | Stacked area; classification unverified; nonbaseline sectors harder to compare |
| 04 | Where and when do ratios differ? Locate patterns | ABS 53a; eight states, year, all-sector/all-level ratio | Rectangles; grid position, sequential colour | Rows trace time, columns compare places; tooltips | Heatmap; candidate advanced; colour less precise than position |
| 05 | How do sectors differ within jurisdictions? Compare paired values | ABS 53a; 2025 government/non-government ratio, all levels | Connected points; x ratio, y state, categorical colour | Gap visible within each pair; tooltips | Dumbbell; candidate advanced; no claim about shortages |
| 06 | How do age profiles differ? Compare subgroup distributions | AITSL Table 3; 2024 classroom/relief subgroup shares | Lines/points; x ordered age bands, y percent, colour group | Relief teachers have higher oldest-band shares; tooltips | Frequency polygon; classification unverified; age widths unequal, categorical x |
| 07 | How broad is the working-hours range? Inspect published distribution summaries | AITSL Tables 22–24; 2024 full-time classroom teachers, term hours | Thin 5th–95th rule, thick IQR bar, median tick | Median 50h; tooltips show exact quantiles | Quantile interval plot; candidate advanced; not raw observations or standard min/max boxplot |
| 08 | Which pressures feature in departure intentions? Rank reasons | AITSL Table 21; 2024 teachers intending to leave | Horizontal bars; x percent, y reason | Multiple responses; workload prominent; tooltips | Basic bar; intentions differ from actual departure |

All charts have source/year captions, separate JSON, dataset links and export menus. ABS sources: https://www.abs.gov.au/statistics/people/education/schools/2025 . AITSL source: https://www.aitsl.edu.au/resources/national-trends-teacher-workforce . Source table numbers above identify exact variables.

## Implemented additions

| Spec | Question / Why | What: population and variables | How: marks and channels | Reading / interaction | Classification and limitations |
| --- | --- | --- | --- | --- | --- |
| 09 | Where does capacity relative to students differ? Compare geographic rates | ABS 53a, state/all-level ratio, 2006–2025, four school sectors | Choropleth; Albers geometry, fixed sequential colour | Year/sector controls, linked state highlight, click, tooltip, table | Advanced map; land area is not teacher count; ACT small but labelled and table accessible |
| 10 | Where is the workforce concentrated? Compare totals | ABS 51a teacher FTE, same states/years/sectors | Proportional circles at official ABS representative points; area encodes FTE | Same geographic explorer; fixed circle-area scale | Advanced map; aggregate anchor points, not school locations |
| 11 | What if area represented workforce rather than land? Compare geographic quantities | ABS 51a, all sectors, 2025 | Non-contiguous area cartogram; resized Albers outlines | Linked state highlight, exact tooltip | Advanced map; shape area/FTE invariant checked; schematic displacement, no meaningful distances |
| 12 | How common are employment arrangements? Compare composition | AITSL key findings, 2024 overall teacher workforce, 71/16/13% | 100-cell waffle; each cell is one percentage point; categorical colour | Tooltip and explicit written shares | Candidate advanced waffle; not sampled individuals, includes early childhood and casual workforce |
| 13 | How do career-stage profiles differ? Compare distributions | AITSL Table 7, classroom vs casual relief, 2024 | Mirrored experience pyramid; signed x for layout only, axis labels show positive shares | Tooltip; compare 40+ year tail and early-career shares | Candidate advanced pyramid; percentages within groups, unequal-width experience categories |
| 14 | Which reported pressures changed? Compare endpoints | AITSL Table 21, four selected reasons, 2020/2024 | Slopegraph, line endpoints, x year, y share, categorical reason | Tooltip; selected changes narrated | Candidate advanced slopegraph; independent weighted surveys, multi-response denominator restricted to intended leavers |
| 15 | How do state and sector structure fit together? Compare hierarchy | ABS 51a, state/sector FTE, 2025 | Nested treemap; area FTE, colour sector, labels state | Linked state highlight and exact tooltip | Candidate advanced treemap; small states require tooltip/table for precision |
| 16 | How does gender composition differ by setting? Compare subgroup shares | AITSL Table 3, women %, classroom/relief/early-childhood, 2024 | Lollipop; horizontal position percentage, aligned subgroup rows | Tooltip; early-childhood population caveat | Basic lollipop; no inferred binary complement or headcounts |

Eight or more *candidate* advanced idioms are present: three map types, heatmap, dumbbell, waffle, pyramid, slopegraph, treemap and quantile interval plot. This is not a rubric-confirmed classification; the official lecturer's classification was unavailable. The three map idioms differ in what is encoded: polygon colour for a rate, circle area at geographic anchors for a total, and polygon area for the geographic distribution of that total. The cartogram changes geometry and separates outlines; it is not a recoloured choropleth or an arbitrary tile grid.

## Replaced candidate plan (historical)

1. State ratio choropleth with suitable Australian equal-area projection; 2025 all-sector ratios. Requires attributed boundaries and ACT visibility treatment.
2. State-aggregate proportional symbol map of teacher FTE with explicitly explained representative locations, not implied school locations.
3. A defensible third geographic idiom, to be checked against rubric. Consider geographic small multiples or a properly justified cartogram; avoid claiming simple variation of the first two maps is distinct.
4. AITSL experience distributions (Table 7), employment arrangements (Tables 8–9), and observed changes in reported pressures (Table 21) provide further exact numerical evidence.

Each new chart must add an analytical question. No invented flows or detailed spatial allocations. Target 12+ meaningful charts and 8 rubric-confirmed advanced idioms without inflating counts through repetition.
