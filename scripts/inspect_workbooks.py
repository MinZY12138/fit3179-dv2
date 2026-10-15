"""Read source XLSX XML with Python's standard library (no workbook changes)."""
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import re

ROOT = Path(__file__).resolve().parents[1]
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def sheets(path):
    with ZipFile(path) as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            strings = [''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        relationships = {e.attrib['Id']: e.attrib['Target'] for e in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        for sheet in ET.fromstring(z.read('xl/workbook.xml')).find('m:sheets', NS):
            target = relationships[sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
            member = target.lstrip('/') if target.startswith('/') else 'xl/' + target
            rows = []
            for row in ET.fromstring(z.read(member)).findall('.//m:sheetData/m:row', NS):
                cells = {}
                for cell in row:
                    value = cell.find('m:v', NS)
                    text = value.text if value is not None else ''
                    if cell.attrib.get('t') == 's':
                        text = strings[int(text)]
                    elif cell.attrib.get('t') == 'inlineStr':
                        text = ''.join(cell.find('m:is', NS).itertext())
                    if text:
                        cells[re.sub(r'\d', '', cell.attrib['r'])] = text
                if cells:
                    rows.append((int(row.attrib['r']), cells))
            yield sheet.attrib['name'], rows

if __name__ == '__main__':
    for path in sorted((ROOT / 'data/raw').glob('*.xlsx')):
        print('\nWORKBOOK', path.name)
        for name, rows in sheets(path):
            print('SHEET', name, 'nonempty rows', len(rows))
            for number, cells in rows[:20]:
                print(number, cells)
