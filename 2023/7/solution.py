
from enum import IntEnum
from collections import defaultdict
from itertools import combinations_with_replacement

RANKINGS = {
    c: rank for rank, c in enumerate(
        ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    )
}

JOKER_RANKINGS = {
    c: rank for rank, c in enumerate(
        ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
    )
}

NON_JOKERS = [k for k in RANKINGS.keys() if k != 'J']

class HandType(IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_KIND = 5
    FIVE_OF_KIND = 6

def get_type(hand: str):
    counts = defaultdict(int)
    for card in hand:
        counts[card] += 1

    raw_counts = sorted(list(counts.values()))
    max_count = max(raw_counts)
    if max_count == 5:
        return HandType.FIVE_OF_KIND
    
    if max_count == 4:
        return HandType.FOUR_OF_KIND
    
    if raw_counts == [2, 3]:
        return HandType.FULL_HOUSE
    
    if max_count == 3:
        return HandType.THREE_OF_KIND
    
    if raw_counts.count(2) == 2:
        return HandType.TWO_PAIR
    
    if max_count == 2:
        return HandType.ONE_PAIR

    return HandType.HIGH_CARD

def get_type_with_joker(hand: str):
    hand_without_jokers = hand.replace('J', '')
    num_jokers = len(hand) - len(hand_without_jokers)
    return max(
        get_type(hand_without_jokers + "".join(combination))
        for combination in combinations_with_replacement(NON_JOKERS, num_jokers)
    )

class Hand():
    def __init__(self, hand, bid, jokers_wild=False):
        self.hand = hand
        self.bid = bid
        self.jokers_wild = jokers_wild
        self.type = get_type_with_joker(hand) if jokers_wild else get_type(hand)
        ranking = JOKER_RANKINGS if self.jokers_wild else RANKINGS
        self.lex_hand = tuple(ranking[c] for c in hand)

    def __lt__(self, other):
        if self.type == other.type:
            return self.lex_hand < other.lex_hand
        return self.type < other.type

def accumulate_winnings(hands):
    return sum((rank + 1) * h.bid for rank, h in enumerate(hands))

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        raw_data = [line.split() for line in f.readlines()]
        raw_data = [(hand, int(bid)) for hand,bid in raw_data]

        hands = sorted(Hand(*x) for x in raw_data)
        print(accumulate_winnings(hands))

        joker_hands = sorted(Hand(*x, jokers_wild=True) for x in raw_data)
        print(accumulate_winnings(joker_hands))
