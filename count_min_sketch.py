#!/usr/bin/env python3
"""count_min_sketch — Probabilistic frequency estimation. Zero deps."""
import hashlib, math

class CountMinSketch:
    def __init__(self, width=1000, depth=5):
        self.width, self.depth = width, depth
        self.table = [[0]*width for _ in range(depth)]
        self.total = 0

    def _hashes(self, item):
        for i in range(self.depth):
            h = int(hashlib.md5(f"{i}:{item}".encode()).hexdigest(), 16)
            yield i, h % self.width

    def add(self, item, count=1):
        self.total += count
        for row, col in self._hashes(item):
            self.table[row][col] += count

    def estimate(self, item):
        return min(self.table[row][col] for row, col in self._hashes(item))

    def merge(self, other):
        r = CountMinSketch(self.width, self.depth)
        for i in range(self.depth):
            for j in range(self.width):
                r.table[i][j] = self.table[i][j] + other.table[i][j]
        r.total = self.total + other.total
        return r

def main():
    import random; random.seed(42)
    cms = CountMinSketch(width=500, depth=5)
    # Zipf-like distribution
    freqs = {}
    for _ in range(100000):
        item = f"item_{random.randint(0, 999)}"
        cms.add(item)
        freqs[item] = freqs.get(item, 0) + 1
    print("Count-Min Sketch (w=500, d=5, 100K inserts):\n")
    top = sorted(freqs.items(), key=lambda x: -x[1])[:10]
    print(f"  {'Item':<12} {'Actual':>8} {'Estimate':>10} {'Error':>8}")
    for item, actual in top:
        est = cms.estimate(item)
        print(f"  {item:<12} {actual:>8} {est:>10} {est-actual:>+8}")
    mem = cms.width * cms.depth * 8
    print(f"\n  Memory: {mem//1024}KB, Total items: {cms.total}")

if __name__ == "__main__":
    main()
