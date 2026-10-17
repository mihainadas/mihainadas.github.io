"""Prepare, but never purchase or publish, an inspected spoken script.

The output stays under ignored vendor/narration. No credentials are read and
no network request is made. Tables, equations and code need a human adaptation.
"""

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def chunks(text, limit=9000):
    result, current = [], ''
    for paragraph in text.strip().split('\n\n'):
        if len(paragraph) > limit:
            raise ValueError('adapt the overlong paragraph before narration')
        candidate = (current + '\n\n' + paragraph).strip()
        if len(candidate) > limit:
            result.append(current)
            current = paragraph
        else:
            current = candidate
    if current:
        result.append(current)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('post', help='repository-relative existing post')
    parser.add_argument('script', help='repository-relative, reviewed plain spoken text')
    args = parser.parse_args()
    post, script = ROOT / args.post, ROOT / args.script
    for path in (post, script):
        if not path.resolve().is_relative_to(ROOT) or path.is_symlink() or not path.is_file():
            parser.error('inputs must be real files inside this checkout')
    if post.parent != ROOT / '_posts':
        parser.error('the source must be a published post')
    spoken = script.read_text(encoding='utf-8')
    if 'synthetic voice' not in spoken.lower():
        parser.error('the spoken script must disclose the synthetic voice')
    if any(marker in spoken for marker in ('```', '{%', '| ---', '\\[', '\\(')):
        parser.error('adapt code, tables, template tags and equations for listening first')
    try:
        parts = chunks(spoken)
    except ValueError as error:
        parser.error(str(error))
    digest = hashlib.sha256(spoken.encode()).hexdigest()
    destination = ROOT / 'vendor/narration' / f'{post.stem}-{digest[:12]}'
    destination.mkdir(parents=True, exist_ok=False)
    for index, part in enumerate(parts, 1):
        request = {'model': 'elevenlabs/eleven-v4', 'input': part, 'voice': 'george', 'response_format': 'mp3'}
        (destination / f'{index:03d}-request.json').write_text(json.dumps(request, ensure_ascii=False, indent=2) + '\n')
    manifest = {'status': 'prepared-not-generated', 'source': args.post,
                'source_sha256': hashlib.sha256(post.read_bytes()).hexdigest(),
                'script_sha256': digest, 'characters': sum(map(len, parts)),
                'requests': len(parts), 'model': 'elevenlabs/eleven-v4', 'voice': 'george'}
    (destination / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Prepared {len(parts)} request(s), {manifest["characters"]} characters. No network or spending.')
    print(destination.relative_to(ROOT))


if __name__ == '__main__':
    main()
