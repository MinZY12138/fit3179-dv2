"""Download immutable official source snapshots; never overwrite existing files."""
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import quote
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
SOURCES = {
    'abs_51a.xlsx': 'https://www.abs.gov.au/statistics/people/education/schools/2025/' + quote('Table 51a Full-time equivalent (FTE) in-school staff, 2006-2025.xlsx'),
    'abs_53a.xlsx': 'https://www.abs.gov.au/statistics/people/education/schools/2025/' + quote('Table 53a Full-time equivalent (FTE) student to (FTE) teaching staff ratios, 2006-2025.xlsx'),
    'abs_43a.xlsx': 'https://www.abs.gov.au/statistics/people/education/schools/2025/' + quote('Table 43a Full-time equivalent (FTE) students, 2006-2025.xlsx'),
    'aitsl_national_trends.html': 'https://www.aitsl.edu.au/resources/national-trends-teacher-workforce',
}

if __name__ == '__main__':
    RAW.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name, url in SOURCES.items():
        path = RAW / name
        if not path.exists():
            with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=60) as response:
                content = response.read()
            if name.endswith('.xlsx') and not content.startswith(b'PK'):
                raise ValueError(f'Not an Excel workbook: {url}')
            path.write_bytes(content)
        content = path.read_bytes()
        manifest.append({'file': name, 'url': url, 'bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest(), 'retrieved': '2026-10-16'})
        print(name, len(content), 'bytes')
    (RAW / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
