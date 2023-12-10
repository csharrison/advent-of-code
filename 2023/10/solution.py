from enum import Enum

class Connection(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

ALL_DIRS = [Connection.UP, Connection.DOWN, Connection.LEFT, Connection.RIGHT]

def opposite_dir(dir):
    if dir == Connection.UP: return Connection.DOWN
    if dir == Connection.DOWN: return Connection.UP
    if dir == Connection.RIGHT: return Connection.LEFT
    if dir == Connection.LEFT: return Connection.RIGHT

PIPES = {
    '|': [Connection.UP, Connection.DOWN],
    '-': [Connection.LEFT, Connection.RIGHT],
    'L': [Connection.UP, Connection.RIGHT],
    'J': [Connection.UP, Connection.LEFT],
    '7': [Connection.DOWN, Connection.LEFT],
    'F': [Connection.DOWN, Connection.RIGHT],
    'S': ALL_DIRS,
    '.': []
}

def in_bounds(cell, lines):
    x, y = cell
    if x < 0 or x >= len(lines[0]):
        return False
    if y < 0 or y >= len(lines):
        return False
    return True

def is_adjacent(cell1, cell2, lines):
    x1, y1 = cell1
    x2, y2 = cell2

    if not in_bounds(cell1, lines) or not in_bounds(cell2, lines):
        return False

    char1 = lines[y1][x1]
    char2 = lines[y2][x2]

    assert x1 == x2 or y1 == y2
    direction = None
    if x1 == x2:
        direction = Connection.UP if y1 > y2 else Connection.DOWN
    elif y1 == y2:
        direction = Connection.LEFT if x1 > x2 else Connection.RIGHT

    return direction in PIPES[char1] and opposite_dir(direction) in PIPES[char2]


def find_start(lines):
    for y, l in enumerate(lines):
        if 'S' in l:
            x = l.index('S')
            return x, y
    assert False


def get_loop(start, lines):
    curx, cury = start
    loop = [start]
    while True:
        candidates = [(curx - 1, cury), (curx + 1, cury), (curx, cury - 1), (curx, cury + 1)]
        for c in candidates:
            if is_adjacent((curx, cury), c, lines):
                if c == start and len(loop) > 2:
                    return loop
                elif len(loop) >= 2 and c == loop[-2]: continue
                curx, cury = c
                loop.append(c)
                break

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()
        x, y = find_start(lines)
        loop = get_loop((x, y), lines)


        connect_down = ['|', 'F', '7']
        connect_up = ['|', 'J', 'L']
        start_connects_down = (x, y - 1) in loop and lines[y - 1][x] in connect_up
        if start_connects_down:
            connect_down.append('S')

        print(len(loop) / 2)

        loop_set = set(loop)
        in_loop = 0
        for y, line in enumerate(lines):
            num_crosses = 0
            for x, char in enumerate(line):
                if (x, y) not in loop_set:
                    is_in_loop = 1 if num_crosses % 2 == 1 else 0
                    in_loop += is_in_loop
                elif char in connect_down:
                    num_crosses += 1
        print(in_loop)



                    





