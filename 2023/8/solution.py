import re
from collections import defaultdict, deque
import math

def direction_gen(directions):
    dirs = [0 if d == 'L' else 1 for d in directions.strip()]
    while True:
        for d in dirs:
            yield d

def parse_line(line, m):
    groups = re.match("([0-9A-Z]*) = \(([0-9A-Z]*), ([0-9A-Z]*)\)", line).groups()
    m[groups[0]] = (groups[1], groups[2])

def parse_file(lines):
    directions = lines[0]
    map = {}
    for line in lines[2:]:
        parse_line(line, map)
    return map, directions

def navigate(directions, map):
    cur_location = "AAA"
    num_steps = 0
    for idx in direction_gen(directions):
        cur_location = map[cur_location][idx]
        num_steps += 1
        if cur_location == "ZZZ":
            return num_steps


def navigate2(directions, map):
    cur_locations = [k for k in map.keys() if k.endswith('A')]
    num_steps = 0

    # Map from a Z location to the first time step it was spotted
    first_zs = {}
    # Map from a Z location to its period (i.e. how many steps before it loops)
    loops = {}

    loc_loops = [set() for k in cur_locations]
    for idx in direction_gen(directions):
        relative_step = num_steps % len(directions)
        for i, c in enumerate(cur_locations):
            new_loc = map[c][idx]
            cur_locations[i] = new_loc
        num_steps += 1

        for i, c in enumerate(cur_locations):
            if c.endswith('Z'):
                if c not in first_zs:
                    first_zs[c] = num_steps
                elif c not in loops:
                    first = first_zs[c]
                    loops[c] = num_steps - first
                    loc_loops[i].add(c)

        if all(len(s) > 0 for s in loc_loops):
            return math.lcm(*loops.values())

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()
        map, dir = parse_file(lines)
        print(navigate(dir, map))
        print(navigate2(dir, map))
