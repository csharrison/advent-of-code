
from functools import reduce
import operator
import math

def parse_file(lines):
    parse_nums = lambda x: [int(i) for i in x.split(':')[1].strip().split()]
    times = parse_nums(lines[0])
    distance = parse_nums(lines[1])
    return zip(times, distance)

def parse_file2(lines):
    parse_nums = lambda x: int(x.split(':')[1].replace(" ", ""))
    time = parse_nums(lines[0])
    distance = parse_nums(lines[1])
    return (time, distance)

def compute_distance(time_holding_button, race_time):
    time_not_holding_button = race_time - time_holding_button
    return time_holding_button * time_not_holding_button

def compute_winners_naive(race_data):
    time, distance = race_data
    return sum(1 for i in range(time) if compute_distance(i, time) > distance)

def compute_winners_clever(race_data):
    race_time, distance = race_data
    # time_holding_button = T
    # race_time = r
    # Distance = D
    # T(r - T) > D
    # -T^2 + Tr > D which is a quadratic inequality
    # (T-r/2)^2 < (-4D + r^2) / 4
    # T < (1/2) sqrt(r^2 - 4D) + r/2
    # T > (-1/2) sqrt(r^2 - 4D) + r/2
    t_greater = math.ceil((-1/2) * math.sqrt(race_time**2 - 4 * distance) + race_time/2)
    t_less = math.ceil((1/2) * math.sqrt(race_time**2 - 4 * distance) + race_time/2)
    return t_less - t_greater

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()
        races = parse_file(lines)
        print(reduce(operator.mul, (compute_winners_naive(r) for r in races)))
        print(compute_winners_clever(parse_file2(lines)))