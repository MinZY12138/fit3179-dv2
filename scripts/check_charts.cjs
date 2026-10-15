// Headless Vega compilation and SVG rendering. QA libraries live in ignored .qa/.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const context = vm.createContext({ console, setTimeout, clearTimeout, URL, performance, structuredClone });
for (const file of ['vega.min.js', 'vega-lite.min.js']) vm.runInContext(fs.readFileSync(path.join(root, '.qa', file), 'utf8'), context);
const { vega, vegaLite } = context;
(async () => {
  const results = [];
  const geography = JSON.parse(fs.readFileSync(path.join(root, 'data/geo/abs_states.geojson'), 'utf8'));
  if (geography.features.length !== 8) throw new Error('Eight jurisdictions required');
  for (const feature of geography.features) {
    const area = vega.expressionFunction('geoArea')(null, feature);
    if (!(area > 0 && area < 1)) throw new Error(`Invalid spherical geometry for ${feature.properties.state}`);
  }
  for (const file of fs.readdirSync(path.join(root, 'charts')).filter(x => x.endsWith('.json'))) {
    const spec = JSON.parse(fs.readFileSync(path.join(root, 'charts', file), 'utf8'));
    spec.width = 760;
    const isVega = spec.$schema.includes('/vega/');
    const dataFile = isVega ? spec.data[0].url : spec.data?.url || 'multiple sources';
    const compiled = isVega ? spec : vegaLite.compile(spec).spec;
    const loader = vega.loader();
    loader.load = async uri => fs.readFileSync(path.join(root, uri), 'utf8');
    const view = new vega.View(vega.parse(compiled), { renderer: 'none', loader });
    await view.runAsync();
    const svg = await view.toSVG();
    if (svg.includes('NaN') || svg.includes('Infinity')) throw new Error(`${file}: non-finite SVG coordinates`);
    const sourceRows = view.data(compiled.data[0].name).length;
    if (!sourceRows) throw new Error(`${file}: no source records`);
    if (file === '09-ratio-choropleth.json') {
      const stateRows = Object.values(view.getState({ data: () => true }).data).find(rows => rows.length === 8 && rows[0].properties && Number.isFinite(rows[0].ratio));
      if (!stateRows || stateRows.some(row => !Number.isFinite(row.ratio))) throw new Error('Map joins failed');
    }
    fs.writeFileSync(path.join(root, '.qa', file.replace('.json', '.svg')), svg);
    results.push({ file, dataFile, sourceRows, svgBytes: Buffer.byteLength(svg), status: 'passed' });
    view.finalize();
  }
  fs.writeFileSync(path.join(root, 'docs/chart_runtime_validation.json'), JSON.stringify(results, null, 2) + '\n');
  console.log(JSON.stringify(results, null, 2));
})().catch(error => { console.error(error); process.exitCode = 1; });
