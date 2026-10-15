"""Read reference sites/repositories for design study; no source reuse."""
from urllib.request import urlopen, Request
from urllib.parse import urljoin
from pathlib import Path
import re, json
OUT=Path(__file__).resolve().parents[1]/'.qa/references'
OUT.mkdir(parents=True,exist_ok=True)
for name,url,repo in [('emilia','https://emiliakylee.github.io/FIT3179-DV2/','Emiliakylee/FIT3179-DV2'),('hzern','https://hzern.github.io/fit3179-dv2/','HZern/fit3179-dv2'),('asher','https://asherdinggg.github.io/3179/','AsherDinggg/3179')]:
    html=urlopen(url,timeout=40).read().decode('utf-8')
    (OUT/(name+'.html')).write_text(html,encoding='utf-8')
    print(name,'HEADINGS',[re.sub('<[^>]+>','',v).strip() for v in re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>',html,re.S)][:14])
    assets=re.findall(r'''(?:src|href)=["']([^"']+(?:css|js|json))["']''',html)
    print('ASSETS',assets[:18])
    for asset in assets:
        if asset.endswith(('.css','.js')) and not asset.startswith('http'):
            code=urlopen(urljoin(url,asset),timeout=40).read().decode('utf-8')
            (OUT/(name+'-'+asset.replace('/','-'))).write_text(code,encoding='utf-8')
            print('IMPLEMENTATION',asset,'bytes',len(code),'fonts',re.findall(r'font-family\s*:\s*([^;}]+)',code)[:4],'CSS grids',code.count('grid-template-columns'),'embed calls',code.count('vegaEmbed'),'responsive queries',code.count('@media'))
    d=json.load(urlopen(Request('https://api.github.com/repos/'+repo+'/git/trees/HEAD?recursive=1',headers={'User-Agent':'teacher-workforce-research'}),timeout=40))
    print('REPO',[x['path'] for x in d.get('tree',[]) if x['path'].endswith(('.json','.css','.js'))][:30])
