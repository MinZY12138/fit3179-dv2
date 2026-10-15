"""Fetch the same pinned runtime used by the page, for local headless checks."""
from pathlib import Path
from urllib.request import urlopen
ROOT = Path(__file__).resolve().parents[1]
target = ROOT / '.qa'
target.mkdir(exist_ok=True)
for package, version, name in [('vega', '5.33.0', 'vega.min.js'), ('vega-lite', '5.23.0', 'vega-lite.min.js'), ('vega-embed', '6.26.0', 'vega-embed.min.js')]:
    with urlopen(f'https://cdn.jsdelivr.net/npm/{package}@{version}/build/{name}', timeout=40) as response:
        content = response.read()
    (target / name).write_bytes(content)
    print(name, len(content), 'bytes')
