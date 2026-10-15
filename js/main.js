'use strict';
const views = new Map();
const geoNames = ['09-ratio-choropleth', '10-teacher-symbols'];
const linkedNames = new Set([...geoNames, '04-ratio-heatmap', '05-sector-gap', '11-area-cartogram', '15-sector-treemap']);
const controls = { year: document.querySelector('#map-year'), sector: document.querySelector('#map-sector'), state: document.querySelector('#state-select') };
let mapRows = [];

function settings() { return { year: Number(controls.year.value), sector: controls.sector.value, state: controls.state.value }; }
function absolutizeUrls(value) {
  if (!value || typeof value !== 'object') return;
  for (const [key, child] of Object.entries(value)) {
    if (key === 'url' && typeof child === 'string' && child.startsWith('data/')) value[key] = new URL(child, document.baseURI).href;
    else absolutizeUrls(child);
  }
}
function dataLinks(spec) {
  const urls = new Set();
  function walk(value) {
    if (!value || typeof value !== 'object') return;
    if (typeof value.url === 'string') urls.add(value.url);
    Object.values(value).forEach(walk);
  }
  walk(spec);
  return [...urls];
}
async function updateExplorer() {
  const current = settings();
  const pending = [];
  for (const [name, { view }] of views) {
    if (linkedNames.has(name)) view.signal('selectedState', current.state);
    if (geoNames.includes(name)) view.signal('mapYear', current.year).signal('mapSector', current.sector);
    if (linkedNames.has(name)) pending.push(view.runAsync());
  }
  const table = document.querySelector('#state-table');
  table.replaceChildren();
  for (const row of mapRows.filter(r => r.year === current.year && r.sector === current.sector)) {
    const tr = document.createElement('tr');
    tr.classList.toggle('selected-row', row.state === current.state);
    for (const [index, value] of [row.state, row.teacher_fte.toLocaleString('en-AU', { maximumFractionDigits: 1 }), row.student_fte.toLocaleString('en-AU', { maximumFractionDigits: 1 }), row.ratio.toFixed(1)].entries()) {
      const td = document.createElement(index ? 'td' : 'th');
      if (!index) td.scope = 'row';
      td.textContent = value;
      tr.append(td);
    }
    table.append(tr);
  }
  document.querySelector('#explorer-status').textContent = `${current.year} · ${current.sector} · ${current.state === 'All states' ? 'All states shown' : current.state + ' highlighted'}. Cartogram and treemap: 2025, all sectors.`;
  await Promise.all(pending);
}

async function renderChart(element) {
  const name = element.dataset.chart;
  const specPath = `charts/${name}.json`;
  try {
    if (!window.vegaEmbed) throw new Error('The chart library could not load. Check your internet connection.');
    const response = await fetch(specPath);
    if (!response.ok) throw new Error(`Specification returned HTTP ${response.status}`);
    const spec = await response.json();
    const nativeVega = spec.$schema.includes('/vega/');
    if (name === '12-employment-waffle') spec.height = Math.round(element.clientWidth / 4);
    if (linkedNames.has(name) && !nativeVega && !spec.params?.some(p => p.name === 'selectedState')) {
      spec.params = [...(spec.params || []), { name: 'selectedState', value: 'All states' }];
      const opacity = { condition: { test: "selectedState === 'All states' || datum.state === selectedState", value: 1 }, value: 0.2 };
      if (spec.layer) spec.layer.forEach(layer => { layer.encoding = { ...(layer.encoding || {}), opacity }; });
      else spec.encoding.opacity = opacity;
    }
    if (element.clientWidth < 600 && !nativeVega) {
      spec.config.legend = { ...spec.config.legend, direction: 'vertical', columns: 1, labelLimit: 260 };
      if (spec.encoding?.y?.axis?.labelLimit) spec.encoding.y.axis.labelLimit = 130;
      if (name === '04-ratio-heatmap') spec.encoding.x.axis.labelExpr = 'toNumber(datum.label) % 2 === 1 ? datum.label : ""';
    }
    if (name === '04-ratio-heatmap') spec.encoding.color.legend = { direction: 'horizontal', gradientLength: 180, gradientThickness: 10 };
    if (geoNames.includes(name)) {
      spec.height = Math.min(440, Math.round(element.clientWidth * 0.9));
      if (name === '09-ratio-choropleth') spec.layer[0].encoding.color.legend = { title: 'Students per teacher FTE', direction: 'horizontal', gradientLength: 180, gradientThickness: 10 };
    }
    if (nativeVega) {
      spec.width = Math.max(240, element.clientWidth - 12);
      if (name === '11-area-cartogram') spec.height = spec.width * 520 / 760;
    }
    const linksToData = dataLinks(spec);
    absolutizeUrls(spec);
    const { view } = await vegaEmbed(element, spec, { renderer: 'svg', actions: { export: true, source: true, compiled: false, editor: false } });
    views.set(name, { view, element, nativeVega });
    if (linkedNames.has(name)) view.addEventListener('click', (_event, item) => {
      const state = item?.datum?.state || item?.datum?.properties?.state;
      if ([...controls.state.options].some(option => option.value === state)) {
        controls.state.value = state === controls.state.value ? 'All states' : state;
        updateExplorer().catch(console.error);
      }
    });
    let lastWidth = element.clientWidth;
    const observer = new ResizeObserver(() => {
      const width = element.clientWidth;
      if (Math.abs(lastWidth - width) < 2) return;
      lastWidth = width;
      if (nativeVega) {
        view.width(Math.max(240, width - 12));
        if (name === '11-area-cartogram') view.height((width - 12) * 520 / 760);
      }
      view.resize().runAsync().catch(console.error);
    });
    observer.observe(element);
    const links = document.createElement('p'); links.className = 'source chart-links';
    for (const [href, label] of [[specPath, 'Chart specification ↗'], ...linksToData.map((url, i) => [url, `Data${linksToData.length > 1 ? ' ' + (i + 1) : ''} ↗`])]) {
      const link = document.createElement('a'); link.href = href; link.textContent = label; links.append(link);
    }
    element.after(links);
    element.dataset.ready = 'true';
  } catch (error) {
    element.classList.add('chart-error');
    element.textContent = `This chart could not load. ${error.message}`;
    console.error(name, error);
  }
}

async function start() {
  const result = await fetch('data/processed/map_values.csv');
  if (!result.ok) throw new Error('State comparison data could not load.');
  mapRows = vega.read(await result.text(), { type: 'csv', parse: { year: 'number', ratio: 'number', teacher_fte: 'number', student_fte: 'number' } });
  const rendered = await Promise.allSettled([...document.querySelectorAll('[data-chart]')].map(renderChart));
  await updateExplorer();
  Object.values(controls).forEach(control => control.addEventListener('change', () => updateExplorer().catch(console.error)));
  document.querySelector('#reset-controls').addEventListener('click', () => {
    controls.year.value = '2025'; controls.sector.value = 'All sectors'; controls.state.value = 'All states';
    updateExplorer().catch(console.error);
  });
  // Read-only test surface for reproducible browser checks.
  window.workforceApp = { views, updateExplorer, rendered };
}
start().catch(error => {
  document.querySelector('#explorer-status').textContent = 'The data explorer could not load. Please refresh or check your connection.';
  console.error(error);
});
