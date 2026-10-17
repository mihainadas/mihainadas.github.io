"""Audio remains hidden until source, transcript and actual playback are reviewed."""

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts.check_audio import validate_audio
from scripts.prepare_narration import chunks


class AudioTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for folder in ('_data', '_posts', 'assets/transcripts'):
            (self.root / folder).mkdir(parents=True)
        post = self.root / '_posts/2026-10-17-example.md'
        post.write_text('A source fixture.')
        transcript = self.root / 'assets/transcripts/example.txt'
        transcript.write_text('This uses a synthetic voice. A spoken fixture.')
        self.episode = {'article_url': '/2026/10/17/example.html', 'source': '_posts/2026-10-17-example.md',
                        'source_sha256': hashlib.sha256(post.read_bytes()).hexdigest(),
                        'transcript': '/assets/transcripts/example.txt',
                        'transcript_sha256': hashlib.sha256(transcript.read_bytes()).hexdigest(),
                        'audio_url': 'https://example.org/episode.mp3', 'mime_type': 'audio/mpeg',
                        'bytes': 10000, 'duration_seconds': 60, 'duration_label': '1:00',
                        'voice': 'fixture', 'voice_kind': 'stock', 'listening_reviewed': '2026-10-17',
                        'listening_reviewed_by': 'Test fixture, not an actual episode'}

    def check(self, episodes=None):
        (self.root / '_data/audio.json').write_text(json.dumps({'episodes': episodes if episodes is not None else [self.episode]}))
        return validate_audio(self.root)

    def test_empty_catalogue_is_valid(self):
        self.assertEqual(self.check([]), [])

    def test_complete_record_is_valid(self):
        self.assertEqual(len(self.check()), 1)

    def test_stale_source_is_rejected(self):
        self.episode['source_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'stale'):
            self.check()

    def test_transcript_change_is_rejected(self):
        self.episode['transcript_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'transcript changed'):
            self.check()

    def test_missing_listening_review_is_rejected(self):
        self.episode['listening_reviewed_by'] = ''
        with self.assertRaisesRegex(ValueError, 'listening review'):
            self.check()

    def test_expiring_enclosure_is_rejected(self):
        self.episode['audio_url'] += '?token=not-a-secret'
        with self.assertRaisesRegex(ValueError, 'stable public'):
            self.check()

    def test_wrong_platform_is_rejected(self):
        self.episode['apple_url'] = 'https://music.apple.com/test'
        with self.assertRaisesRegex(ValueError, 'platform URL'):
            self.check()

    def test_missing_synthetic_voice_disclosure_is_rejected(self):
        transcript = self.root / 'assets/transcripts/example.txt'
        transcript.write_text('A spoken fixture without a disclosure.')
        self.episode['transcript_sha256'] = hashlib.sha256(transcript.read_bytes()).hexdigest()
        with self.assertRaisesRegex(ValueError, 'disclose'):
            self.check()

    def test_voice_cloning_is_not_silently_allowed(self):
        self.episode['voice_kind'] = 'cloned'
        with self.assertRaisesRegex(ValueError, 'stock voice'):
            self.check()

    def test_wrong_duration_is_rejected(self):
        self.episode['duration_label'] = '2:00'
        with self.assertRaisesRegex(ValueError, 'duration label'):
            self.check()

    def test_source_traversal_is_rejected(self):
        self.episode['source'] = '_posts/../_data/audio.json'
        with self.assertRaisesRegex(ValueError, 'bounded'):
            self.check()

    def test_duplicates_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            self.check([self.episode, self.episode])

    def test_script_chunking_preserves_paragraphs(self):
        self.assertEqual(chunks('abcd\n\nefgh\n\nij', 8), ['abcd', 'efgh\n\nij'])

    def test_long_paragraph_needs_adaptation(self):
        with self.assertRaises(ValueError):
            chunks('a' * 11, 10)


if __name__ == '__main__':
    unittest.main()
