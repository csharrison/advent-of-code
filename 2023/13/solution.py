def string_diff(str1, str2):
    return sum(1 for c1, c2 in zip(str1, str2) if c1 != c2)

def check_off_by_one(pattern1, pattern2):
    assert len(pattern1) == len(pattern2)
    return sum(string_diff(s1, s2) for s1, s2 in zip(pattern1, pattern2)) == 1

def get_horizontal_reflection(pattern, exact=True):
    for i in range(len(pattern)):
        # i is the index right before the mirror
        before = list(reversed(pattern[:i]))
        after = pattern[i:]

        min_length = min(len(before), len(after))
        if min_length == 0:
            continue

        r1 = before[:min_length]
        r2 = after[:min_length]
        if (exact and r1 == r2) or (not exact and check_off_by_one(r1, r2)):
            return len(before)
    return 0

def get_vertical_reflection(pattern, exact=True):
    return get_horizontal_reflection(list(zip(*pattern)), exact)

def compute_contribution(pattern, exact=True):
    return get_vertical_reflection(pattern, exact) + get_horizontal_reflection(pattern, exact) * 100

def parse_patterns(lines):
    pattern = []
    for l in lines:
        if l == '\n':
            yield pattern
            pattern = []
        else:
            pattern.append(l.strip())
    yield pattern
    
if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()
        patterns = list(parse_patterns(lines))
        print(sum(compute_contribution(p, exact=True)for p in patterns))
        print(sum(compute_contribution(p, exact=False)for p in patterns))



