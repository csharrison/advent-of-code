from enum import Enum
from operator import itemgetter

def compute_load(rocks, dimensions):
    num_rows = dimensions[1]
    return sum(num_rows - y for x, y in rocks)

def find_rocks(lines):
    moveable = set()
    unmoveable = set()
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == "O":
                moveable.add((x, y))
            elif c == "#":
                unmoveable.add((x, y))
    return moveable, unmoveable

class Direction(Enum):
    NORTH = 1
    WEST = 2
    SOUTH = 3
    EAST = 4

def move(x, y, direction: Direction, dimensions):
    newx, newy = x, y
    if direction == Direction.NORTH:
        newy -= 1
    elif direction == Direction.SOUTH:
        newy += 1
    elif direction == Direction.WEST:
        newx -= 1
    elif direction == Direction.EAST:
        newx += 1
    
    if newx < 0 or newx >= dimensions[0] or newy < 0 or newy >= dimensions[1]:
        return x, y
    return newx, newy

def sort_by_dir(items, direction: Direction):
    if direction == Direction.NORTH:
        return sorted(items, key=itemgetter(1))
    if direction == Direction.SOUTH:
        return sorted(items, key=itemgetter(1), reverse=True)
    if direction == Direction.WEST:
        return sorted(items, key=itemgetter(0))
    if direction == Direction.EAST:
        return sorted(items, key=itemgetter(0), reverse=True)

def tilt(dir: Direction, moveable, unmoveable, dimensions):
    new_moveable = set()
    for x, y in sort_by_dir(moveable, dir):
        while True:
            newx, newy = move(x, y, dir, dimensions)
            if x == newx and y == newy or (newx, newy) in unmoveable or (newx, newy) in new_moveable:
                break
            x, y = newx, newy
        new_moveable.add((x, y))
    return new_moveable

def spin(rocks, immovable, dims):
    # north, west, south, east
    rocks = tilt(Direction.NORTH, rocks, immovable, dims)
    rocks = tilt(Direction.WEST, rocks, immovable, dims)
    rocks = tilt(Direction.SOUTH, rocks, immovable, dims)
    rocks = tilt(Direction.EAST, rocks, immovable, dims)
    return tuple(rocks)

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = [list(l.strip()) for l in f.readlines()]
        dims = (len(lines[0]), len(lines))
        rocks, immovable = find_rocks(lines)
        idx_map = {}
        n = 1_000_000_000
        i = 0
        while i < n:
            rocks = spin(rocks, immovable, dims)
            if rocks in idx_map:
                idx = idx_map[rocks]
                loop = i - idx
                i += loop * ((n - i) // loop)
            else:
                idx_map[rocks] = i
            i += 1
        print(compute_load(rocks, dims))


