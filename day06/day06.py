import argparse
import re
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

with open(args.filename) as f:
    lines = f.read().splitlines()


def parse_input(lines, part=1):
    time_strs = lines[0].split(':')[-1].split()
    dist_strs = lines[1].split(':')[-1].split()
    if part == 1:
        times = [int(t) for t in time_strs]
        dists = [int(d) for d in dist_strs]
    if part == 2:
        times = [int(''.join(time_strs))]
        dists = [int(''.join(dist_strs))]

    return list(zip(times, dists))


def waysToBeat(time, rec):
    # get possible distances for each time
    dists = []
    for t_charge in range(time+1):
        charge_rate = 1
        t_going = time - t_charge
        speed = charge_rate * t_charge
        dist = speed * t_going
        dists.append(dist)
    dists = np.array(dists)
    return len(dists[dists > rec])

# part 1
time_distrec = parse_input(lines, part=1)
ways = []
for time, rec in time_distrec:
    ways.append(waysToBeat(time, rec))
print(f'part 1: ways to beat: {np.prod(ways)}')

# part 2
ways = []
time_distrec = parse_input(lines, part=2)
for time, rec in time_distrec:
    ways.append(waysToBeat(time, rec))
print(f'part 2: ways to beat: {np.prod(ways)}')
