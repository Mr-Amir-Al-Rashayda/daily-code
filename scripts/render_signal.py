"""Render link-safe Markdown and accessible SVGs without third-party services."""
from collections import Counter
from datetime import date
from html import escape
from pathlib import Path
import re
from urllib.parse import quote, urlsplit

OWNER = 'Mr-Amir-Al-Rashayda'


def safe_url(value):
    value = str(value or '')
    parts = urlsplit(value)
    if parts.scheme != 'https' or not parts.hostname or parts.username:
        return ''
    return quote(value, safe=':/?=&%#@+,-._~')


def md(value):
    text = escape(re.sub(r'\s+', ' ', str(value or '')).strip(), quote=False)
    return re.sub(r'([\\`*_\[\]|])', r'\\\1', text)


def repo_url(name):
    return f'https://github.com/{OWNER}/{quote(name, safe="")}'


def language_chart(repos):
    counts = Counter(r['language'] for r in repos if r.get('language'))
    rows = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
    colors = ['#5eead4', '#60a5fa', '#c4b5fd', '#fbbf24', '#fb7185', '#a3e635']
    height = 115 + len(rows) * 43
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" viewBox="0 0 960 {height}" role="img" aria-labelledby="title desc">',
           '<title id="title">Public repository language mix</title>',
           '<desc id="desc">Repositories grouped by primary language, not lines of code.</desc>',
           f'<rect width="960" height="{height}" rx="20" fill="#0d1526"/>',
           '<text x="32" y="42" fill="#e2e8f0" font-family="sans-serif" font-size="22" font-weight="700">THE STACK</text>',
           '<text x="32" y="68" fill="#94a3b8" font-family="sans-serif" font-size="14">Public source repositories by primary language · not code volume</text>']
    for i, (language, count) in enumerate(rows):
        y = 99 + i * 43
        width = round(count / max(counts.values()) * 570)
        svg += [f'<text x="32" y="{y+16}" fill="#cbd5e1" font-family="sans-serif" font-size="15">{escape(language)}</text>',
                f'<rect x="215" y="{y}" width="{width}" height="22" rx="6" fill="{colors[i % len(colors)]}"/>',
                f'<text x="820" y="{y+16}" fill="#cbd5e1" font-family="sans-serif" font-size="14">{count} · {count/sum(counts.values()):.0%}</text>']
    if not rows:
        svg += ['<text x="32" y="100" fill="#94a3b8" font-family="sans-serif" font-size="14">Language data is temporarily unavailable.</text>']
    return '\n'.join(svg + ['</svg>']) + '\n'


def banner(day, count):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="280" viewBox="0 0 960 280" role="img" aria-labelledby="title desc">
<title id="title">Daily Signal — Amir Al-Rashayda</title><desc id="desc">An automated daily developer briefing and project observatory.</desc>
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#0c1629"/><stop offset="1" stop-color="#102b36"/></linearGradient></defs>
<rect width="960" height="280" rx="22" fill="url(#bg)"/>
<path d="M600 200h40l20-60 28 90 30-135 28 105h100" fill="none" stroke="#5eead4" stroke-width="3" opacity=".65"/>
<circle cx="900" cy="44" r="5" fill="#5eead4"/>
<text x="40" y="48" fill="#5eead4" font-family="monospace" font-size="13" letter-spacing="3">AMIR AL-RASHAYDA / DEVELOPER OBSERVATORY</text>
<text x="37" y="122" fill="#f1f5f9" font-family="sans-serif" font-size="62" font-weight="800">Daily Signal</text>
<text x="40" y="161" fill="#94a3b8" font-family="sans-serif" font-size="18">Build. Learn. Find the next idea.</text>
<text x="40" y="231" fill="#cbd5e1" font-family="monospace" font-size="15">{day}   /   {count} PUBLIC PROJECTS   /   3 API SOURCES</text>
</svg>
'''


def render_plan(plan):
    lines = ['## AI next move', '', f'**Reviewed {md(plan["date"])} by local Codex · Proposed, not implemented**', '',
             f'### {md(plan["title"])}', '', f'**Project:** [{md(plan["project"])}]({repo_url(plan["project"])}) · **Estimated effort:** {md(plan["effort"])}', '',
             md(plan['value']), '', '**Why this next:** ' + md(plan['why_now']), '']
    if plan['carry_forward']:
        lines += ['*Carried forward after reviewing the previous recommendation.*', '']
    lines += ['**Implementation outline**', ''] + [f'{i}. {md(step)}' for i, step in enumerate(plan['steps'], 1)]
    lines += ['', '**Acceptance checks**', ''] + [f'- [ ] {md(check)}' for check in plan['acceptance_checks']]
    lines += ['', '**Evidence inspected**', ''] + [f'- [Source {i}]({safe_url(e["url"])}): {md(e["observation"])}' for i, e in enumerate(plan['evidence'], 1)]
    lines += ['', '**Other ideas considered**', ''] + [f'- **{md(a["project"])} — {md(a["title"])}:** {md(a["reason_not_selected"])}' for a in plan['alternatives']]
    return '\n'.join(lines) + '\n'


def render(day, sources, previous_issues, plan=None):
    repos = sources['github']['data']
    projects = [r for r in repos if r['name'].lower() not in ('daily-code', OWNER.lower())]
    ordinal = date.fromisoformat(day).toordinal()
    body = [render_plan(plan), ''] if plan else []
    body += ['## Project spotlight', '']
    if projects:
        p = projects[ordinal % len(projects)]
        body += [f'### [{md(p["name"])}]({repo_url(p["name"])})', '',
                 md(p.get('description') or 'Explore the source and documentation for this project.'), '',
                 f'**Stack:** {md(p.get("language") or "Not reported")} · **Stars:** {p["stargazers_count"]}', '']
    else:
        body += ['Project data is temporarily unavailable.', '']
    candidates = [p for p in projects if not p.get('description')]
    if candidates:
        p = candidates[ordinal % len(candidates)]
        body += ['## One small portfolio improvement', '',
                 f'Add a one-line description to [{md(p["name"])}]({repo_url(p["name"])}). '
                 'Explain the problem it solves and its main technology. This is a suggestion; no changes were made to that project.', '']
    body += ['## Around the developer community', '', 'Top Hacker News stories at collection time. Community links, not endorsements.', '']
    for item in sources['hacker_news']['data']:
        body += [f'- [{md(item["title"])}]({safe_url(item["url"])}) — {item["score"]} points · [{item["comments"]} comments]({safe_url(item["discussion"])})']
    if not sources['hacker_news']['data']:
        body += ['Hacker News is temporarily unavailable.']
    body += ['', '## Read & learn', '', 'Popular programming articles on DEV. Original articles stay with their authors.', '']
    for item in sources['dev']['data']:
        minutes = f' · {item["minutes"]} min read' if isinstance(item.get('minutes'), int) else ''
        body += [f'- [{md(item["title"])}]({safe_url(item["url"])}){minutes}']
    if not sources['dev']['data']:
        body += ['DEV is temporarily unavailable.']
    health = ['## Source freshness', '', '| Source | Status | Last successful fetch (UTC) |', '| :-- | :-- | :-- |']
    health += [f'| {name} | {s["status"]} | {s["fetched_at"] or "—"} |' for name, s in sources.items()]
    content = '\n'.join(body + ['', *health, '', '*Generated automatically. Cached sources may contain older information.*', ''])
    archive_path = f'digests/{day[:4]}/{day[5:7]}/{day}.md'
    issues = sorted(set(previous_issues + [archive_path]), reverse=True)
    readme = f'''<p align="center"><img src="assets/banner.svg" alt="Daily Signal — Amir Al-Rashayda" width="960"></p>

<p align="center"><strong>A living developer journal. Public APIs in, useful daily signals out.</strong></p>
<p align="center"><a href="digests/README.md">Daily issues</a> · <a href="plans/README.md">AI planning journal</a> · <a href="data/latest.json">Open data</a> · <a href="https://github.com/{OWNER}">My GitHub</a></p>

[Open today's full issue →]({archive_path})

''' + '\n'.join(body) + '''

## My public project mix

<img src="assets/languages.svg" alt="Public source repositories grouped by primary language, not code volume" width="960">

''' + '\n'.join(health) + '''

## How it works

GitHub Actions runs daily at **07:17 UTC** (09:17 in Hebron during standard time; 10:17 during daylight time). Python collects public repository metadata, Hacker News stories, and DEV programming articles, then builds this README, accessible SVG graphics, a JSON snapshot, and a dated Markdown issue.

Updates contain real source data. An issue is generated at most once per date. Each API is fetched independently with timeouts and retries. If an API fails, its last successful snapshot is marked **cached**. If every API fails, the existing dashboard is preserved and the run fails visibly. GitHub may delay scheduled runs. The previous random commit batches have been replaced by one useful daily briefing.

### Run it yourself

```sh
python3 scripts/publish_daily.py
python3 -m unittest discover -s tests -v
```

Python 3.10+ and an IANA timezone database are required (included on GitHub's Ubuntu runner). Windows users may need `pip install tzdata`. No paid APIs or external API keys are required. The workflow uses its built-in token only for GitHub requests and pushing to this repository.

### Local AI planner

Local Codex reviews real project documentation and code, compares three possible tasks, and publishes one evidence-backed recommendation with an implementation outline and acceptance checks. It reads the planning journal before deciding, so an unfinished useful task can be carried forward instead of inventing a new one every day. Proposals are dated and never presented as completed work.

The AI review runs daily at **10:00 Asia/Hebron** through a local Codex scheduled task. **This computer must be awake and Codex running.** It uses the existing Codex session, with no separate model API key. The GitHub-hosted daily brief continues independently. If the local planner misses a run, the last proposal keeps its original review date. See [PLANNER.md](PLANNER.md) for the procedure and publication format.

**API references:** [GitHub](https://docs.github.com/en/rest/repos/repos), [Hacker News](https://github.com/HackerNews/API), [DEV / Forem](https://developers.forem.com/api).

**Controls:** Run the workflow manually from Actions; check its refresh option to rebuild today's issue after recovering an API. Disable the workflow there to stop updates. Other projects are only read; portfolio suggestions do not edit them. The original Python exercises remain in [examples/](examples/).
'''
    index = '# Daily Signal archive\n\nDaily API snapshots. Source freshness is recorded in each issue.\n\n'
    index += '\n'.join(f'- [{Path(p).stem}]({p.removeprefix("digests/")})' for p in issues) + '\n'
    return {'README.md': readme, archive_path: f'# Daily Signal · {day}\n\n' + content,
            'digests/README.md': index, 'assets/banner.svg': banner(day, len(repos)),
            'assets/languages.svg': language_chart(repos)}
