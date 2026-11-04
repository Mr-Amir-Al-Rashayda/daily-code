"""Publish a deterministic random daily batch of automated Python exercises."""
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import random
import math
import subprocess


def daily_count(today):
    # Stable across retries, with a new random target each calendar day.
    return random.Random('daily-count:' + today.isoformat()).randint(1, 12)


def generate(today, index):
    rng = random.Random(f'{today}:{index}')
    a, b = rng.randint(20, 5000), rng.randint(20, 5000)
    values = sorted(rng.sample(range(1000), 20))
    target = rng.choice(values + [-1])
    cases = [
        ('Euclidean GCD', 'Replace (a, b) with (b, a % b) until b is zero. Time: O(log(min(a, b))).',
         'def gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return abs(a)\n',
         f'assert gcd({a}, {b}) == {math.gcd(a,b)}\nassert gcd(0, 12) == 12\nassert gcd(-18, 24) == 6\n'),
        ('Binary search', 'Maintain a half-open interval [lo, hi) and discard half each step. Input must be sorted. Time: O(log n).',
         'def search(values, target):\n    lo, hi = 0, len(values)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if values[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid\n    return lo if lo < len(values) and values[lo] == target else -1\n',
         f'assert search({values!r}, {target}) == {values.index(target) if target in values else -1}\nassert search([], 5) == -1\nassert search([2, 2, 2], 2) == 0\n'),
        ('Prime factorization', 'Try divisors up to the square root of the remaining number. Divide out every matching factor. Input must be at least 2. Time: O(sqrt(n)) worst case.',
         'def factors(n):\n    result = []\n    divisor = 2\n    while divisor * divisor <= n:\n        while n % divisor == 0:\n            result.append(divisor)\n            n //= divisor\n        divisor += 1\n    if n > 1:\n        result.append(n)\n    return result\n',
         f'import math\nresult = factors({a})\nassert math.prod(result) == {a}\nassert all(p >= 2 and all(p % d for d in range(2, math.isqrt(p) + 1)) for p in result)\nassert factors(13) == [13]\nassert factors(36) == [2, 2, 3, 3]\n'),
    ]
    title, explanation, solution, checks = cases[(today.toordinal() + index - 1) % len(cases)]
    folder = Path('examples') / str(today.year)
    folder.mkdir(parents=True, exist_ok=True)
    suffix = '' if index == 1 else f'-{index:02d}'
    destination = folder / (today.isoformat() + suffix + '.py')
    if destination.exists():
        print('Already published today; nothing to change.')
        return None
    content = f'# {today}: {title}\n# Automatically generated practice example.\n# {explanation}\n\n{solution}\n{checks}'
    compile(content, str(destination), 'exec')
    exec(content, {})
    destination.write_text(content, encoding='utf-8')
    return destination, title, explanation


def publish(today):
    target = daily_count(today)
    print(f'{today}: target is {target} example commits')
    for index in range(1, target + 1):
        result = generate(today, index)
        if result is None:
            continue
        destination, title, explanation = result
        Path('README.md').write_text(
            '# Daily Code\n\n'
            'Automatically generated Python practice examples. These are automated examples, '
            'not a record of manual daily work.\n\n'
            f'## Latest example\n\n**{today} - {title} ({index}/{target})**\n\n'
            f'{explanation}\n\n[View and run the example]({destination.as_posix()})\n\n'
            'Run any example with Python 3; its assertions check the worked solution.\n\n'
            '## Schedule\n\nGitHub Actions runs daily at 07:17 UTC '
            '(09:17 in Hebron during standard time, 10:17 during daylight time). '
            'Each day has a random target of 1-12 example commits. '
            'The target and examples stay the same on retries, preventing duplicates. '
            'GitHub determines contribution-calendar colors and may delay scheduled jobs.\n\n'
            'To stop: open Actions, select Daily Python example, and disable the workflow.\n',
            encoding='utf-8')
        subprocess.run(['git', 'add', str(destination), 'README.md'], check=True)
        subprocess.run(['git', 'commit', '-m',
                        f'Add automated Python practice for {today} ({index}/{target}): {title}'],
                       check=True)


if __name__ == '__main__':
    publish(datetime.now(ZoneInfo('Asia/Hebron')).date())
