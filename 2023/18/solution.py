from enum import Enum
from operator import attrgetter

class Orientation(Enum):
    VERT = 1
    HORIZ = 2

class Segment():
    def __init__(self, start, end):
        # Sort by x then by y.
        self.s, self.e = sorted((start, end))
        self.length = (self.e[0] - self.s[0]) + (self.e[1] - self.s[1]) + 1
        self.orientation = Orientation.VERT if self.e[0] == self.s[0] else Orientation.HORIZ

    def vertical_range(self):
        return (self.s[1], self.e[1])
        
    def __eq__(self, o):
        return (self.s, self.e) == (o.s, o.e)
    
    def __hash__(self):
        return (self.s, self.e).__hash__()

def parse_line(line):
    d, n, color = line.strip().replace(')', '').replace('(', '').split()    
    dx, dy = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}[d]
    return dx, dy, int(n)

def parse_line2(line):
    color = line.strip().replace(')', '').replace('(', '').split()[-1]
    dx, dy = {"0": (1, 0), "2": (-1, 0), "3": (0, -1), "1": (0, 1)}[color[-1]]
    return dx, dy, int(color[1:-1], base=16)

def parse(lines, parse_line_func):
    return [parse_line_func(l) for l in lines]

def gen_segments(parsed):
    segments = []
    x, y = (0, 0)
    for dx, dy, n in parsed:
        new_x, new_y = x + dx * n, y + dy * n
        segments.append(Segment((x, y), (new_x, new_y)))
        x, y = new_x, new_y
    return segments

def range_overlap(r1, r2):
    begin1, end1 = r1
    begin2, end2 = r2
    overlap_begin = max(begin1, begin2)
    overlap_end = min(end1, end2)
    if overlap_begin > overlap_end:
        return None
    return (overlap_begin, overlap_end)

def del_range(r, to_delete):
    rbegin, rend = r
    dbegin, dend = to_delete
    assert dbegin >= rbegin
    assert dend <= rend

    new_ranges = []    
    if dbegin > rbegin:
        new_ranges.append((rbegin, dbegin - 1))

    if dend < rend:
        new_ranges.append((dend + 1, rend))
    
    return new_ranges

def compute_area_for_segment(v, verts, horiz_set, tainted):
    if v in tainted:
        return 0
    
    ranges = [(v.s[1], v.s[1]), (v.e[1], v.e[1])]
    if v.length > 2:
        ranges.append((v.s[1] + 1, v.e[1] - 1))
    
    area = 0
    while len(ranges):
        r = ranges.pop()
        connection = next(c for c in verts if c != v and c.s[0] > v.s[0] and range_overlap(r, c.vertical_range()) is not None)
        c_range = (connection.s[1], connection.e[1])
        overlap_range = range_overlap(r, c_range)

        length = overlap_range[1] - overlap_range[0] + 1
        width = connection.s[0] - v.s[0] + 1
        if length == 1:
            seg = Segment((v.s[0], overlap_range[0]), (connection.s[0], overlap_range[1]))
            if seg in horiz_set:
                continue
        
        new_ranges = del_range(r, overlap_range)
        area += length * (width - 2)
        ranges.extend(new_ranges)
        tainted.add(connection)
    return area


def compute_area(segments):
    verts = sorted([s for s in segments if s.orientation == Orientation.VERT], key=attrgetter('s'))    
    horiz_set = set(s for s in segments if s.orientation == Orientation.HORIZ)
    tainted = set()
    circumference = sum(s.length - 1 for s in segments)
    return circumference + sum(compute_area_for_segment(v, verts, horiz_set, tainted) for v in verts)

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()
        segments1 = gen_segments(parse(lines, parse_line))
        print(compute_area(segments1))

        segments1 = gen_segments(parse(lines, parse_line2))
        print(compute_area(segments1))