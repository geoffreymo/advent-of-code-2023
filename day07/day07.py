import argparse
import re
import numpy as np
from collections import Counter
from functools import cmp_to_key

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

with open(args.filename) as f:
    lines = f.read().splitlines()

def parse_input(lines):
    hands, bids = np.array([line.split() for line in lines]).T
    return hands, [int(bid) for bid in bids]

def handtype(hand):
    '''0 is most powerful, 6 is least'''
    cntr = Counter(hand)
    cntrvals_rank = {
        (5,): 0,
        (1, 4): 1,
        (2, 3): 2,
        (1, 1, 3): 3,
        (1, 2, 2): 4,
        (1, 1, 1, 2): 5,
        (1, 1, 1, 1, 1): 6
    }
    return cntrvals_rank[tuple(sorted(cntr.values()))]

def comp(hand1, hand2):
    '''Again, 0 is most powerful. Negative when hand1 > hand2'''
    for i in range(len(hand1)):
        let1, let2 = hand1[i], hand2[i]
        if order.index(let1) < order.index(let2):
            return -1
        elif order.index(let1) > order.index(let2):
            return 1

# part 1
order = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
hands, bids = parse_input(lines)
handbids = {h:b for h, b in zip(hands, bids)}

hand_groups = {i: [] for i in range(7)}
for hand in hands:
    hand_groups[handtype(hand)].append(hand)
hands_sorted_groups = [sorted(hand_groups[i], key=cmp_to_key(comp))
                       for i in range(7)]
hands_sorted = [hand for group in hands_sorted_groups for hand in group][::-1]

winnings = 0
for i, hand in enumerate(hands_sorted):
    winnings += (i+1) * handbids[hand]

print(f'part 1: winnings are {winnings}')

# part 2
order = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
hands, bids = parse_input(lines)
handbids = {h:b for h, b in zip(hands, bids)}

def handtype(hand):
    '''0 is most powerful, 6 is least'''
    cntr = Counter(hand)
    cntrvals_rank = {
        (5,): 0,
        (1, 4): 1,
        (2, 3): 2,
        (1, 1, 3): 3,
        (1, 2, 2): 4,
        (1, 1, 1, 2): 5,
        (1, 1, 1, 1, 1): 6
    }
    rank = cntrvals_rank[tuple(sorted(cntr.values()))]
    if 'J' in hand:
        if rank in [0, 1, 2]:
            # JJAAA rank 2 -> rank 0
            # AAJJJ rank 2 -> rank 0
            rank = 0
        elif rank == 3:
            # AAA1J rank 3 -> rank 1
            # A2JJJ rank 3 -> rank 1
            rank = 1
        elif rank == 4:
            if cntr['J'] == 1:
                rank = 2
            elif cntr['J'] == 2:
                rank = 1
        elif rank == 5:
            # A233J becomes rank 3
            # A69JJ becomes rank 3
            rank = 3
        elif rank == 6:
            # AK79J becomes rank 5
            rank = 5
    return np.max([rank, 0])


hand_groups = {i: [] for i in range(7)}
for hand in hands:
    hand_groups[handtype(hand)].append(hand)
hands_sorted_groups = [sorted(hand_groups[i], key=cmp_to_key(comp))
                       for i in range(7)]
hands_sorted = [hand for group in hands_sorted_groups for hand in group][::-1]

winnings = 0
for i, hand in enumerate(hands_sorted):
    winnings += (i+1) * handbids[hand]

print(f'part 2: winnings are {winnings}')
