"""Validate a plan reasoned by local Codex, then update the public dashboard.

This script never calls a model or executes suggested steps. Codex supplies JSON.
"""
import argparse
from datetime import date, datetime
import json
from pathlib import Path
from zoneinfo import ZoneInfo
from urllib.parse import urlsplit
from publish_daily import ROOT, write_text
from render_signal import OWNER, render, render_plan

FIELDS = {'date', 'generated_by', 'status', 'project', 'title', 'value', 'why_now',
          'effort', 'carry_forward', 'steps', 'acceptance_checks', 'evidence', 'alternatives'}


def validate(plan, projects, today=None, catch_up=False):
    today = today or datetime.now(ZoneInfo('Asia/Hebron')).date().isoformat()
    fields = FIELDS | {'reviewed_on'} if catch_up else FIELDS
    if not isinstance(plan, dict) or set(plan) != fields:
        raise ValueError('Plan fields must match the documented schema exactly')
    planned_date = date.fromisoformat(plan['date'])
    current_date = date.fromisoformat(today)
    if catch_up:
        if planned_date >= current_date or plan['reviewed_on'] != today:
            raise ValueError('Catch-up entries need a past date and the actual current review date')
    elif planned_date != current_date:
        raise ValueError('Normal publication requires the current date')
    if plan['generated_by'] != 'Codex local' or plan['status'] != 'proposed':
        raise ValueError('Expected a current, proposed plan produced by local Codex')
    if plan['project'] not in projects or not isinstance(plan['carry_forward'], bool):
        raise ValueError('Unknown project or invalid carry_forward flag')
    for key in ('title', 'value', 'why_now', 'effort'):
        if not isinstance(plan[key], str) or not 1 <= len(plan[key].strip()) <= 1400:
            raise ValueError(f'Invalid {key}')
    for key in ('steps', 'acceptance_checks'):
        if not isinstance(plan[key], list) or not 2 <= len(plan[key]) <= 7:
            raise ValueError(f'Expected 2-7 {key}')
        if any(not isinstance(s, str) or not 1 <= len(s.strip()) <= 700 for s in plan[key]):
            raise ValueError(f'Invalid {key} entry')
    if not isinstance(plan['evidence'], list) or not 1 <= len(plan['evidence']) <= 8:
        raise ValueError('Supply 1-8 evidence items')
    selected_has_evidence = False
    for item in plan['evidence']:
        if not isinstance(item, dict) or set(item) != {'url', 'observation'}:
            raise ValueError('Invalid evidence item')
        parts = urlsplit(item['url'])
        path = parts.path.strip('/').split('/')
        if parts.scheme != 'https' or parts.netloc != 'github.com' or len(path) < 2 or path[0] != OWNER or path[1] not in projects:
            raise ValueError('Evidence must link to an inspected public project belonging to the owner')
        if not isinstance(item['observation'], str) or not 1 <= len(item['observation'].strip()) <= 1400:
            raise ValueError('Describe the observation supporting each source')
        selected_has_evidence |= path[1] == plan['project']
    if not selected_has_evidence:
        raise ValueError('The selected project needs evidence')
    if not isinstance(plan['alternatives'], list) or len(plan['alternatives']) != 2:
        raise ValueError('Compare exactly two alternatives')
    for item in plan['alternatives']:
        if not isinstance(item, dict) or set(item) != {'project', 'title', 'reason_not_selected'} or item['project'] not in projects:
            raise ValueError('Invalid alternative')
        for key in ('title', 'reason_not_selected'):
            if not isinstance(item[key], str) or not 1 <= len(item[key].strip()) <= 1400:
                raise ValueError('Invalid alternative explanation')
    if len(json.dumps(plan)) > 16000:
        raise ValueError('Plan exceeds the publication limit')
    return plan


def publish(plan, root=ROOT, today=None, catch_up=False):
    snapshot = json.loads((root / 'data/latest.json').read_text(encoding='utf-8'))
    projects = {r['name'] for r in snapshot['sources']['github']['data']}
    validate(plan, projects, today, catch_up=catch_up)
    target = root / 'plans' / (plan['date'] + '.json')
    if target.exists():
        if json.loads(target.read_text(encoding='utf-8')) != plan:
            raise ValueError('A plan is already published for this date; preserve its history')
        print('This plan is already published; no duplicate changes.')
        return
    files = {}
    if not catch_up:
        issues = [p.relative_to(root).as_posix() for p in (root / 'digests').rglob('????-??-??.md')]
        files = render(snapshot['date'], snapshot['sources'], issues, plan=plan)
    text = json.dumps(plan, ensure_ascii=False, indent=2) + '\n'
    files[f'plans/{plan["date"]}.json'] = text
    files[f'plans/{plan["date"]}.md'] = render_plan(plan)
    if not catch_up:
        files['plans/latest.json'] = text
    dates = sorted({p.stem for p in (root / 'plans').glob('????-??-??.json')} | {plan['date']}, reverse=True)
    entries = []
    for day in dates:
        entry = plan if day == plan['date'] else json.loads((root / 'plans' / (day + '.json')).read_text(encoding='utf-8'))
        suffix = f' — catch-up reviewed {entry["reviewed_on"]}' if 'reviewed_on' in entry else ''
        entries.append(f'- [{day}]({day}.md){suffix}')
    files['plans/README.md'] = '# AI planning journal\n\nPlans are proposals, not records of completed work. Catch-up entries show their actual review date.\n\n' + '\n'.join(entries) + '\n'
    for path, content in files.items():
        write_text(root / path, content)
    print(f'Published AI proposal: {plan["title"]}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True, help='JSON plan drafted by local Codex')
    parser.add_argument('--catch-up', action='store_true', help='Archive a missed past date, requiring reviewed_on=today; keep the current dashboard unchanged')
    args = parser.parse_args()
    publish(json.loads(args.input.read_text(encoding='utf-8-sig')), catch_up=args.catch_up)
