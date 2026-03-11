#!/usr/bin/env python3
"""Count-Min Sketch — probabilistic frequency estimation.

One file. Zero deps. Does one thing well.

Estimates frequency of elements in a stream using sub-linear space.
Always overestimates (never undercounts). Used in network monitoring, NLP.
"""
import hashlib, struct, math, sys

class CountMinSketch:
    def __init__(self, width=1000, depth=7):
        self.w = width
        self.d = depth
        self.table = [[0] * width for _ in range(depth)]
        self.total = 0

    @classmethod
    def from_error(cls, epsilon=0.001, delta=0.01):
        """Create with error guarantees: P(error > epsilon*N) < delta."""
        w = int(math.ceil(math.e / epsilon))
        d = int(math.ceil(math.log(1 / delta)))
        return cls(w, d)

    def _hashes(self, item):
        if isinstance(item, str): item = item.encode()
        h = hashlib.sha256(item).digest()
        h1 = struct.unpack_from('<Q', h, 0)[0]
        h2 = struct.unpack_from('<Q', h, 8)[0]
        return [(h1 + i * h2) % self.w for i in range(self.d)]

    def add(self, item, count=1):
        self.total += count
        for i, j in enumerate(self._hashes(item)):
            self.table[i][j] += count

    def query(self, item):
        return min(self.table[i][j] for i, j in enumerate(self._hashes(item)))

    def __getitem__(self, item):
        return self.query(item)

    def merge(self, other):
        assert self.w == other.w and self.d == other.d
        result = CountMinSketch(self.w, self.d)
        result.total = self.total + other.total
        for i in range(self.d):
            for j in range(self.w):
                result.table[i][j] = self.table[i][j] + other.table[i][j]
        return result

def main():
    cms = CountMinSketch.from_error(epsilon=0.001, delta=0.01)
    print(f"Count-Min Sketch (w={cms.w}, d={cms.d})\n")
    # Zipf-like distribution
    import random
    random.seed(42)
    actual = {}
    for _ in range(100000):
        # Power law: most items are rare, few are frequent
        item = f"item-{int(random.paretovariate(1))}"
        actual[item] = actual.get(item, 0) + 1
        cms.add(item)
    # Check top items
    top = sorted(actual.items(), key=lambda x: -x[1])[:10]
    print(f"{'Item':15s} {'Actual':>8s} {'Estimate':>8s} {'Error':>8s}")
    for item, count in top:
        est = cms.query(item)
        print(f"{item:15s} {count:8d} {est:8d} {est-count:+8d}")
    # Check rare items
    print(f"\nRare items (actual=1):")
    rare = [k for k, v in actual.items() if v == 1][:5]
    for item in rare:
        est = cms.query(item)
        print(f"  {item}: est={est}")
    print(f"\nTotal items: {cms.total:,}, distinct: {len(actual):,}")

if __name__ == "__main__":
    main()
