from copy import deepcopy
from datetime import datetime, timezone
import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
planner = importlib.import_module('publish_plan')
publisher = importlib.import_module('publish_daily')


def sample():
    return {'date': '2026-11-05', 'generated_by': 'Codex local', 'status': 'proposed',
            'project': 'demo', 'title': 'Add a useful report', 'value': 'Make results reproducible.',
            'why_now': 'The inspected code lacks a report.', 'effort': 'One hour', 'carry_forward': False,
            'steps': ['Add the report.', 'Document a runnable example.'],
            'acceptance_checks': ['Report matches the input.', 'Regression tests pass.'],
            'evidence': [{'url': 'https://github.com/Mr-Amir-Al-Rashayda/demo/blob/main/main.py', 'observation': 'Code inspected.'}],
            'alternatives': [{'project': 'demo', 'title': f'Alternative {i}', 'reason_not_selected': 'Lower impact.'} for i in range(2)]}


class PlannerTests(unittest.TestCase):
    def test_requires_current_date_known_project_and_real_source(self):
        planner.validate(sample(), {'demo'}, '2026-11-05')
        changes = [('date', '2025-01-01'), ('project', 'invented'), ('status', 'completed')]
        for field, value in changes:
            plan = sample()
            plan[field] = value
            with self.assertRaises(ValueError):
                planner.validate(plan, {'demo'}, '2026-11-05')
        for address in ('javascript:alert(1)', 'https://github.com/another-owner/demo', 'https://github.com/Mr-Amir-Al-Rashayda/unknown'):
            plan = sample()
            plan['evidence'][0]['url'] = address
            with self.assertRaises(ValueError):
                planner.validate(plan, {'demo'}, '2026-11-05')

    def test_publishes_preserves_history_and_survives_next_daily_render(self):
        repo = {'name': 'demo', 'language': 'Python', 'description': 'Demo', 'stargazers_count': 0}
        sources = {name: {'status': 'live', 'fetched_at': 'now', 'data': data}
                   for name, data in [('github', [repo]), ('hacker_news', []), ('dev', [])]}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'data').mkdir()
            (root / 'data/latest.json').write_text(json.dumps({'date': '2026-11-05', 'sources': sources}))
            planner.publish(sample(), root, '2026-11-05')
            before = (root / 'README.md').read_bytes()
            planner.publish(sample(), root, '2026-11-05')
            self.assertEqual(before, (root / 'README.md').read_bytes())
            replacement = sample()
            replacement['title'] = 'Rewrite history'
            with self.assertRaises(ValueError):
                planner.publish(replacement, root, '2026-11-05')
            with patch.object(publisher, 'repositories', return_value=[repo]), \
                 patch.object(publisher, 'hacker_news', return_value=[]), \
                 patch.object(publisher, 'dev_articles', return_value=[]):
                publisher.build(root, datetime(2026, 11, 6, 9, tzinfo=timezone.utc))
            text = (root / 'README.md').read_text(encoding='utf-8')
            self.assertIn('Reviewed 2026-11-05', text)
            self.assertIn('Proposed, not implemented', text)
            self.assertIn('Add a useful report', text)


if __name__ == '__main__':
    unittest.main()
