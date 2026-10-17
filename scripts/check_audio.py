"""Fail closed on stale, unreviewed, or incomplete published audio editions."""

from datetime import date
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit


def https_url(value, host=None):
    parts = urlsplit(value)
    return (parts.scheme == 'https' and bool(parts.hostname) and not parts.username
            and not parts.password and not parts.fragment
            and (host is None or parts.hostname == host))


def local_file(root, value, prefix):
    if not value.startswith(prefix) or '..' in Path(value).parts:
        raise ValueError('audio path must be local and bounded')
    path = root / value.lstrip('/')
    if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('audio source or transcript is missing or unsafe')
    return path


def validate_audio(root):
    episodes = json.loads((root / '_data/audio.json').read_text())['episodes']
    seen = set()
    for episode in episodes:
        url = episode['article_url']
        if url in seen:
            raise ValueError('duplicate audio edition')
        seen.add(url)
        post = local_file(root, episode['source'], '_posts/')
        stem = post.stem
        expected = '/' + stem[:10].replace('-', '/') + '/' + stem[11:] + '.html'
        if url != expected:
            raise ValueError('audio article URL does not match source')
        if hashlib.sha256(post.read_bytes()).hexdigest() != episode['source_sha256']:
            raise ValueError('audio edition is stale after an article change')
        transcript = local_file(root, episode['transcript'], '/assets/transcripts/')
        if hashlib.sha256(transcript.read_bytes()).hexdigest() != episode['transcript_sha256']:
            raise ValueError('spoken transcript changed after audio review')
        if 'synthetic voice' not in transcript.read_text().lower():
            raise ValueError('spoken transcript must disclose the synthetic voice')
        if not https_url(episode['audio_url']) or '?' in episode['audio_url']:
            raise ValueError('audio requires a stable public HTTPS enclosure without credentials')
        if episode['mime_type'] != 'audio/mpeg' or episode['bytes'] <= 0 or episode['duration_seconds'] <= 0:
            raise ValueError('audio media measurements must be verified')
        seconds = round(episode['duration_seconds'])
        if episode['duration_label'] != f'{seconds // 60}:{seconds % 60:02d}':
            raise ValueError('audio duration label disagrees with measured seconds')
        if not episode['voice'] or episode['voice_kind'] != 'stock':
            raise ValueError('only an authorized stock voice is supported')
        if not episode['listening_reviewed_by'] or date.fromisoformat(episode['listening_reviewed']) > date.today():
            raise ValueError('audio needs an actual, dated listening review')
        for key, host in (('spotify_url', 'open.spotify.com'), ('apple_url', 'podcasts.apple.com')):
            if episode.get(key) and not https_url(episode[key], host):
                raise ValueError('audio platform URL is invalid')
    return episodes
