def parse_nums(nums):
  return set(int(i) for i in nums.strip().split())

def parse_line(line):
  _, nums = line.split(':')
  winning, have = (parse_nums(i) for i in nums.split('|'))
  return (winning, have)
  
def parse_file(lines):
  return [parse_line(l) for l in lines]

def score(parsed_line):
  winning, have = parsed_line
  num_matching = len(winning.intersection(have))
  if num_matching == 0: return 0
  return 2**(num_matching-1)

def compute_score(parsed_lines):
  return sum(score(l) for l in parsed_lines)

def compute_score2(parsed_lines):
  num_cards = [1] * len(parsed_lines)
  for i,l in enumerate(parsed_lines):
    winning, have = l
    num_matching = len(winning.intersection(have))
    for card in range(i + 1, min(i + 1 + num_matching, len(parsed_lines))):
      num_cards[card] += num_cards[i]
  return sum(num_cards)

if __name__ == "__main__":
  with open("input.txt", "r") as f:
    lines = f.readlines()
    print(compute_score(parse_file(lines)))
    print(compute_score2(parse_file(lines)))
