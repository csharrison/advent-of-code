
from collections import defaultdict
from functools import reduce
import operator

MAX_CUBES = {
  "red": 12,
  "green": 13,
  "blue": 14
}

def parse_round(round):
  round = [r.strip().split(' ') for r in round]
  return {
    x[1]: int(x[0]) for x in round
  }

def parse_line(line: str):
  game, rounds = line.split(':')
  game_id = int(game.split(' ')[1])
  rounds = [parse_round(r.split(',')) for r in rounds.split(';')]
  return (game_id, rounds)

def game_valid(round):
  print(round)
  return all(MAX_CUBES[k] >= round[k] for k in round.keys())

def minimum_cubes_power(rounds):
  cubes = defaultdict(int)
  for r in rounds:
    for k, v in r.items():
      cubes[k] = max(cubes[k], v)
  return reduce(operator.mul, cubes.values())

if __name__ == "__main__":
  with open("input.txt", "r") as f:
    parsed = [parse_line(l) for l in f.readlines()]
    print(sum(id for id, rounds in parsed if all(game_valid(r) for r in rounds)))
    print(sum(minimum_cubes_power(rounds) for id, rounds in parsed))
