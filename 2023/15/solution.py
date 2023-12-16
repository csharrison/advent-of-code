from functools import reduce
import re

class Box():
    def __init__(self, box_num):
        self.lens_slots = []
        self.box_num = box_num

    def index(self, label):
        for i, slot in enumerate(self.lens_slots):
            if slot[0] == label:
                return i
        return None
    
    def remove_lens(self, lens_label):
        i = self.index(lens_label)
        if i is not None:
            self.lens_slots.pop(i)

    def replace_lens(self, lens_label, focal_length):
        i = self.index(lens_label)
        if i is None:
            self.lens_slots.append((lens_label, focal_length))
        else:
            self.lens_slots[i] = (lens_label, focal_length)

    def focusing_power(self):
        return sum((1 + self.box_num) * (1 + i) * l[1] for i, l in enumerate(self.lens_slots))


def HASH(str):
    return reduce(lambda c, x: ((c + ord(x)) * 17) % 256, str, 0)

def HASHMAP(str, boxes):
    split = re.split('=|-', str)
    label = split[0]
    box = boxes[HASH(label)]
    if str.count('-') > 0:
        box.remove_lens(label)
    else:
        box.replace_lens(label, int(split[1]))

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        sequence = f.read().replace('\n','').split(',')
        print(sum(HASH(s) for s in sequence))

        boxes = [Box(b) for b in range(256)]
        for s in sequence:
            HASHMAP(s, boxes)
        print(sum(b.focusing_power() for b in boxes))