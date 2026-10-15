// Chrome DevTools Protocol smoke tests, using Node's built-in WebSocket.
const fs = require('node:fs');
const path = require('node:path');
const { setTimeout: pause } = require('node:timers/promises');
const root = path.resolve(__dirname, '..');
async function main() {
  const list = await (await fetch('http://127.0.0.1:9223/json/list')).json();
  const target = list.find(t => t.type === 'page');
  const socket = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise(resolve => socket.addEventListener('open', resolve, { once: true }));
  const pending = new Map(); let id = 0; const errors = [], failures = [];
  socket.addEventListener('message', ({ data }) => {
    const message = JSON.parse(data);
    if (message.id) { const p = pending.get(message.id); pending.delete(message.id); message.error ? p.reject(message.error) : p.resolve(message.result); }
    if (message.method === 'Runtime.exceptionThrown') errors.push(message.params.exceptionDetails.text + ': ' + (message.params.exceptionDetails.exception?.description || ''));
    if (message.method === 'Runtime.consoleAPICalled' && message.params.type === 'error') errors.push(message.params.args.map(a => a.value || a.description).join(' '));
    if (message.method === 'Network.loadingFailed') failures.push(message.params.errorText);
    if (message.method === 'Network.responseReceived' && message.params.response.status >= 400) failures.push(message.params.response.url + ' ' + message.params.response.status);
  });
  const send = (method, params = {}) => new Promise((resolve, reject) => { const n = ++id; pending.set(n, { resolve, reject }); socket.send(JSON.stringify({ id: n, method, params })); });
  const evaluate = async expression => {
    const result = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    if (result.exceptionDetails) throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
    return result.result.value;
  };
  await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable');
  const results = [];
  const base = process.argv[2] || 'http://127.0.0.1:8000/';
  for (const width of [1440, 1280, 1024, 390]) {
    await send('Emulation.setDeviceMetricsOverride', { width, height: 900, deviceScaleFactor: 1, mobile: false });
    await send('Page.navigate', { url: base });
    let ready = false;
    for (let n = 0; n < 100; n++) { await pause(200); if (await evaluate('!!window.workforceApp')) { ready = true; break; } }
    if (!ready) throw new Error('Page did not finish rendering');
    const metrics = await evaluate(`({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,charts:document.querySelectorAll('[data-ready="true"]').length,chartErrors:document.querySelectorAll('.chart-error').length,svgCount:document.querySelectorAll('.chart svg').length,clippedCharts:[...document.querySelectorAll('.chart')].filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>e.dataset.chart)})`);
    const screenshot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
    fs.writeFileSync(path.join(root, '.qa', `page-${width}.png`), Buffer.from(screenshot.data, 'base64'));
    if (metrics.charts !== 16 || metrics.chartErrors || metrics.scrollWidth > width || metrics.clippedCharts.length) throw new Error(JSON.stringify(metrics));
    if (width === 1280 || width === 390) {
      const names = await evaluate(`[...document.querySelectorAll('figure .chart')].map(e=>e.dataset.chart)`);
      for (const name of names) {
        await evaluate(`document.querySelector('[data-chart="${name}"]').closest('figure').scrollIntoView({behavior:'instant',block:'start'})`);
        const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
        fs.writeFileSync(path.join(root, '.qa', `${name}-${width}.png`), Buffer.from(shot.data, 'base64'));
      }
    }
    results.push(metrics);
  }
  await evaluate(`(async()=>{document.querySelector('#map-year').value='2006';document.querySelector('#map-sector').value='Independent';document.querySelector('#state-select').value='ACT';await workforceApp.updateExplorer();return true})()`);
  const interaction = await evaluate(`({year:workforceApp.views.get('09-ratio-choropleth').view.signal('mapYear'),sector:workforceApp.views.get('10-teacher-symbols').view.signal('mapSector'),selectedState:workforceApp.views.get('11-area-cartogram').view.signal('selectedState'),tableRows:document.querySelectorAll('#state-table tr').length,status:document.querySelector('#explorer-status').textContent})`);
  if (interaction.year !== 2006 || interaction.sector !== 'Independent' || interaction.selectedState !== 'ACT' || interaction.tableRows !== 8) throw new Error('Interaction check failed');
  await evaluate(`document.querySelector('#reset-controls').click()`); await pause(100);
  const reset = await evaluate(`workforceApp.views.get('09-ratio-choropleth').view.signal('mapYear')===2025 && workforceApp.views.get('11-area-cartogram').view.signal('selectedState')==='All states'`);
  await evaluate(`document.querySelector('[data-chart="09-ratio-choropleth"]').scrollIntoView({behavior:'instant',block:'start'})`);
  const nsw = await evaluate(`(()=>{const e=[...document.querySelectorAll('[data-chart="09-ratio-choropleth"] svg text')].find(t=>t.textContent==='NSW');const r=e.getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()`);
  await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: nsw.x, y: nsw.y + 14 }); await pause(100);
  const tooltip = await evaluate(`document.querySelector('#vg-tooltip-element')?.textContent || ''`);
  await send('Input.dispatchMouseEvent', { type: 'mousePressed', x: nsw.x, y: nsw.y, button: 'left', clickCount: 1 });
  await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: nsw.x, y: nsw.y, button: 'left', clickCount: 1 }); await pause(100);
  const clickedState = await evaluate(`workforceApp.views.get('11-area-cartogram').view.signal('selectedState')`);
  const report = { base, results, interaction, reset, tooltip, clickedState, errors, failures };
  fs.writeFileSync(path.join(root, 'docs/browser_validation.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
  await send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 900, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: base });
  socket.close();
  if (errors.length || failures.length || !reset || clickedState !== 'NSW' || !tooltip.includes('NSW')) process.exitCode = 1;
}
main().catch(error => { console.error(error); process.exit(1); });
