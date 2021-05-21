import hashlib

# Memory lookup

class Memory:
    def __init__(self):
        self.hit_count = 0

    def get_hit_count(self):
        return self.hit_count

    def name(self):
        return "Memory"

    # This implementation is provided as a stub for a memory
    # access. Do not make assumptions about the implementation
    # here. Your code may be evaluated against a different
    # implementation. All you should assume is that making a call to
    # lookup will provide an answer.
    def lookup(self, address):
        # This one actually has no cache, so every lookup
        # requires a memory hit.
        print("Memory Access", end=" ")
        self.hit_count += 1
        string = str(address ^ 3).encode()
        return hashlib.md5(string).hexdigest()[:8]
