"""Check publication assets, provenance, chart coverage and numeric invariants."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import urlopen
import json, hashlib, csv, sys
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self): super().__init__();self.charts=[];self.assets=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'data-chart' in attrs:self.charts.append(attrs['data-chart'])
        for key in ['src','href']:
            value=attrs.get(key,'')
            if value and not value.startswith(('http','#','mailto:')):self.assets.append(value)
page=Page();page.feed((ROOT/'index.html').read_text(encoding='utf-8'))
assert len(page.charts)==16 and len(set(page.charts))==16
paths=set(page.assets)
def assets(value):
    if not isinstance(value,(dict,list)):return
    if isinstance(value,dict):
        if isinstance(value.get('url'),str) and value['url'].startswith('data/'):paths.add(value['url'])
        for v in value.values():assets(v)
    else:
        for v in value:assets(v)
for name in page.charts:
    paths.add('charts/'+name+'.json')
    assets(json.loads((ROOT/'charts'/f'{name}.json').read_text(encoding='utf-8')))
for path in paths:assert (ROOT/path).is_file(),path
for item in json.loads((ROOT/'data/raw/manifest.json').read_text()):
    assert hashlib.sha256((ROOT/'data/raw'/item['file']).read_bytes()).hexdigest()==item['sha256']
cartogram=json.loads((ROOT/'data/geo/teacher_cartogram.json').read_text())
assert len(cartogram)==8
area_per_fte=[r['area']/r['teacher_fte'] for r in cartogram]
assert max(area_per_fte)-min(area_per_fte)<1e-9
csv_files=set(p for p in paths if p.endswith('.csv'))
csv_bytes=sum((ROOT/p).stat().st_size for p in csv_files)
data_bytes=sum((ROOT/p).stat().st_size for p in paths if p.startswith('data/'))
assert data_bytes<2_000_000
base=sys.argv[1] if len(sys.argv)>1 else None
if base:
    for path in sorted(paths):
        with urlopen(base.rstrip('/')+'/'+path,timeout=30) as response:assert response.status==200
report={'chart_count':16,'map_idioms':['Choropleth','Proportional symbol map','Non-contiguous area cartogram'],'asset_count':len(paths),'chart_csv_bytes':csv_bytes,'browser_data_bytes':data_bytes,'raw_hashes':'passed','cartogram_area_invariant':'passed','checked_base':base,'asset_requests':'passed' if base else 'not requested'}
(ROOT/'docs/project_validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
