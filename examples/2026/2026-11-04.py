# 2026-11-04: Binary search
# Automatically generated practice example.
# Maintain a half-open interval [lo, hi) and discard half each step. Input must be sorted. Time: O(log n).

def search(values, target):
    lo, hi = 0, len(values)
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo if lo < len(values) and values[lo] == target else -1

assert search([1, 42, 49, 79, 97, 98, 138, 185, 227, 330, 387, 505, 518, 554, 574, 599, 648, 794, 849, 871], 387) == 10
assert search([], 5) == -1
assert search([2, 2, 2], 2) == 0
