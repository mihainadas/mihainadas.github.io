"""Keep public career evidence, business routing, and the downloadable resume honest."""

import hashlib
import json
import re
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
RESUME_INPUTS = {'_data/profile.json', 'scripts/render_resume.py', 'assets/media-sources/manrope.ttf'}


def validate_professional(root=ROOT):
    profile = json.loads((root / '_data/profile.json').read_text(encoding='utf-8'))
    reviewed = date.fromisoformat(profile['reviewed'])
    today = datetime.now(ZoneInfo('Europe/Bucharest')).date()
    if reviewed > today:
        raise ValueError('professional review date is in the future')
    if (today - reviewed).days > 90:
        print(f'::warning::Professional record needs a factual review; last reviewed {reviewed}. Do not auto-refresh the date.')
    if not profile['contact_url'].startswith('https://') or not profile['boundary']:
        raise ValueError('professional contact or responsibility boundary missing')
    now = (root / '_data/now.yml').read_text(encoding='utf-8')
    roles = []
    for role in profile['experience']:
        if not all(role.get(key) for key in ('title', 'organization', 'period', 'source', 'detail')) or not role['source'].startswith('https://'):
            raise ValueError('career role lacks a date, factual description, or public source')
        if role['current']:
            roles.append((role['title'], role['organization']))
    expected = re.findall(r'- title: (.+)\n\s+organization: (.+)', now)
    if roles != expected:
        raise ValueError('resume current roles disagree with the About/current-work record')
    if not any('In progress' in item['status'] for item in profile['education']):
        raise ValueError('ongoing doctorate must not be presented as an awarded degree')
    for group in ('education', 'publications', 'evidence', 'identities'):
        for item in profile[group]:
            url = item.get('source', item.get('url', ''))
            if not url.startswith(('https://', '/')):
                raise ValueError(f'{group}: unsupported source or destination')
    # The profile may cite local pages and dated posts, but not an invented
    # download, a private route, or a page that disappeared from the source tree.
    local_routes = set()
    for source in root.glob('*.md'):
        match = re.search(r'^permalink: (/.+?)\s*$', source.read_text(encoding='utf-8'), re.M)
        if match:
            local_routes.add(match.group(1))
    for post in (root / '_posts').glob('*.md'):
        local_routes.add('/' + post.stem[:10].replace('-', '/') + '/' + post.stem[11:] + '.html')
    for item in profile['evidence']:
        if item['url'].startswith('/') and item['url'] not in local_routes:
            raise ValueError('professional evidence does not resolve to a public source page')
    business = json.loads((root / '_data/business.json').read_text(encoding='utf-8'))
    slugs = {path.stem[11:] for path in (root / '_posts').glob('*.md')}
    if len({theme['id'] for theme in business['themes']}) != len(business['themes']):
        raise ValueError('duplicate business theme ID')
    for theme in business['themes']:
        if not theme['posts'] or not set(theme['posts']).issubset(slugs):
            raise ValueError(f'business evidence does not resolve: {theme["id"]}')
    strategy = json.loads((root / '_data/strategy.json').read_text(encoding='utf-8'))
    if not all(strategy.get(key) for key in ('name', 'thesis', 'basis', 'source')) or not strategy['source'].startswith('https://'):
        raise ValueError('strategy thread needs a stated basis and primary source')
    connections = strategy['connections']
    if len({item['slug'] for item in connections}) != len(connections):
        raise ValueError('duplicate strategy connection')
    for item in connections:
        if item['slug'] not in slugs or not item['question'] or not item['limit']:
            raise ValueError('strategy connection needs a real article, question, and limitation')
    record = json.loads((root / '_data/resume_build.json').read_text(encoding='utf-8'))
    if record['reviewed'] != profile['reviewed'] or set(record['inputs']) != RESUME_INPUTS:
        raise ValueError('resume build record does not describe the current profile and inputs')
    for name, expected in record['inputs'].items():
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f'downloadable resume is stale: regenerate after changing {name}')
    pdf = root / 'assets/downloads/mihai-nadas-resume.pdf'
    if hashlib.sha256(pdf.read_bytes()).hexdigest() != record['pdf_sha256'] or not pdf.read_bytes().startswith(b'%PDF-'):
        raise ValueError('resume PDF is missing, corrupt, or differs from its reviewed build')
    for name in ('profile', 'business', 'media', 'strategy'):
        text = (root / f'_data/{name}.json').read_text(encoding='utf-8')
        if '\u2014' in text or re.search(r'\b(?:TODO|FIXME|XXX)\b|lorem ipsum', text, re.I):
            raise ValueError(f'{name}: publication prose contains an em dash or placeholder')
    return profile


if __name__ == '__main__':
    validate_professional()
    print('professional record checks passed')
