import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

with open(args.filename) as f:
    lines = f.read().splitlines()

# part 1
possible = {'red': 12,
            'green': 13,
            'blue': 14,
           }
allowed_games = []

for line in lines:
    game_num = int(line.split(':')[0].split('Game ')[-1])
    revealed = {'red': 0,
                'green': 0,
                'blue': 0,
               }
    reveals = line.split(': ')[-1].split(';')
    for reveal in reveals:
        this_reveal = {'red': 0,
                    'green': 0,
                    'blue': 0,
                   }
        revealed_colours = reveal.split(',')
        for revealed_colour in revealed_colours:
            this_colour = {}
            for colour in ['red', 'green', 'blue']:
                this_colour[colour] = (int(
                    re.sub('[^0-9]', '', revealed_colour)) if colour in
                    revealed_colour else 0)
            for colour in ['red', 'green', 'blue']:
                if this_colour[colour] > this_reveal[colour]:
                    this_reveal[colour] = this_colour[colour]
        # each this_reveal shows how many colours were in a particular reveal
        # if for any colour, the colour from this_reveal is greater than the
        # revealed colour, replace the revealed colour with this
        for colour in ['red', 'green', 'blue']:
            if this_reveal[colour] > revealed[colour]:
                revealed[colour] = this_reveal[colour]
    # is this game allowed?
    allowed = all([(revealed[colour] <= possible[colour])
               for colour in ['red', 'green', 'blue']])
    if allowed:
        allowed_games.append(game_num)

print(f'part 1: sum of allowed game indices: {sum(allowed_games)}')

# part 2
powers = []
for line in lines:
    game_num = int(line.split(':')[0].split('Game ')[-1])
    revealed = {'red': 0,
                'green': 0,
                'blue': 0,
               }
    reveals = line.split(': ')[-1].split(';')
    for reveal in reveals:
        this_reveal = {'red': 0,
                    'green': 0,
                    'blue': 0,
                   }
        revealed_colours = reveal.split(',')
        for revealed_colour in revealed_colours:
            this_colour = {}
            for colour in ['red', 'green', 'blue']:
                this_colour[colour] = (int(
                    re.sub('[^0-9]', '', revealed_colour)) if colour in
                    revealed_colour else 0)
            for colour in ['red', 'green', 'blue']:
                if this_colour[colour] > this_reveal[colour]:
                    this_reveal[colour] = this_colour[colour]
        # each this_reveal shows how many colours were in a particular reveal
        # if for any colour, the colour from this_reveal is greater than the
        # revealed colour, replace the revealed colour with this
        for colour in ['red', 'green', 'blue']:
            if this_reveal[colour] > revealed[colour]:
                revealed[colour] = this_reveal[colour]
    # power of this game
    power = revealed['red'] * revealed['green'] * revealed['blue']
    powers.append(power)

print(f'part 2: sum of powers is {sum(powers)}')
