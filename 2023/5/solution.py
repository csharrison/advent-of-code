from collections import defaultdict
import cProfile

class RangeMap():
    def __init__(self, line):
        dest, source, range = (int(i) for i in line.split())
        self.source = source
        self.dest = dest
        self.range = range

    def contains(self, num):
        return num >= self.source and num < self.source + self.range
    
    def range_overlaps(self, num, length):
        return num < self.source + self.range and num + length > self.source

    def transform(self, num):
        assert self.contains(num)
        return self.dest + (num - self.source)
    
    def transform_range(self, num, length):
        # Find the overlap in the source domain
        new_start = max(self.source, num)
        new_end = min(num + length, self.source + self.range)
        new_range = new_end - new_start

        # Transform to the dest domain
        overlap = (self.transform(new_start), new_range)

        # Left
        left = None
        if num < self.source:
            left_start = min(self.source, num)
            left_end = max(self.source, num)
            left = (left_start, left_end - left_start)

        # Right
        right = None
        if num + length > self.source + self.range:
            right_start = min(self.source + self.range, num + length)
            right_end = max(self.source + self.range, num + length)
            right = (right_start, right_end - right_start)
        return overlap, left, right

class Map():
    def __init__(self, lines):
        self.ranges = [RangeMap(l) for l in lines]

    def transform(self, source_num):
        for r in self.ranges:
            if r.contains(source_num):
                return r.transform(source_num)
        return source_num
    
    def transform_range(self, position, length):
        for r in self.ranges:
            if r.range_overlaps(position, length):
                overlap, left, right = r.transform_range(position, length)
                yield overlap
                if left is not None:
                    yield from self.transform_range(*left)
                if right is not None:
                    yield from self.transform_range(*right)
                return
        yield (position, length)


def process(position, maps):
    for m in maps:
        position = m.transform(position)
    return position

def process_ranges(position_ranges, maps, i):
    for position, range in position_ranges:
        new_ranges = list(maps[i].transform_range(position, range))
        if i == len(maps) - 1:
            yield min(new_ranges)[0]
        else:
            yield from process_ranges(new_ranges, maps, i + 1)

def eval(f):
    initial_seeds = [int(s) for s in f.readline().split(': ')[1].split()]
    f.readline()

    line_chunks = []
    cur_chunk = []
    for line in f.readlines():
        if line == "\n":
            line_chunks.append(cur_chunk)
            cur_chunk = []
        else:
            cur_chunk.append(line)
    line_chunks.append(cur_chunk)
    
    maps = []
    for chunk in line_chunks:
        maps.append(Map(chunk[1:]))

    initial_pos = min(process(s, maps) for s in initial_seeds)

    seed_ranges = zip(initial_seeds[::2], initial_seeds[1::2])
    final_pos = min(process_ranges(seed_ranges, maps, 0))
    return initial_pos,final_pos


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        print(eval(f))
