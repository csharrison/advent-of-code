def extrapolate_history(line):
    def get_differences(l):
        for i in range(1, len(l)):
            yield l[i] - l[i-1]
    lines = [line]
    while any(d != 0 for d in line):
        line = list(get_differences(line))
        lines.append(line)

    next_differences = (0, 0)
    for d in reversed(lines):
        d.insert(0, d[0] - next_differences[0])
        d.append(d[-1] + next_differences[1])
        next_differences = (d[0], d[-1])
    return lines[0]  

def parse_line(line):
    return [int(num) for num in line.split()]

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()
        sums = [0, 0]
        for line in lines:
            history = extrapolate_history(parse_line(line))
            sums[0] += history[0]
            sums[1] += history[-1]
        print(sums)