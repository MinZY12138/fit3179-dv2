"""Editorial refinements, derived annotations and readable scales for final charts."""
import json
import csv
import textwrap

def refine(folder):
    def load(name): return json.loads((folder / (name+'.json')).read_text(encoding='utf-8'))
    def save(name,spec): (folder/(name+'.json')).write_text(json.dumps(spec,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    def text_layer(test, text, **mark):
        return {'transform':[{'filter':test}],'mark':{'type':'text','fontSize':12,'fontWeight':'bold',**mark},'encoding':{'text':{'field':text,'type':'nominal'}}}
    for file in folder.glob('*.json'):
        s=json.loads(file.read_text(encoding='utf-8'))
        if '/vega-lite/' in s['$schema']:
            s['config']['axis'].update(labelFontSize=12,titleFontSize=13,tickCount=6)
            s['config']['legend'].update(labelFontSize=12,labelLimit=300)
        save(file.stem,s)

    s=load('01-teacher-trends')
    s['title']={'text':'Government schools remain the largest employer','anchor':'start','fontSize':13,'color':'#23776f'}
    save('01-teacher-trends',s)
    s=load('03-sector-shares')
    s['title']={'text':'Independent share: 15.3% → 18.8%','subtitle':'Share of national teacher FTE, 2006 → 2025','anchor':'start','fontSize':13,'color':'#23776f'}
    save('03-sector-shares',s)

    s=load('04-ratio-heatmap');s['encoding']['color']['scale']['domain']=[10,17]
    s['encoding']['stroke']={'condition':{'test':"datum.year === 2025 && (datum.state === 'WA' || datum.state === 'NT')",'value':'#263e3b'},'value':'#faf8f2'}
    s['encoding']['strokeWidth']={'condition':{'test':"datum.year === 2025 && (datum.state === 'WA' || datum.state === 'NT')",'value':2},'value':1}
    s['title']={'text':'The 2025 contrast: WA 13.7 · NT 11.0','subtitle':'Outlined cells locate the highest and lowest 2025 ratios. Colours share the map’s 10–17 scale.','anchor':'start','fontSize':13}
    save('04-ratio-heatmap',s)

    s=load('05-sector-gap');s['encoding']['x']['scale']['domain']=[10,15]
    s['title']={'text':'Sector differences do not all point the same way','subtitle':'Comparison scale starts at 10. Government has the higher ratio in WA; the lower ratio in NT.','anchor':'start','fontSize':13}
    s['transform'] += [{'joinaggregate':[{'op':'max','field':'ratio','as':'hi'},{'op':'min','field':'ratio','as':'lo'}],'groupby':['state']},{'calculate':"'Gap ' + format(datum.hi-datum.lo,'.1f')",'as':'gapLabel'}]
    t=text_layer("datum.state === 'WA' && datum.sector === 'Government'",'gapLabel',align='right',dy=-15,color='#263e3b')
    s['layer'].append(t);save('05-sector-gap',s)

    s=load('06-age-profile');s['transform']=[{'calculate':"format(datum.percent,'.0f') + '%'",'as':'label'}]
    m=s.pop('mark');s['layer']=[{'mark':m},text_layer("datum.age === '69+'",'label',align='right',dx=-8,dy=-13)]
    s['title']={'text':'Aged 60+: 41% of relief teachers, 14% of classroom teachers','subtitle':'Reported age-band shares added within each subgroup; percentages are rounded.','anchor':'start','fontSize':13}
    save('06-age-profile',s)

    s=load('07-hours-interval')
    s['layer'].append({'mark':{'type':'text','dy':-23,'color':'#23776f','fontWeight':'bold','fontSize':12},'encoding':{'x':{'field':'Median','type':'quantitative'},'text':{'field':'Median','type':'quantitative','format':'.0f'}}})
    s['title']={'text':'50 hours is the median in all three settings','subtitle':'Thick bar: middle half of responses · thin line: 5th–95th percentiles · light tick: median','anchor':'start','fontSize':13}
    save('07-hours-interval',s)

    s=load('08-leaving-reasons');s['height']=900
    s['transform'].append({'calculate':"replace(datum.reason, '*', '')",'as':'displayReason'})
    reasons=[r['reason'].replace('*','') for r in csv.DictReader((folder.parent/'data/processed/leaving_reasons.csv').open(encoding='utf-8')) if r['year']=='2024']
    wrapped={r:textwrap.wrap(r,width=36,break_long_words=False) for r in reasons}
    s['encoding']['y'].update(field='displayReason',axis={'labelLimit':0,'labelFontSize':12,'labelLineHeight':14,'labelExpr':f'({json.dumps(wrapped)})[datum.label] || datum.label'})
    order=sorted([r for r in csv.DictReader((folder.parent/'data/processed/leaving_reasons.csv').open(encoding='utf-8')) if r['year']=='2024'],key=lambda r:-float(r['percent']))
    s['encoding']['y']['sort']=[r['reason'].replace('*','') for r in order]
    s['transform'].append({'calculate':"format(datum.percent,'.0f')+'%'",'as':'label'})
    m=s.pop('mark');s['layer']=[{'mark':m},{'mark':{'type':'text','align':'left','dx':6,'fontSize':12,'color':'#263e3b'},'encoding':{'text':{'field':'label','type':'nominal'}}}]
    s['title']={'text':'75% of intended leavers selected workload','subtitle':'All 22 reported reasons shown. Multiple selections were allowed; this is not a share of all teachers.','anchor':'start','fontSize':13}
    save('08-leaving-reasons',s)

    # Derive map callouts from the active scope, never hard-code 2025 labels
    # on a map that can be filtered to other years or school sectors.
    s=load('09-ratio-choropleth')
    s['layer'][0]['encoding']['tooltip'][0]['field']='properties.state_name_2021'
    s['transform'] += [{'lookup':'properties.state','from':{'data':{'url':'data/processed/state_points.csv','format':{'type':'csv'}},'key':'state','fields':['longitude','latitude']}},{'joinaggregate':[{'op':'min','field':'ratio','as':'minimum'},{'op':'max','field':'ratio','as':'maximum'}]},{'calculate':"format(datum.ratio,'.1f') + (datum.ratio === datum.maximum ? ' · highest' : ' · lowest')",'as':'extreme'}]
    s['layer'].append({'transform':[{'filter':'datum.ratio === datum.maximum || datum.ratio === datum.minimum'}],'mark':{'type':'text','dy':15,'fontSize':12,'fontWeight':'bold','fill':'#263e3b','stroke':'#faf8f2','strokeWidth':3},'encoding':{'longitude':{'field':'longitude','type':'quantitative'},'latitude':{'field':'latitude','type':'quantitative'},'text':{'field':'extreme','type':'nominal'}}})
    save('09-ratio-choropleth',s)
    s=load('10-teacher-symbols');points=s['layer'][1]
    points['transform'] += [{'joinaggregate':[{'op':'sum','field':'teacher_fte','as':'total'},{'op':'max','field':'teacher_fte','as':'largest'}]},{'calculate':"format(datum.teacher_fte,',.0f')+' FTE · '+format(datum.teacher_fte/datum.total,'.1%')",'as':'largestLabel'}]
    s['layer'].append({'data':points['data'],'transform':points['transform']+[{'filter':'datum.teacher_fte === datum.largest'}],'mark':{'type':'text','dy':21,'fontSize':12,'fontWeight':'bold','fill':'#263e3b','stroke':'#faf8f2','strokeWidth':3},'encoding':{'longitude':{'field':'longitude','type':'quantitative'},'latitude':{'field':'latitude','type':'quantitative'},'text':{'field':'largestLabel','type':'nominal'}}})
    save('10-teacher-symbols',s)

    s=load('11-area-cartogram');s['title']={'text':'NSW + Victoria account for 56.7% of teacher FTE','subtitle':'2025 · all sectors · shape area represents workforce, not land','anchor':'start','fontSize':14,'color':'#23776f'}
    save('11-area-cartogram',s)
    s=load('12-employment-waffle');s['title']={'text':'71% permanent · 16% casual · 13% fixed-term','subtitle':'One cell = one percentage point, not an individual respondent','anchor':'start','fontSize':13};save('12-employment-waffle',s)
    s=load('13-experience-pyramid');s['title']={'text':'40+ years’ experience: relief 24% · classroom 6%','anchor':'start','fontSize':13};save('13-experience-pyramid',s)
    s=load('14-pressure-slope');s['height']=360
    s['transform'].append({'calculate':"datum.reason + '  ' + format(datum.percent,'.0f')+'%'",'as':'endLabel'})
    m=s.pop('mark');s['layer']=[{'mark':m}]+[text_layer(f"datum.year === 2024 && datum.reason === '{reason}'",'endLabel',align='right',dx=-8,dy=offset) for reason,offset in [('Workload',-14),('Insufficient pay',-22),('Student behaviour',0),('Class size',15)]]
    s['title']={'text':'Higher than 2020 does not mean a continuous rise','subtitle':'Workload fell from 80% in 2021 to 75% in 2024; pay fell from 54% in 2023 to 48% in 2024.','anchor':'start','fontSize':13}
    save('14-pressure-slope',s)
    s=load('15-sector-treemap');s['title']={'text':'Government schools account for 61.9% of teacher FTE','subtitle':'2025 · rectangles are grouped by state, then school sector','anchor':'start','fontSize':14};save('15-sector-treemap',s)
    s=load('16-gender-profile');s['transform']=[{'calculate':"format(datum.percent,'.0f')+'%'",'as':'label'}]
    s['layer'].append({'mark':{'type':'text','align':'right','dx':-9,'dy':-14,'fontSize':12,'fontWeight':'bold'},'encoding':{'text':{'field':'label','type':'nominal'}}});save('16-gender-profile',s)
