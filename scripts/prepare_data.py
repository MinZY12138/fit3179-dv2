"""Reproduce small web datasets from official snapshots, using only stdlib."""
from collections import defaultdict
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path
import csv
import json
import re
from inspect_workbooks import sheets, ROOT

OUT = ROOT / 'data/processed'
STATES = {'NSW', 'VIC', 'QLD', 'SA', 'WA', 'TAS', 'NT', 'ACT'}

def clean(value):
    return re.sub(r'^[a-z] ', '', value).strip().rstrip('.')

def state(value):
    value = clean(value).upper()
    return 'Australia' if value == 'AUST' else value

def write(name, rows):
    assert rows, name
    with (OUT / name).open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def records(filename, tab):
    return [cells for name, rows in sheets(ROOT / 'data/raw' / filename) if name == tab for number, cells in rows if number >= 5 and cells.get('A', '').isdigit()]

class Tables(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables, self.table, self.row, self.cell = [], None, None, None
    def handle_starttag(self, tag, attrs):
        if tag == 'table': self.table = []
        elif tag == 'tr' and self.table is not None: self.row = []
        elif tag in ('td', 'th') and self.row is not None: self.cell = []
    def handle_data(self, data):
        if self.cell is not None: self.cell.append(data)
    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cell is not None:
            self.row.append(re.sub(r'\s+', ' ', ''.join(self.cell)).strip())
            self.cell = None
        elif tag == 'tr' and self.row is not None:
            self.table.append(self.row)
            self.row = None
        elif tag == 'table' and self.table is not None:
            self.tables.append(self.table)
            self.table = None

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    teachers, students = defaultdict(Decimal), defaultdict(Decimal)
    teacher_keys, student_keys = set(), set()
    for r in records('abs_51a.xlsx', 'Table 2 Data table'):
        if clean(r['G']).casefold() != 'teaching staff': continue
        assert state(r['B']) in STATES
        key = tuple(r.get(c, '') for c in 'ABCDEFG')
        assert key not in teacher_keys, key
        teacher_keys.add(key)
        teachers[int(r['A']), state(r['B']), clean(r['D'])] += Decimal(r['H'])
    for r in records('abs_43a.xlsx', 'Table 2 Data table'):
        assert state(r['B']) in STATES
        key = tuple(r.get(c, '') for c in 'ABCDEFGHI')
        assert key not in student_keys, key
        student_keys.add(key)
        students[int(r['A']), state(r['B']), clean(r['D'])] += Decimal(r['L'])
    assert teachers.keys() == students.keys()
    rows = []
    for year in range(2006, 2026):
        for region in sorted(STATES) + ['Australia']:
            for sector in ['Government', 'Catholic', 'Independent', 'All sectors']:
                keys = [k for k in teachers if k[0] == year and (region == 'Australia' or k[1] == region) and (sector == 'All sectors' or k[2] == sector)]
                assert keys
                t, s = sum(teachers[k] for k in keys), sum(students[k] for k in keys)
                rows.append({'year': year, 'state': region, 'sector': sector, 'teacher_fte': round(float(t), 1), 'student_fte': round(float(s), 1)})
    write('workforce.csv', rows)
    ratios = []
    for r in records('abs_53a.xlsx', 'Table 1 Data table'):
        sector = clean(r['C']).title().replace('All Affiliations', 'All sectors')
        ratios.append({'year': int(r['A']), 'state': state(r['B']), 'sector': sector, 'level': clean(r['D']).title(), 'ratio': float(r['E'])})
    assert len({(r['year'], r['state'], r['sector'], r['level']) for r in ratios}) == len(ratios)
    write('ratios.csv', ratios)
    map_values=[]
    for r in rows:
        if r['state']=='Australia':continue
        published=next(x for x in ratios if x['year']==r['year'] and x['state']==r['state'] and x['sector']==r['sector'] and x['level']=='All Levels')
        map_values.append({**r,'ratio':published['ratio'],'key':f"{r['state']}|{r['year']}|{r['sector']}"})
    write('map_values.csv',map_values)
    # Compare rounded published ratios with compatible FTE sums. Ratios are not averaged.
    differences = []
    for r in rows:
        published = next(x for x in ratios if x['year'] == r['year'] and x['state'] == r['state'] and x['sector'] == r['sector'] and x['level'] == 'All Levels')
        diff = abs(r['student_fte'] / r['teacher_fte'] - published['ratio'])
        differences.append(diff)
        assert diff < 0.055, (r, published, diff)
    parser = Tables()
    parser.feed((ROOT / 'data/raw/aitsl_national_trends.html').read_text(encoding='utf-8'))
    (OUT / 'aitsl_tables.json').write_text(json.dumps(parser.tables, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    # Explicit table and subgroup selections avoid merged-header ambiguity.
    ages = []
    for row in parser.tables[2][1:]:
        if row[0] not in ['School classroom teachers', 'Casual relief teachers']: continue
        assert len(row) == 8
        for band, value in zip(parser.tables[2][0][2:], row[2:]):
            ages.append({'group': row[0], 'age': band, 'percent': float(value.rstrip('%')), 'year': 2024, 'table': 3})
    write('age.csv', ages)
    gender=[]
    for row in parser.tables[2][1:]:
        if row[0] in ['School classroom teachers','Deployed in early childhood setting','Casual relief teachers']:
            gender.append({'group':row[0],'percent':float(row[1].rstrip('%')),'year':2024,'table':3})
    write('gender.csv',gender)
    experience=[]
    for row in parser.tables[6][1:]:
        if row[0] not in ['School classroom teachers','Casual relief teachers','Teacher workforce, overall']:continue
        assert len(row)==7
        for band,value in zip(parser.tables[6][0][1:],row[1:]):
            assert re.fullmatch(r'\d+%',value)
            experience.append({'group':row[0],'experience':band,'percent':float(value.rstrip('%')),'year':2024,'table':7})
    write('experience.csv',experience)
    # Exact percentages explicitly reported in the report's key findings.
    plain=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',(ROOT/'data/raw/aitsl_national_trends.html').read_text(encoding='utf-8')))
    assert re.search(r'71%.*?permanent.*?16%.*?casual.*?13%.*?fixed-term',plain)
    write('employment.csv',[{'arrangement':name,'percent':value,'year':2024} for name,value in [('Permanent',71),('Casual',16),('Fixed-term',13)]])
    reasons = []
    for row in parser.tables[20][1:]:
        assert len(row) == 6
        for year, value in zip(range(2020, 2025), row[1:]):
            if re.fullmatch(r'\d+%', value):
                reasons.append({'reason': row[0], 'year': year, 'percent': float(value.rstrip('%')), 'table': 21})
            elif value.strip():
                raise ValueError(('Unrecognised reported percentage', row))
    write('leaving_reasons.csv', reasons)
    hours = []
    for table_number in [22, 23, 24]:
        table = parser.tables[table_number - 1]
        block = None
        for row in table[1:]:
            if row[0] in ['During term', 'With holidays']: block = row[0]; continue
            if block == 'During term':
                assert len(row) == 6
                for year, value in zip(range(2020, 2025), row[1:]):
                    hours.append({'school': table[0][0], 'statistic': row[0], 'year': year, 'hours': float(value), 'table': table_number})
    write('working_hours.csv', hours)
    national = [r for r in rows if r['state'] == 'Australia' and r['sector'] == 'All sectors']
    first, last = national[0], national[-1]
    summary = {'teacher_fte_2025': last['teacher_fte'], 'student_fte_2025': last['student_fte'], 'teacher_growth_2006_2025_pct': (last['teacher_fte'] / first['teacher_fte'] - 1) * 100, 'student_growth_2006_2025_pct': (last['student_fte'] / first['student_fte'] - 1) * 100}
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    report = {'workforce_rows': len(rows), 'ratio_rows': len(ratios), 'teacher_leaf_rows': len(teacher_keys), 'student_leaf_rows': len(student_keys), 'aitsl_tables': len(parser.tables), 'max_ratio_rounding_difference': max(differences), 'checks': ['Unique source leaf records', 'Eight states present', 'Matched teacher/student aggregation keys', 'All 720 comparable ratios within 0.055; allows one-decimal ratio rounding and student confidentiality adjustment']}
    (ROOT / 'docs').mkdir(exist_ok=True)
    (ROOT / 'docs/data_validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    print(json.dumps(summary, indent=2))

if __name__ == '__main__': main()
