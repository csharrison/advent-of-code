def parse_line(line: str):
  digits = [d for d in line if d.isdigit()]
  return int(digits[0] + digits[-1])

if __name__ == "__main__":
  with open('input.txt', 'r') as f:
    print(sum(parse_line(l) for l in f.readlines()))
