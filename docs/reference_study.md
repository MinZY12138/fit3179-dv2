# Reference design and implementation study

All three live HTML pages, their stylesheets, available embedding JS and public repository file trees were read using `scripts/review_references.py`. Reference material is confined to ignored `.qa/references/`, not republished or used as assessment content. No grade is inferred from these examples.

## A — Emilia Kylee: university experience

https://emiliakylee.github.io/FIT3179-DV2/ · https://github.com/Emiliakylee/FIT3179-DV2

The page develops a question-led narrative from experience over time to fields of study, geography and student cohorts. Its explanatory headings make the interpretation clear before exploration. CSS pairs Inter with Source Serif 4, uses a limited number of grid arrangements and a responsive breakpoint. Its small main JS file loads separate Vega specifications; the repository has individually named trend, heatmap, dumbbell, slope, profile and geographic specifications. The useful lesson is editorial hierarchy and traceable chart files, rather than reproducing its composition or written argument.

## B — HZern: STEM education and workforce

https://hzern.github.io/fit3179-dv2/ · https://github.com/HZern/fit3179-dv2

The story follows a pipeline from school mathematics to university enrolments, international participation, gender and work. Its repository separates bump, heatmap, state choropleth, proportional symbols, flow, dumbbell and waffle specifications. CSS uses IBM Plex Sans/Space Grotesk, several grid arrangements and two responsive breakpoints. Separate state and world geometry files support different analytical scales. The useful lesson is choosing a chart idiom to match a specific comparison, with consistent technical organisation. Our project uses no flows because the workforce data contain no observed origin/destination relationships.

## C — Asher Ding: running in Australia

https://asherdinggg.github.io/3179/ · https://github.com/AsherDinggg/3179

The page connects participation, motivations, geography and events under a running theme. It uses question headings, a serif/sans pairing (Georgia and Arial), two grid arrangements and a mobile breakpoint. Its embedding JS references separate JSON idioms rather than a single large inline specification. The useful lesson is maintaining subject coherence across varied charts.

## Original implementation choices

Our four chapters follow the statistical argument: FTE growth, jurisdictional differences, workforce composition, then working conditions and intentions. A cream/teal/coral editorial palette, explicitly shared category colours, accessible exact-value explorer, official ABS representative points and a non-contiguous area cartogram were independently implemented for this dataset. There are no copied chart specifications, CSS, JS, prose, illustrations or datasets from these references. Source review informs general design principles; it does not substitute for the actual assignment rubric.
