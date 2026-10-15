"""ABS ASGS boundaries and representative points; deterministic area cartogram."""
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlencode
import json, math, csv, hashlib

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw'
GEO = ROOT / 'data/geo'
GEO.mkdir(exist_ok=True)
codes = {'1':'NSW','2':'VIC','3':'QLD','4':'SA','5':'WA','6':'TAS','7':'NT','8':'ACT'}
base = 'https://geo.abs.gov.au/arcgis/rest/services/ASGS2021/STE/MapServer/'
manifest = []
for layer, name in [(1, 'abs_states'), (2, 'abs_state_points')]:
    params = {'where': "state_code_2021 IN ('1','2','3','4','5','6','7','8')", 'outFields':'state_code_2021,state_name_2021', 'outSR':4326,'f':'geojson','returnGeometry':'true'}
    if layer == 1: params.update(maxAllowableOffset=0.025, geometryPrecision=4)
    url = base + str(layer) + '/query?' + urlencode(params)
    file = RAW / (name + '.geojson')
    if not file.exists():
        with urlopen(url, timeout=60) as response: file.write_bytes(response.read())
    data = json.loads(file.read_text(encoding='utf-8'))
    assert len(data['features']) == 8, data
    for f in data['features']:
        p=f['properties']; p['state']=codes[p['state_code_2021']]
        if layer == 1:
            # ArcGIS GeoJSON follows RFC 7946 (CCW exteriors); D3 geographic
            # shapes use clockwise exteriors. Reverse every ring, including holes.
            g=f['geometry']; polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
            def signed_area(ring):
                return math.fsum(a[0]*b[1]-b[0]*a[1] for a,b in zip(ring,ring[1:]))/2
            cleaned=[]
            for poly in polys:
                # Generalisation can collapse tiny offshore rings. Such rings
                # can be interpreted as hemisphere complements by D3. Omit
                # sub-tolerance islands/holes, never entire jurisdictions.
                if abs(signed_area(poly[0])) < 0.001: continue
                kept=[]
                for index,ring in enumerate(poly):
                    area=signed_area(ring)
                    if abs(area)<0.00001:continue
                    if (index==0 and area>0) or (index>0 and area<0):ring.reverse()
                    kept.append(ring)
                cleaned.append(kept)
            assert cleaned
            g['coordinates']=cleaned if g['type']=='MultiPolygon' else cleaned[0]
    (GEO / (name + '.geojson')).write_text(json.dumps(data, separators=(',', ':'))+'\n', encoding='utf-8')
    manifest.append({'url':url,'file':file.name,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'retrieved':'2026-10-16','attribution':'Australian Bureau of Statistics, ASGS Edition 3 (2021), CC BY 4.0'})
(GEO/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
points=json.loads((GEO/'abs_state_points.geojson').read_text(encoding='utf-8'))
anchors={f['properties']['state']:f['geometry']['coordinates'] for f in points['features']}
anchors={k:(v[0] if isinstance(v[0],list) else v) for k,v in anchors.items()}
with (ROOT/'data/processed/state_points.csv').open('w',newline='',encoding='utf-8') as file:
    w=csv.writer(file);w.writerow(['state','longitude','latitude'])
    for state,(lon,lat) in anchors.items():w.writerow([state,lon,lat])

def project(point):
    # Spherical Albers equal-area: central meridian 132E, parallels 18S/36S.
    lon,lat=map(math.radians,point); p1,p2=map(math.radians,[-18,-36])
    n=(math.sin(p1)+math.sin(p2))/2; c=math.cos(p1)**2+2*n*math.sin(p1)
    rho=math.sqrt(c-2*n*math.sin(lat))/n; theta=n*(lon-math.radians(132))
    return [rho*math.sin(theta),rho*math.cos(theta)]

def ring_area(r):return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(r,r[1:]))/2

values={r['state']:float(r['teacher_fte']) for r in csv.DictReader((ROOT/'data/processed/workforce.csv').open()) if r['year']=='2025' and r['sector']=='All sectors' and r['state']!='Australia'}
features=json.loads((GEO/'abs_states.geojson').read_text(encoding='utf-8'))['features']
shapes=[]
# Schematic cartogram centres, not longitude/latitude or school locations.
# Preserve the broad west/east and north/south arrangement while separating
# enlarged outlines. ACT is moved east for visibility; Tasmania remains south.
centres={'WA':(100,300),'NT':(320,100),'SA':(330,390),'QLD':(650,220),'NSW':(650,550),'VIC':(480,770),'ACT':(850,690),'TAS':(650,900)}
for f in features:
    state=f['properties']['state'];g=f['geometry']; polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
    rings=[[project(p) for p in ring] for poly in polys for ring in poly]
    area=abs(sum(ring_area(r) for r in rings));pts=[p for r in rings for p in r]
    cx=(min(p[0] for p in pts)+max(p[0] for p in pts))/2;cy=(min(p[1] for p in pts)+max(p[1] for p in pts))/2
    scale=math.sqrt(values[state]*0.42/area)
    rings=[[[round((x-cx)*scale,3),round((y-cy)*scale,3)] for x,y in r] for r in rings]
    pts=[p for r in rings for p in r]
    shapes.append({'state':state,'teacher_fte':values[state],'area':area*scale*scale,'rings':rings,'rx':max(abs(p[0]) for p in pts),'ry':max(abs(p[1]) for p in pts),'x':centres[state][0],'y':centres[state][1]})
# Deterministic collision relaxation on bounding boxes. It changes positions,
# not shape sizes or areas. Approximate geographic arrangement remains.
for _ in range(250):
    for i,a in enumerate(shapes):
        for b in shapes[i+1:]:
            dx,dy=b['x']-a['x'],b['y']-a['y'];ox=a['rx']+b['rx']+18-abs(dx);oy=a['ry']+b['ry']+26-abs(dy)
            if ox>0 and oy>0:
                if ox<oy: shift=(ox/2+0.01)*(1 if dx>=0 else -1);a['x']-=shift;b['x']+=shift
                else:shift=(oy/2+0.01)*(1 if dy>=0 else -1);a['y']-=shift;b['y']+=shift
xmin=min(s['x']-s['rx'] for s in shapes);xmax=max(s['x']+s['rx'] for s in shapes)
ymin=min(s['y']-s['ry'] for s in shapes);ymax=max(s['y']+s['ry'] for s in shapes)
fit=min(700/(xmax-xmin),450/(ymax-ymin))
result=[]
for s in shapes:
    path=' '.join('M'+'L'.join(f'{x*fit:.3f},{y*fit:.3f}' for x,y in ring)+'Z' for ring in s['rings'])
    result.append({'state':s['state'],'teacher_fte':s['teacher_fte'],'path':path,'x':round((s['x']-xmin)*fit+(760-(xmax-xmin)*fit)/2,3),'y':round((s['y']-ymin)*fit+30,3),'area':s['area']*fit*fit,'year':2025})
ratios=[r['area']/r['teacher_fte'] for r in result]
assert max(ratios)-min(ratios)<1e-9
(GEO/'teacher_cartogram.json').write_text(json.dumps(result,separators=(',',':'))+'\n',encoding='utf-8')
print('Eight ABS states and points retained; cartogram area/FTE invariant passed. Files:',[(p.name,p.stat().st_size) for p in GEO.iterdir()])
