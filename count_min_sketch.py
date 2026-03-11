#!/usr/bin/env python3
"""Count-Min Sketch — frequency estimation for streaming data."""
import hashlib, sys

class CountMinSketch:
    def __init__(self, width=1000, depth=5):
        self.width, self.depth = width, depth
        self.table = [[0]*width for _ in range(depth)]
        self.total = 0
    def _hashes(self, item):
        for i in range(self.depth):
            h = int(hashlib.sha256(f"{i}:{item}".encode()).hexdigest(), 16)
            yield i, h % self.width
    def add(self, item, count=1):
        self.total += count
        for row, col in self._hashes(item): self.table[row][col] += count
    def estimate(self, item):
        return min(self.table[row][col] for row, col in self._hashes(item))
    def merge(self, other):
        for i in range(self.depth):
            for j in range(self.width):
                self.table[i][j] += other.table[i][j]
        self.total += other.total

if __name__ == "__main__":
    cms = CountMinSketch(500, 5)
    words = "the cat sat on the mat the cat".split()
    for w in words: cms.add(w)
    for w in sorted(set(words)):
        actual = words.count(w)
        print(f"  {w}: actual={actual}, estimated={cms.estimate(w)}")
    print(f"Total: {cms.total}")
