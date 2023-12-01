import string
def parse_line(line: str):
  digits = [d for d in line if d.isdigit()]
  return int(digits[0] + digits[-1])

DIGIT_WORDS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
def to_digit(digit_or_word: str):
  if digit_or_word not in DIGIT_WORDS:
    return digit_or_word
  return str(DIGIT_WORDS.index(digit_or_word) + 1)

def parse_line2(line: str):
  to_find = DIGIT_WORDS + list(string.digits[1:])
  minimum = min((line.index(d), d) for d in to_find if d in line)
  maximum = max((line.rindex(d), d) for d in to_find if d in line)

  return int(to_digit(minimum[1]) + to_digit(maximum[1]))

if __name__ == "__main__":
  with open('input.txt', 'r') as f:
    lines = f.readlines()
    print(sum(parse_line(l) for l in lines))
    print(sum(parse_line2(l) for l in lines))
