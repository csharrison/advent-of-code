import itertools

def get_expansions(rows):
    cols = zip(*rows)
    expanded = lambda lst: [i for i, r in enumerate(lst) if "#" not in r]
    return expanded(rows), expanded(cols)

def find_all(needle, haystack):
    return (i for i, c in enumerate(haystack) if c == needle)

def get_galaxies(lines):
    galaxies = set()
    for y in range(len(lines)):
        for x in find_all("#", lines[y]):
            yield x, y

def shortest_distance(a, b, expanded_rows, expanded_cols, expansion_rate):
    x1, y1 = a
    x2, y2 = b

    rows_to_traverse = set(range(*sorted((y1, y2))))
    cols_to_traverse = set(range(*sorted((x1, x2))))

    expanded_rows_to_traverse = rows_to_traverse.intersection(expanded_rows)
    expanded_cols_to_traverse = cols_to_traverse.intersection(expanded_cols)

    return len(rows_to_traverse) + len(cols_to_traverse) \
        + len(expanded_rows_to_traverse) * (expansion_rate - 1) \
        + len(expanded_cols_to_traverse) * (expansion_rate - 1)


def sum_distances(galaxies, expanded_rows, expanded_cols, expansion_rate):
    return sum(shortest_distance(x, y, expanded_rows, expanded_cols, expansion_rate)
               for x, y in itertools.combinations(galaxies, 2))

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()
        galaxies = set(get_galaxies(lines))
        expanded_rows, expanded_cols = get_expansions(lines)
        print(sum_distances(galaxies, expanded_rows, expanded_cols, 2))
        print(sum_distances(galaxies, expanded_rows, expanded_cols, 1_000_000))