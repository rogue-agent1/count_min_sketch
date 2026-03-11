#!/usr/bin/env python3
"""Count-Min Sketch — probabilistic frequency estimation."""
import sys, hashlib, random

class CountMinSketch:
    def __init__(self, width=1000, depth=5):
        self.w = width; self.d = depth
        self.table = [[0]*width for _ in range(depth)]
        self.seeds = [random.randint(0, 2**32) for _ in range(depth)]
    def _hash(self, item, i):
        h = hashlib.md5(f"{self.seeds[i]}:{item}".encode()).hexdigest()
        return int(h, 16) % self.w
    def add(self, item, count=1):
        for i in range(self.d):
            self.table[i][self._hash(item, i)] += count
    def estimate(self, item):
        return min(self.table[i][self._hash(item, i)] for i in range(self.d))

if __name__ == "__main__":
    cms = CountMinSketch(width=100, depth=5)
    words = "the quick brown fox the fox the the dog cat the fox brown".split()
    for w in words: cms.add(w)
    print(f"Count-Min Sketch ({len(words)} items):")
    actual = {}
    for w in words: actual[w] = actual.get(w, 0) + 1
    for w in sorted(set(words)):
        est = cms.estimate(w)
        print(f"  {w:>8s}: estimated={est}, actual={actual[w]}")
