import string
import re
import collections

def is_symbol(char):
  return not (char in '.\n' + string.digits)

def maybe_append(c: set, x, y, grid):
  if x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid):
    c.append((x,y))

def adjacent_cells(num: str, x: int, y: int, grid):
  """Returns a list of coordinate tuples for all cells adjecent to the number starting at position (x,y)"""
  length = len(num)
  adjacent = []
  maybe_append(adjacent, x - 1, y, grid)
  for xi in range(x - 1, x + length + 1):
    maybe_append(adjacent, xi, y - 1, grid)
    maybe_append(adjacent, xi, y + 1, grid)
  maybe_append(adjacent, x + length, y, grid)
  return adjacent

def parse_file(lines):
  # Map from (x,y) tuple to list of numbers
  gears = collections.defaultdict(list)
  sum = 0
  for y, line in enumerate(lines):
    x = 0
    for string in re.split('(\d+)', line):
      adjacent = adjacent_cells(string, x, y, lines)
      if string.isnumeric() and any(is_symbol(lines[yi][xi]) for (xi, yi) in adjacent):
        sum += int(string)
        for xi,yi in adjacent:
          if lines[yi][xi] == '*':
            gears[(xi,yi)].append(int(string))
      x += len(string)
  
  gear_sums = 0
  for cell, lst in gears.items():
    if len(lst) == 2:
      gear_sums += lst[0] * lst[1]
  return sum, gear_sums

if __name__ == "__main__":
  with open("input.txt", "r") as f:
    print(parse_file(f.readlines()))

