from functools import lru_cache
from collections import deque

def parse_line(line):
    record, runs = line.split()
    runs = tuple(int(i) for i in runs.split(','))
    return record, runs

def parse_line2(line):
    record, runs = parse_line(line)
    return "?".join([record] * 5), runs * 5

def is_valid(record, runs):
    assert "?" not in record
    return runs == tuple(len(r) for r in record.split('.') if r != '')

# If only python had immutable linked lists! Too lazy to implement one
# from scratch.
@lru_cache(maxsize=1000)
def count_arrangements_recursive(record, runs, in_run=False):
    if len(record) == 0 or len(runs) == 0:    
        return int(is_valid(record.replace('?', '.'), runs))

    head = record[0]
    tail = record[1:]

    if head == "?":
        damaged = count_arrangements_recursive("#" + tail, runs, in_run)
        dot = count_arrangements_recursive("." + tail, runs, in_run)
        return dot + damaged

    if head == "#":
        if runs[0] == 1:
            # We're in our last damaged part, we have to have a dot next.
            # Just do it right here.
            if len(tail) > 0 and tail[0] == '#':
                return 0
            return count_arrangements_recursive(tail[1:], runs[1:], False)
        
        # Just continue the existing run, we're chillin.
        return count_arrangements_recursive(tail, (runs[0] - 1,) + runs[1:], True)
        
    return 0 if in_run else count_arrangements_recursive(tail, runs, False)    

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()
        print(sum(count_arrangements_recursive(*parse_line(l)) for l in lines))
        print(sum(count_arrangements_recursive(*parse_line2(l)) for l in lines))