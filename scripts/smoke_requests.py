"""Very small smoke traffic generator. Not a performance benchmark."""
import argparse
import urllib.request
from collections import Counter

p = argparse.ArgumentParser()
p.add_argument('--url', default='http://127.0.0.1:8002/api/ping')
p.add_argument('--count', type=int, default=50)
a = p.parse_args()
counts = Counter()
for _ in range(a.count):
    try:
        with urllib.request.urlopen(a.url, timeout=3) as r:
            counts[r.status] += 1
    except Exception as exc:
        counts[type(exc).__name__] += 1
print(dict(counts))
