import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

with open(args.filename) as f:
    lines = f.read().splitlines()


def parse_card(line):
    '''Returns list of winning numbers and list of numbers I have
    '''
    numbers = line.split(': ')[-1]
    winning_str, mine_str = numbers.split(' | ')
    winning = winning_str.split()
    mine = mine_str.split()
    return [int(n) for n in winning], [int(m) for m in mine]


def points_per_card(winning, mine):
    '''Calculate points per card given lists of winning numbers and numbers I
    have
    '''
    winning = set(winning)
    points = 0
    for num in mine:
        if num in winning:
            if points == 0:
                points += 1
            else:
                points *= 2
    return points

# part 1
total_points = 0
for line in lines:
    winning, mine = parse_card(line)
    total_points += points_per_card(winning, mine)

print(f'part 1: total number of points is {total_points}')


# part 2
def matching_numbers(winning, mine):
    winning = set(winning)
    return len([n for n in mine if n in winning])


def make_card_match_dict(lines):
    card_matches = {}
    for i, line in enumerate(lines):
        winning, mine = parse_card(line)
        card_matches[i+1] = matching_numbers(winning, mine)
    return card_matches


def subsequent_numcards(card: int, card_matches: dict):
    matches = card_matches[card]
    total = 0
    if matches == 0:
        return 0
    else:
        spawned_cards = list(range(card + 1, card + 1 + matches))
        total += len(spawned_cards)
        for spawned_card in spawned_cards:
            total += subsequent_numcards(spawned_card, card_matches)
        return total


card_matches = make_card_match_dict(lines)
scratchcards = 0
for card in range(len(lines)):
    card += 1
    scratchcards += 1
    scratchcards += subsequent_numcards(card, card_matches)

print(f'part 2: total number of scratchcards is {scratchcards}')
