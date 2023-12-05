import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

with open(args.filename) as f:
    lines = f.read().splitlines()

colours = ['red', 'green', 'blue']

# part 1
possible = {'red': 12,
            'green': 13,
            'blue': 14,
           }
allowed_games = []
# part 2
powers = []

for line in lines:
    game_num = int(line.split(':')[0].split('Game ')[-1])
    game_colours = {}
    for col in colours:
        col_instances = re.findall(rf'\d+ {col}', line)
        col_max = max([
            int(instance.split(' ')[0]) for instance in col_instances])
        game_colours[col] = col_max

    # is this game allowed?
    allowed = all([(game_colours[colour] <= possible[colour])
               for colour in ['red', 'green', 'blue']])
    if allowed:
        allowed_games.append(game_num)

    # part 2: power of these games
    power = game_colours['red'] * game_colours['green'] * game_colours['blue']
    powers.append(power)

print(f'part 1: sum of allowed game indices: {sum(allowed_games)}')
print(f'part 2: sum of powers is {sum(powers)}')
