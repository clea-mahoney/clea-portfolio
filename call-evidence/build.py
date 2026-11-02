"""Embed the anonymized presentation data; no external dependencies."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
data = json.dumps(json.loads((root / 'presentation-data.json').read_text()), ensure_ascii=False)
template = (root / 'index.template.html').read_text()
for asset, token in [('app.js', '__APP_VERSION__'), ('week-engine.js', '__ENGINE_VERSION__'), ('styles.css', '__STYLE_VERSION__')]:
    template = template.replace(token, hashlib.sha256((root / asset).read_bytes()).hexdigest()[:12])
(root / 'index.html').write_text(template.replace('__PRESENTATION_DATA__', data.replace('<', '\\u003c')))

# Both fixed presentations share the same story, data, and interaction code.
candidate = template.replace('data-brand="clea"', 'data-brand="zapier"')
candidate = candidate.replace('<head>', '<head>\n<base href="../">')
brand_version = hashlib.sha256((root / 'candidate-brand.css').read_bytes()).hexdigest()[:12]
candidate = candidate.replace('</head>', f'<link rel="stylesheet" href="candidate-brand.css?v={brand_version}">\n</head>')
(root / 'candidate').mkdir(exist_ok=True)
(root / 'candidate' / 'index.html').write_text(candidate.replace('__PRESENTATION_DATA__', data.replace('<', '\\u003c')))
