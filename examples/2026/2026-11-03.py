# 2026-11-03: Euclidean GCD
# Automatically generated practice example.
# Replace (a, b) with (b, a % b) until b is zero. Time: O(log(min(a, b))).

def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

assert gcd(292, 532) == 4
assert gcd(0, 12) == 12
assert gcd(-18, 24) == 6
