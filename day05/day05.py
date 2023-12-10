import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

with open(args.filename) as f:
    lines = f.read().splitlines()


def parse_input_seeds(lines, part=1):
    seed_ints = [int(n) for n in lines[0].split(': ')[-1].split()]
    if part == 1:
        return seed_ints
    elif part == 2:
        seed_pairs = zip(*(iter(seed_ints),) * 2)
        return [range(s, s+d) for s, d in seed_pairs]


def parse_input_maps(lines):
    maps = []
    this_map = []
    for line in lines[2:]:
        if 'map' in line:
            if len(this_map) == 0:
                continue
            else:
                maps.append(this_map)
                this_map = []
        else:
            if len(line) > 0:
                this_map.append([int(n) for n in line.split()])
    maps.append(this_map)
    return maps


def apply_map(in_num, map_ranges):
    for dest_start, source_start, rangelen in map_ranges:
        if source_start <= in_num <= source_start + rangelen:
            return dest_start + (in_num - source_start)
    return in_num


def send_through_maps(seed, maps):
    for m in maps:
        seed = apply_map(seed, m)
    return seed

# part 1
seeds = parse_input_seeds(lines)
map_bones = parse_input_maps(lines)
locations = [send_through_maps(seed, map_bones) for seed in seeds]
print(f'part 1: lowest location is {min(locations)}')

# part 2
def sieve_shift_all(input_range, overlapping_rules):
    # input range like range(0, 10)
    # overlapping_rules like [(range(2, 7), 10), (range(8, 9), 20)]
    # out should be [range(0, 2), range(12, 17), range(7, 8), range(28, 29),
    # range(9, 10)]
    outs = []
    overlapping_rules = sorted(overlapping_rules, key=lambda x: x[0].start)
    start = input_range.start
    for overlap, shift_amt in overlapping_rules:
        outs.append(range(start, overlap.start))
        outs.append(range(overlap.start + shift_amt, overlap.stop + shift_amt))
        start = overlap.stop
    if sum([len(r) for r in outs]) != len(input_range):
        outs.append(range(start, input_range.stop))
    return outs


def apply_map_to_ranges(input_ranges, map_rules_list, verbose=False):
    # input ranges like [range(79, 93), range(55, 68)]
    # map_rules_list like [[50, 98, 2], [52, 50, 48]]
    if verbose: print(f'\ninput ranges: {input_ranges}')
    out_ranges = []
    for input_range in input_ranges:
        if verbose: print(f'now handling input range: {input_range}')
        overlapping_rules = []
        full_overlap = False
        for dest_start, source_start, rangelen in map_rules_list:
            shift_amt = dest_start - source_start
            source_range = range(source_start, source_start + rangelen)
            overlap = range(max(input_range.start, source_range.start),
                            min(input_range.stop, source_range.stop))
            if len(overlap) > 0:
                overlapping_rules.append((overlap, shift_amt))
            if len(overlap) == len(input_range):
                # full overlap, shift orig
                out_ranges.append(
                    range(overlap.start + shift_amt,
                          overlap.stop + shift_amt)
                )
                full_overlap = True
        if full_overlap:
            continue
        if len(overlapping_rules) == 0:  # no overlap, keep original
            if verbose: print(f'no overlapping rules')
            out_ranges.append(input_range)
        else:  # some overlap, split into new ranges and add all
            if verbose:
                print(f'{len(overlapping_rules)} rules to deal with, '
                      f'of a total possible {len(map_rules_list)}')
            out_ranges.extend(sieve_shift_all(input_range, overlapping_rules))

    out_ranges = list(set(out_ranges))
    if verbose: print(f'in total length is {sum([len(r) for r in input_ranges])}')
    if verbose: print(f'out total length is {sum([len(r) for r in out_ranges])}')
    if verbose: print(f'out is {out_ranges}')
    return out_ranges

verbose = False

seed_ranges = parse_input_seeds(lines, part=2)
if verbose: print(f'length of total ranges is {sum([len(r) for r in seed_ranges])}')
map_bones = parse_input_maps(lines)
input_ranges = seed_ranges
for mapping in map_bones:
    input_ranges = apply_map_to_ranges(input_ranges, mapping, verbose=verbose)
min_all = min([r.start for r in input_ranges])
if verbose: print(f'we have {len(input_ranges)} input ranges')
if verbose: print(f'length of total ranges is {sum([len(r) for r in input_ranges])}')
print(f'part 2: lowest location is {min_all}')

