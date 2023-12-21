import re
import operator
from functools import reduce

def parse_ratings(line):
    g = re.match("{x=([0-9]+),m=([0-9]+),a=([0-9]+),s=([0-9]+)}", line).groups()
    return {v:int(n) for v,n in zip("xmas", g)}

def parse_lines(lines):
    workflows = []
    ratings = []
    done_with_workflows = False
    for line in lines:
        l = line.strip()
        if l == "":
            done_with_workflows = True
            continue
        if done_with_workflows:
            ratings.append(parse_ratings(l))
        else:
            workflows.append(Workflow(l))
    return workflows, ratings

def split_by_op(ranges, var, op, num):
    """Given a map of xmas -> possible_range, returns two new maps

    The first map will be the map of xmas -> range where var op num is true
    The second map will be where var op num is false
    """
    rbegin, rend = ranges[var]
    range_true = ranges.copy()
    range_false = ranges.copy()
    if op == operator.lt:
        assert rbegin < num
        range_true[var] = (rbegin, num - 1)
        range_false[var] = (num, rend)
    else:
        assert rend > num
        range_true[var] = (num + 1, rend)
        range_false[var] =  (rbegin, num)
    return (range_true, range_false)

class Workflow():
    def __init__(self, line):
        # Do some parsing here just for fun.
        self.name, rules = re.match("([a-z]+){(.*)}", line).groups()
        rules = rules.split(",")
        self.last = rules[-1]

        parse_op = lambda op: operator.lt if op == "<" else operator.gt        
        def parse_condition(c):
            var, op, num, res = re.match("([x|m|a|s])([>|<])([0-9]+):([a-zA-Z]+)", c).groups()
            return var, parse_op(op), int(num), res
        
        self.conditions = [parse_condition(c) for c in rules[:-1]]

    def process_part(self, xmas_dict):
        for var, op, num, res in self.conditions:
            if op(xmas_dict[var], num):
                return res
        return self.last
    
    def recurse_to_children(self, possible_ranges):
        """Given a set of possible ranges for this workflow, return the sets of ranges for each child node and A nodes"""
        children = []
        accepts = []
        rest_range = possible_ranges
        for var, op, num, res in self.conditions:
            true, rest_range = split_by_op(rest_range, var, op, num)
            if res == "A":
                accepts.append(true)
            elif res != "R":
                children.append((res, true))
        
        if self.last == "A":
            accepts.append(rest_range)
        elif self.last != "R":
            children.append((self.last, rest_range))
        return children, accepts

def process_parts(workflows, ratings):
    workflows = {w.name: w for w in workflows}   

    def process_rating(xmas, cur_workflow):
        while cur_workflow not in "AR":
            cur_workflow = workflows[cur_workflow].process_part(xmas)
        return sum(xmas.values()) if cur_workflow == "A" else 0
    return sum(process_rating(x, "in") for x in ratings)

def process_part_combos(workflows):
    workflows = {w.name: w for w in workflows}
    flows_to_process = [("in", {v: (1, 4000) for v in "xmas"})]
    s = 0
    while len(flows_to_process):
        name, range = flows_to_process.pop()
        workflow = workflows[name]
        children, new_accepts = workflow.recurse_to_children(range)
        for a in new_accepts:
            possible_range_sizes = list(t[1] - t[0] + 1 for t in a.values())
            s += reduce(operator.mul, possible_range_sizes, 1)
        flows_to_process.extend(children)
    return s

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()
        workflows, ratings = parse_lines(lines)
        print(process_parts(workflows, ratings))
        print(process_part_combos(workflows))
