from copy import deepcopy
from datetime import datetime, timezone
import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from xml.etree import ElementTree

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
publisher = importlib.import_module('publish_daily')
renderer = importlib.import_module('render_signal')

REPOS = [{'name': 'sample-project', 'description': None, 'language': 'C & C++', 'stargazers_count': 2, 'pushed_at': None}]
STORIES = [{'title': 'A [link] <script> & code', 'url': 'https://example.com/a(b)', 'discussion': 'https://news.ycombinator.com/item?id=1', 'score': 5, 'comments': 2}]
ARTICLES = [{'title': 'Learning Python', 'url': 'https://dev.to/example/python', 'minutes': 4}]


class SignalTests(unittest.TestCase):
    def test_links_and_remote_text_are_escaped(self):
        self.assertEqual(renderer.safe_url('javascript:alert(1)'), '')
        self.assertEqual(renderer.safe_url('https://user:secret@example.com'), '')
        self.assertIn('%28', renderer.safe_url('https://example.com/a(b)'))
        self.assertEqual(renderer.md('[x]<script>\nhello'), r'\[x\]&lt;script&gt; hello')

    def test_failed_source_uses_original_cache_timestamp(self):
        previous = {'data': ARTICLES, 'fetched_at': 'old stamp'}
        with patch.object(publisher, 'dev_articles', side_effect=RuntimeError('offline')):
            result = publisher.source_result(publisher.dev_articles, previous, 'new stamp')
        self.assertEqual(result, {'status': 'cached', 'data': ARTICLES, 'fetched_at': 'old stamp'})
        self.assertEqual(publisher.source_result(lambda: 1 / 0, None, 'now')['status'], 'unavailable')

    def test_repository_schema_and_private_fork_filters(self):
        live = dict(REPOS[0], private=False, fork=False, archived=False)
        with patch.object(publisher, 'get_json', return_value=[live, dict(live, private=True), dict(live, fork=True)]):
            self.assertEqual(publisher.repositories(), REPOS)
        with patch.object(publisher, 'get_json', return_value={'message': 'rate limit'}):
            with self.assertRaises(ValueError):
                publisher.repositories()

    def test_svg_and_archive_rendering(self):
        sources = {name: {'data': data, 'status': 'live', 'fetched_at': 'now'}
                   for name, data in [('github', REPOS), ('hacker_news', STORIES), ('dev', ARTICLES)]}
        files = renderer.render('2026-11-05', sources, [])
        ElementTree.fromstring(files['assets/banner.svg'])
        ElementTree.fromstring(files['assets/languages.svg'])
        ElementTree.fromstring(renderer.language_chart([]))
        self.assertIn('C &amp; C++', files['assets/languages.svg'])
        self.assertNotIn('<script>', files['README.md'])
        self.assertIn('2026/11/2026-11-05.md', files['digests/README.md'])

    def test_daily_build_is_idempotent_and_caches_per_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with patch.object(publisher, 'repositories', return_value=deepcopy(REPOS)), \
                 patch.object(publisher, 'hacker_news', return_value=STORIES), \
                 patch.object(publisher, 'dev_articles', return_value=ARTICLES):
                publisher.build(root, datetime(2026, 11, 5, 9, tzinfo=timezone.utc))
            before = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            with patch.object(publisher, 'repositories', side_effect=AssertionError('should not fetch')) as loader:
                publisher.build(root, datetime(2026, 11, 5, 10, tzinfo=timezone.utc))
                loader.assert_not_called()
            self.assertEqual(before, {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file()})
            with patch.object(publisher, 'repositories', return_value=deepcopy(REPOS)), \
                 patch.object(publisher, 'hacker_news', side_effect=RuntimeError('offline')), \
                 patch.object(publisher, 'dev_articles', return_value=ARTICLES):
                publisher.build(root, datetime(2026, 11, 6, 9, tzinfo=timezone.utc))
            cached = json.loads((root / 'data/latest.json').read_text())['sources']['hacker_news']
            self.assertEqual(cached['status'], 'cached')
            self.assertEqual(cached['fetched_at'], '2026-11-05 09:00 UTC')
            before = (root / 'README.md').read_bytes()
            with patch.object(publisher, 'repositories', side_effect=RuntimeError), \
                 patch.object(publisher, 'hacker_news', side_effect=RuntimeError), \
                 patch.object(publisher, 'dev_articles', side_effect=RuntimeError):
                with self.assertRaises(RuntimeError):
                    publisher.build(root, datetime(2026, 11, 7, 9, tzinfo=timezone.utc))
            self.assertEqual((root / 'README.md').read_bytes(), before)
            self.assertFalse((root / 'digests/2026/11/2026-11-07.md').exists())


if __name__ == '__main__':
    unittest.main()
