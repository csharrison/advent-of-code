from collections import defaultdict
import heapq
import math

CARDINAL_DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

def in_bounds(loc, lines):
    x, y = loc
    return x >= 0 and x < len(lines[0]) and y >= 0 and y < len(lines)

def next_cells(loc, cur_dir, step, lines, step_limits):
    step_min, step_max = step_limits
    for dx, dy in CARDINAL_DIRS:
        new_loc = (loc[0] + dx, loc[1] + dy)
        # can't go off the edge or backtrack
        if not in_bounds(new_loc, lines) or cur_dir == (-dx, -dy): 
            continue

        new_cost = int(lines[new_loc[1]][new_loc[0]])
        if cur_dir == (dx, dy) and step < step_max:
            yield (new_cost, new_loc, (dx, dy), step + 1)
        
        # step == 0 only for the first iteration, when we can go
        # in any direction.
        if cur_dir != (dx, dy) and (step >= step_min or step == 0):
            yield (new_cost, new_loc, (dx, dy), 1)

def navigate(lines, step_limits):
    queue = []
    end = (len(lines[0]) - 1, len(lines) - 1)
    cur_cost, cur, cur_dir, step = 0, (0, 0), (0, 0), 0
    visited = defaultdict(lambda: math.inf)
    while cur != end:
        for cost, loc, dir, new_step in next_cells(cur, cur_dir, step, lines, step_limits):
            new_cost = cost + cur_cost
            if visited[(loc, dir, new_step)] > new_cost:
                visited[(loc, dir, new_step)] = new_cost
                heapq.heappush(queue, (new_cost, loc, dir, new_step))
        cur_cost, cur, cur_dir, step = heapq.heappop(queue)
    return cur_cost

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = tuple(l.strip() for l in f.readlines())
        print(navigate(lines, (1, 3)))
        print(navigate(lines, (4, 10)))