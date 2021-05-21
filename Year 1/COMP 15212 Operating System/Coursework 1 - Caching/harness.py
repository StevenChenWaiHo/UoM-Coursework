import sys
import argparse
from memory import Memory
from cache import CyclicCache, LRUCache

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--strategy',
                        help='Expects one of Memory (default), LRU or Cyclic',
                        default="Memory")
    args = parser.parse_args()
    model = None
    if args.strategy == "Memory":
        model = Memory()
    elif args.strategy == "Cyclic":
        model = CyclicCache()
    elif args.strategy == "LRU":
        model = LRUCache()
    else:
        print("Unknown strategy: {}".format(args.strategy))
        sys.exit(1)

    # Reads a list of integers from the command line. No error
    # checking, so non integers will bomb out.
    count = 0
    location = sys.stdin.readline().strip()
    while(location):
        count += 1
        location = int(location)
        print("{:03d},{:2d},".format(count, location), end=" ")
        print(model.lookup(location))
        location = sys.stdin.readline().strip()
    print()
    print("Model: {}".format(model.name()))
    print("{:03d} Accesses".format(count))
    print("{:03d} Memory Hits".format(model.get_hit_count()))
