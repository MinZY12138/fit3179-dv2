# Data dictionary and transformations

## ABS workforce.csv

| Field | Definition |
| --- | --- |
| year | Integer reference year, 2006–2025 |
| state | NSW, VIC, QLD, SA, WA, TAS, NT, ACT, or calculated Australia |
| sector | Government, Catholic, Independent, or calculated All sectors |
| teacher_fte | Table 51a in-school FTE with Function = Teaching staff, summed over sex and primary/secondary school level |
| student_fte | Table 43a FTE All Students, summed over sex, FT/PT, school level and grade leaf records |

Data table sheets contain leaf records; pivot sheets are not aggregated, avoiding repeated subtotals. Source ordering prefixes such as `a ` and state punctuation are removed. Teaching function matching ignores letter case. Arithmetic uses Decimal, exported FTE aggregates use one decimal. Source leaf values are otherwise unchanged. State/sector keys are reconciled before joining students and teachers. Australia and All sectors are explicit sums of mutually exclusive leaf records, not additional source observations.

Table 43a notes random confidentiality adjustment; small differences from Table 53a may remain after ratio rounding. Do not infer false precision. The validation tolerance of 0.055 is reported explicitly; the largest observed difference is about 0.05016. Published ratios are used in charts instead of replacing them with calculations or averaging ratios.

## ABS ratios.csv

`year`, `state`, `sector`, `level`, `ratio` are normalised published Table 53a fields. Sector additionally includes Non-Government. Level is Primary School, Secondary School or All Levels. `ratio` is FTE students per FTE teaching staff, **not class size**. No ratio averaging is performed.

## Derived measures

- Index = value in year / value in 2006 × 100, separately for students and teachers.
- Growth (%) = (2025 value / 2006 value − 1) × 100.
- Sector share = sector teacher FTE / national teacher FTE for the same year.
- 2025 national teacher FTE = 325,190.5; display rounds to 325,191. National student FTE = 4,155,018.8. These are not headcounts.

## AITSL

`aitsl_tables.json` preserves the 27 report HTML tables in source order; it is a provenance intermediate, not a browser dependency. Superscript footnote numbers can be included in cell text; future extraction must explicitly validate those cells. Do not treat merged header cells as a rectangular dataset without interpretation.

- `age.csv`: exact Table 3 percentages for School classroom teachers and Casual relief teachers across six age groups. `percent` is share within subgroup, `year` = 2024; no age-band interpolation.
- `leaving_reasons.csv`: exact Table 21 percentages by reason and year. Blank cells remain absent, never zero. Reasons can be selected together, so percentages do not sum to 100. Denominator is teachers intending to leave before retirement.
- `working_hours.csv`: Tables 22–24, During term block only, full-time classroom teachers in primary, secondary and combined schools. `statistic` identifies published 5th percentile, 25th percentile, Median, 75th percentile and 95th percentile. `hours` is self-reported weekly working hours. These summaries are not raw individual observations.

AITSL reports workforce estimates, differing from ABS school FTE and registered-teacher headcounts. The report introduction states that survey percentages use weighted respondent counts, adjusting age/gender representation within jurisdictions and the number of responses between jurisdictions. The 2024 survey had 48,068 responses to at least part of the survey, 8.5% of registered teachers. All jurisdictions have participated since 2020; registered-teacher linkage included WA from 2023, affecting earlier alignment. Repeated-year comparisons are not a longitudinal panel of the same respondents.

## Additional AITSL datasets

- `experience.csv`: Table 7, six reported experience bands, classroom teachers, casual relief teachers and workforce overall. The pyramid compares classroom and relief subgroup shares; unequal duration of experience bands means bar length is share, not probability density.
- `gender.csv`: exact Table 3 reported percentages of women for school classroom teachers, casual relief teachers and early childhood-deployed teachers. No unreported gender percentages are inferred by subtraction.
- `employment.csv`: exact numerical key finding: 71% permanent, 16% casual, 13% fixed-term among the 2024 teacher workforce overall. This is not Table 8's deployed-workforce-only distribution. Waffle cells encode percentage points, not individual teachers; no sample records are fabricated.

## Geography and map values

- `map_values.csv`: unique state/year/sector key joins the verified workforce sums to published all-level ratios. Four sectors, 20 years, eight states = 640 rows. No duplication of overlapping government/non-government sectors.
- `state_points.csv`: official ABS ASGS 2021 representative-point coordinates, transformed to EPSG:4326 by the ABS service. These are aggregated jurisdiction anchors, not schools or assumed teacher residences.
- `abs_states.geojson`: ABS ASGS 2021 generalised polygons queried in EPSG:4326 with 0.025-degree service tolerance. Sub-tolerance offshore polygon fragments with planar area below 0.001 square degrees are omitted for small-scale display. All eight jurisdictions, including ACT and Tasmania, remain intact. This is geographic simplification, not a change to any statistical value. Exterior/hole winding is normalised for D3/Vega; spherical area tests prevent hemisphere-complement artifacts.
- Geographic choropleth and symbol maps use Albers conic equal-area, central meridian 132E and parallels 18S/36S. Fixed quantitative colour domain 10–17 covers all observed ratios (10.5–16.2); fixed symbol area domain 0–100,000 covers all observed teacher FTE values (maximum 95,431.3), allowing year/sector comparisons.
- `teacher_cartogram.json`: simplified polygons projected with a spherical Albers formula, then individually scaled by sqrt(FTE × common factor / projected area). Resulting outline area divided by FTE is invariant across all eight states, asserted in preparation and validation. Outline centres are repositioned schematically to separate shapes; ACT is moved east, Tasmania remains south. Coordinates describe the chart layout and must not be interpreted as geographical observations. No flows or school locations are inferred.
- `data/geo/manifest.json` records official service query URLs, raw snapshot hashes, retrieval date and CC BY 4.0 attribution. The raw ArcGIS response is retained unchanged; the processed display geometry is simplified as described above.
