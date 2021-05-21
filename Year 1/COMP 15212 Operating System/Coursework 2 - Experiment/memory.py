import queue
import hashlib
from random import randrange
# Various implementations of caching. This file has stub implementations.

class Memory:
    '''Basic lookup'''
    def __init__(self):
        self.hit_count = 0

    def get_hit_count(self):
        return self.hit_count

    def name(self):
        return "Memory"

    def lookup(self, address):
        # This one actually has no cache, so every lookup requires a
        # memory hit.
        self.hit_count += 1
        string = str(address ^ 3).encode()
        return hashlib.md5(string).hexdigest()[:8]


class CyclicCache(Memory):
    '''Cyclic Cache'''

    def __init__(self, size=4):
        super().__init__()

    def name(self):
        return "Cyclic"

class LRUCache(Memory):
    '''LRU Cache'''
    def __init__(self, size=4):
        super().__init__()

    def name(self):
        return "LRU"

class RandomCache(Memory):
    '''Random Cache'''
    def __init__(self, size=4):
        super().__init__()

    def name(self):
        return "Random"
