"""Read the single production origin shared by Jekyll and generated assets."""

import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def canonical_origin(root=ROOT):
    text = (root / '_config.yml').read_text(encoding='utf-8')
    values = re.findall(r'^url:[ \t]*(.*)$', text, re.M)
    if len(values) != 1:
        raise ValueError('production site.url must declare one bare HTTPS origin')
    value = values[0].strip().strip('\"\'')
    parts = urlsplit(value)
    if (parts.scheme != 'https' or not parts.hostname or parts.username or parts.password
            or parts.port or parts.path not in ('', '/') or parts.query or parts.fragment
            or any(character.isspace() for character in value)):
        raise ValueError('production site.url must be a bare HTTPS origin')
    return value.rstrip('/')
