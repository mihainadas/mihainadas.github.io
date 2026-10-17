"""Validate reusable media, provenance, source retention, and render references."""

import hashlib
import json
import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def local_file(root, value):
    if not isinstance(value, str) or not value.startswith('/assets/') or '..' in value.split('/'):
        raise ValueError(f"media path must be local and bounded: {value}")
    path = root / value.lstrip('/')
    if not path.is_file() or not path.resolve().is_relative_to(root.resolve()) or path.is_symlink():
        raise ValueError(f"missing or unsafe media: {value}")
    return path


def dimensions(path):
    if path.suffix == '.svg':
        svg = ET.fromstring(path.read_text(encoding='utf-8'))
        names = {node.tag.split('}')[-1] for node in svg.iter()}
        if not {'title', 'desc'}.issubset(names) or {'script', 'foreignObject', 'image'}.intersection(names):
            raise ValueError(f"SVG needs accessible, self-contained passive content: {path.name}")
        for node in svg.iter():
            for key, value in node.attrib.items():
                if key.lower().startswith('on') or re.search(r'(?:https?:|javascript:|data:|url\()', value, re.I):
                    raise ValueError(f"active or remote SVG content: {path.name}")
        size = int(svg.attrib['width']), int(svg.attrib['height'])
        if svg.attrib.get('viewBox') != f'0 0 {size[0]} {size[1]}':
            raise ValueError(f"SVG viewBox disagrees with dimensions: {path.name}")
        return size
    data = path.read_bytes()
    if data[:4] != b'RIFF' or data[8:12] != b'WEBP':
        raise ValueError(f"invalid WebP: {path.name}")
    chunk = data[12:16]
    if chunk == b'VP8X':
        return 1 + int.from_bytes(data[24:27], 'little'), 1 + int.from_bytes(data[27:30], 'little')
    if chunk == b'VP8 ' and data[23:26] == b'\x9d\x01\x2a':
        width, height = struct.unpack('<HH', data[26:30])
        return width & 0x3fff, height & 0x3fff
    if chunk == b'VP8L' and data[20] == 47:
        bits = int.from_bytes(data[21:25], 'little')
        return (bits & 0x3fff) + 1, ((bits >> 14) & 0x3fff) + 1
    raise ValueError(f"unsupported WebP header: {path.name}")


def validate_media(root=ROOT):
    catalogue = json.loads((root / '_data/media.json').read_text(encoding='utf-8'))
    if not catalogue:
        raise ValueError('media catalogue is empty')
    known_files = set()
    for asset_id, entry in catalogue.items():
        for field in ('title', 'kind', 'created', 'src', 'width', 'height', 'alt', 'caption', 'provenance', 'rights', 'usage', 'source_status'):
            if not entry.get(field):
                raise ValueError(f'{asset_id}: missing {field}')
        if entry['kind'] not in {'decorative', 'conceptual', 'evidence'}:
            raise ValueError(f'{asset_id}: unknown media kind')
        if entry['kind'] == 'evidence' and not entry.get('source_url', '').startswith('https://'):
            raise ValueError(f'{asset_id}: evidence needs an inspectable source')
        displays = [entry] + entry.get('variants', [])
        if entry.get('mobile_src'):
            displays.append({'src': entry['mobile_src'], 'width': entry['mobile_width'], 'height': entry['mobile_height']})
        for display in displays:
            path = local_file(root, display['src'])
            actual = dimensions(path)
            if actual != (display['width'], display['height']):
                # A responsive default may point to the 960-pixel derivative but
                # reserves the same 3:2 ratio as its largest intrinsic source.
                if display is not entry or not entry.get('variants') or actual[0] * display['height'] != actual[1] * display['width']:
                    raise ValueError(f'{asset_id}: dimensions disagree for {display["src"]}')
            if path.stat().st_size > 200_000:
                raise ValueError(f'{asset_id}: display asset exceeds 200 KB')
            known_files.add(path)
        if entry.get('master'):
            master = local_file(root, entry['master'])
            if hashlib.sha256(master.read_bytes()).hexdigest() != entry.get('master_sha256'):
                raise ValueError(f'{asset_id}: retained master changed; review provenance before replacing')
    for folder in ('assets/media', 'assets/editorial'):
        for path in (root / folder).glob('*'):
            if path.suffix in {'.svg', '.webp'} and path not in known_files:
                raise ValueError(f'unregistered reusable asset: {path.relative_to(root)}')
    for folder in ('_layouts', '_includes'):
        for path in (root / folder).glob('*.html'):
            for asset_id in re.findall(r'include media\.html id="([^"]+)"', path.read_text(encoding='utf-8')):
                if asset_id not in catalogue:
                    raise ValueError(f'unknown media ID in {path.name}: {asset_id}')
    return catalogue


if __name__ == '__main__':
    validate_media()
    print('media library checks passed')
