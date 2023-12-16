class Beam():
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def in_bounds(self, lines):
        x, y = self.x, self.y
        return x >= 0 and x < len(lines[0]) and y >= 0 and y < len(lines)

    def move_and_reemit(self, lines):
        c = lines[self.y][self.x]
        if c == "/":
            self.dx, self.dy = (-self.dy, -self.dx)
        elif c == "\\":
            self.dx, self.dy = (self.dy, self.dx)
        elif c == "-" and self.dx == 0:
            self.dx = -1
            self.dy = 0
            yield Beam(self.x + 1, self.y, 1, 0)
        elif c == "|" and self.dy == 0:
            self.dx = 0
            self.dy = -1
            yield Beam(self.x, self.y + 1, 0, 1)

        self.x += self.dx
        self.y += self.dy
        yield self

def all_starting_beams(lines):
    for y in range(len(lines)):
        yield Beam(0, y, 1, 0)
        yield Beam(len(lines[0]) - 1, y, -1, 0)
    for x in range(len(lines[0])):
        yield Beam(x, 0, 0, 1)
        yield Beam(x, len(lines) - 1, 0, -1)
        
def navigate(lines, starting_beam):
    beams = [starting_beam]
    e_dir = set()
    while len(beams):
        new_beams = []
        for b in beams:
            e_dir.add((b.x, b.y, b.dx, b.dy))
            new_beams.extend(list(b.move_and_reemit(lines)))
        beams = [b for b in new_beams if b.in_bounds(lines) and (b.x, b.y, b.dx, b.dy) not in e_dir]
    return len(set((x, y) for x,y,dx,dy in e_dir))

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines()]
        print(navigate(lines, Beam(0, 0, 1, 0)))
        print(max(navigate(lines, b) for b in all_starting_beams(lines)))