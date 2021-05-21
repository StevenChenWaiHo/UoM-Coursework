from memory import Memory

# Your implementations of the classes below should
# not include any additional print statements.


class CyclicCache(Memory):
    def name(self):
        return "Cyclic"

    # Edit the code below to provide an implementation of a cache that
    # uses a cyclic caching strategy with a cache size of 4. You can
    # use additional methods and variables as you see fit as long as you
    # provide a suitable overridding of the lookup method.

    def __init__(self):
        super().__init__()
        self.size = 4
        self.cacheAddress = [None] * self.size
        self.cacheValue = [None] * self.size
        self.pointer = 0

    def lookup(self, address):
        if(address in self.cacheAddress):
            return self.cacheValue[self.cacheAddress.index(address)]
        else:
            # Save Address and Value in Cache
            self.cacheAddress[self.pointer] = address
            self.cacheValue[self.pointer] = super().lookup(address)

            # Cycle around the Cache
            self.pointer = (self.pointer + 1) % self.size
            return self.cacheValue[self.cacheAddress.index(address)]


class LRUCache(Memory):
    def name(self):
        return "LRU"

    # Edit the code below to provide an implementation of a cache that
    # uses a least recently used caching strategy with a cache size of
    # 4. You can use additional methods and variables as you see fit as
    # long as you provide a suitable overridding of the lookup method.

    def __init__(self):
        super().__init__()
        self.size = 4
        self.cacheAddress = [None] * self.size
        self.cacheValue = [None] * self.size
        self.queue = [i for i in range(self.size)]

    def lookup(self, address):
        # print(self.queue)
        if(address in self.cacheAddress):

            # Move Cache Index in Queue to the back (Most Recently Used)
            # Delete the Cache Index from the Queue
            self.queue.pop(self.queue.index(self.cacheAddress.index(address)))

            # Append it at the back of the Queue
            self.queue.append(self.cacheAddress.index(address))

            return self.cacheValue[self.cacheAddress.index(address)]
        else:
            # Store Address & Value in Cache with First Index of the Queue
            LRUcacheIndex = self.queue.pop(0)

            self.cacheAddress[LRUcacheIndex] = address
            self.cacheValue[LRUcacheIndex] = super().lookup(address)

            # Append the Cache Index to the Queue
            self.queue.append(self.cacheAddress.index(address))

            return self.cacheValue[self.cacheAddress.index(address)]
