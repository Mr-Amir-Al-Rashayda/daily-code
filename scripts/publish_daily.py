"""Collect public APIs and build Daily Signal; Python standard library only."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import time
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from render_signal import OWNER, safe_url, render

ROOT = Path(__file__).resolve().parents[1]


def get_json(url):
    headers = {'User-Agent': f'Daily-Signal/1.0 (https://github.com/{OWNER}/daily-code)', 'Accept': 'application/json'}
    if urlsplit(url).hostname == 'api.github.com':
        headers['Accept'] = 'application/vnd.github+json'
        if os.environ.get('GITHUB_TOKEN'):
            headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    if urlsplit(url).hostname == 'dev.to':
        headers['Accept'] = 'application/vnd.forem.api-v1+json'
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers=headers), timeout=15) as response:
                return json.load(response)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def repositories():
    items = []
    for page in range(1, 11):
        batch = get_json(f'https://api.github.com/users/{OWNER}/repos?per_page=100&type=owner&page={page}')
        if not isinstance(batch, list):
            raise ValueError('Unexpected GitHub list')
        for item in batch:
            if not isinstance(item, dict) or not item.get('name') or 'stargazers_count' not in item:
                raise ValueError('Unexpected repository schema')
            if item.get('private') or item.get('fork') or item.get('archived'):
                continue
            items.append({k: item.get(k) for k in ('name', 'description', 'language', 'stargazers_count', 'pushed_at')})
        if len(batch) < 100:
            break
    if not items:
        raise ValueError('No public source repositories')
    return sorted(items, key=lambda x: x['name'].lower())


def hacker_news():
    ids = get_json('https://hacker-news.firebaseio.com/v0/topstories.json')
    if not isinstance(ids, list) or not ids or not all(isinstance(i, int) for i in ids[:12]):
        raise ValueError('Unexpected Hacker News index')
    def load(item_id):
        try:
            item = get_json(f'https://hacker-news.firebaseio.com/v0/item/{item_id}.json')
            if not isinstance(item, dict) or item.get('type') != 'story' or item.get('deleted') or item.get('dead'):
                return None
            if not item.get('title') or not isinstance(item.get('score'), int):
                return None
            discussion = f'https://news.ycombinator.com/item?id={item_id}'
            return {'title': item['title'], 'url': safe_url(item.get('url')) or discussion,
                    'discussion': discussion, 'score': item['score'], 'comments': item.get('descendants', 0)}
        except Exception:
            return None
    with ThreadPoolExecutor(max_workers=6) as pool:
        stories = [item for item in pool.map(load, ids[:12]) if item][:5]
    if not stories:
        raise ValueError('No readable stories')
    return stories


def dev_articles():
    items = get_json('https://dev.to/api/articles?tag=programming&top=1&per_page=5')
    if not isinstance(items, list):
        raise ValueError('Unexpected DEV list')
    result = []
    for item in items:
        if isinstance(item, dict) and item.get('title') and safe_url(item.get('url')):
            result.append({'title': item['title'], 'url': safe_url(item['url']), 'minutes': item.get('reading_time_minutes')})
    if not result:
        raise ValueError('No readable DEV articles')
    return result


def source_result(loader, previous, stamp):
    try:
        return {'status': 'live', 'fetched_at': stamp, 'data': loader()}
    except Exception as error:
        # Exception messages may contain request details; persist no raw errors.
        print(f'Source unavailable ({type(error).__name__}); checking cache.')
        if isinstance(previous, dict) and previous.get('data'):
            return {'status': 'cached', 'fetched_at': previous.get('fetched_at', 'unknown'), 'data': previous['data']}
        return {'status': 'unavailable', 'fetched_at': None, 'data': []}


def write_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(content, encoding='utf-8', newline='\n')
    temporary.replace(path)


def build(root=ROOT, now=None, refresh=False):
    from zoneinfo import ZoneInfo
    now = now or datetime.now(timezone.utc)
    day = now.astimezone(ZoneInfo('Asia/Hebron')).date().isoformat()
    archive = root / 'digests' / day[:4] / day[5:7] / f'{day}.md'
    if archive.exists() and not refresh:
        print(f'{day}: issue already exists; no duplicate refresh.')
        return
    cache = root / 'data/latest.json'
    previous = json.loads(cache.read_text(encoding='utf-8')).get('sources', {}) if cache.exists() else {}
    stamp = now.strftime('%Y-%m-%d %H:%M UTC')
    loaders = {'github': repositories, 'hacker_news': hacker_news, 'dev': dev_articles}
    with ThreadPoolExecutor(max_workers=3) as pool:
        tasks = {name: pool.submit(source_result, loader, previous.get(name), stamp) for name, loader in loaders.items()}
        sources = {name: task.result() for name, task in tasks.items()}
    if not any(s['status'] == 'live' for s in sources.values()):
        raise RuntimeError('No live sources: preserving the previous dashboard. Retry later.')
    previous_issues = sorted((root / 'digests').rglob('????-??-??.md'), reverse=True) if (root / 'digests').exists() else []
    files = render(day, sources, [p.relative_to(root).as_posix() for p in previous_issues])
    files['data/latest.json'] = json.dumps({'date': day, 'sources': sources}, ensure_ascii=False, indent=2) + '\n'
    # Write the archive last: it acts as the completed-issue marker on retries.
    archive_path = archive.relative_to(root).as_posix()
    for name, content in files.items():
        if name != archive_path:
            write_text(root / name, content)
    write_text(archive, files[archive_path])
    print(f'Built Daily Signal for {day}: ' + ', '.join(f'{k}={s["status"]}' for k, s in sources.items()))


if __name__ == '__main__':
    build(refresh=os.environ.get('DAILY_SIGNAL_REFRESH', 'false').lower() == 'true')
