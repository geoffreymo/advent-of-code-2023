import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

with open(args.filename) as f:
    lines = f.read().splitlines()


def nums_indices(line):
    '''Take in a line and return a list of (number, starting index, end index)
    tuples'''
    matches = re.finditer(r'\d+', line)
    return [(match.group(), match.start(), match.end()) for match in matches]


def is_part_number(line_ind, start_ind, end_ind, lines, verbose=False):
    input_width = len(lines[0])
    input_length = len(lines)

    top_row = True if line_ind == 0 else False
    bottom_row = True if line_ind + 1 == input_length else False
    leftmost = True if start_ind == 0 else False
    rightmost = True if end_ind == input_width else False
    if verbose: print('top, bottom, left, right:', top_row, bottom_row, leftmost, rightmost)

    # get rows, start_ind, end_ind to check
    to_check_row_inds = [line_ind, line_ind - 1, line_ind + 1]
    if top_row: to_check_row_inds.remove(line_ind - 1)
    if bottom_row: to_check_row_inds.remove(line_ind + 1)

    to_check_start_ind = start_ind if leftmost else start_ind - 1
    to_check_end_ind = end_ind if rightmost else end_ind + 1

    # if any of those objects contain a symbol, return is_part_num
    check_rows = lines[min(to_check_row_inds):max(to_check_row_inds)+1]
    check_strs = [row[to_check_start_ind:to_check_end_ind]
                  for row in check_rows]
    regex = re.compile('[^0-9.]')
    if verbose: print('strs to check: ', check_strs)
    for string in check_strs:
        if bool(regex.search(string)):
            return True
    return False

# get all the numbers
num_line_start_end = []
for i, line in enumerate(lines):
    per_line = nums_indices(line)
    num_line_start_end.extend([[per[0], i, per[1], per[2]] for per in per_line])

# check if these are part numbers
part_nums = []
for num, line_ind, start_ind, end_ind in num_line_start_end:
    verbose = False
    if is_part_number(line_ind, start_ind, end_ind, lines, verbose=verbose):
        part_nums.append(int(num))

# sum part numbers
print(f'part 1: sum of part numbers is {sum(part_nums)}')

# part 2
def gear_indices(line):
    '''Take in a line and return a list of (gear, index)
    tuples'''
    matches = re.finditer(r'\*', line)
    return [(match.group(), match.start()) for match in matches]


def find_nums(ind, row_inds, lines):
    nums = []
    for row_ind in row_inds:
        line = lines[row_ind]
        num_startind_endind = [
            [match.group(), match.start(), match.end()]
            for match in re.finditer(r'[0-9]+', line)]
        for num, startind, endind in num_startind_endind:
            length = endind - startind
            if (endind <= ind + 2) and (ind <= endind):
                nums.append(int(num))
            elif (startind >= ind - 1) and (startind <= ind + 1):
                nums.append(int(num))
    return nums

ratios = []

# get all the gears
num_line_ind = []
for i, line in enumerate(lines):
    per_line = gear_indices(line)
    num_line_ind.extend([[per[0], i, per[1]] for per in per_line])

# find gear ratio numbers
ratio_nums = []
input_width = len(lines[0])
input_length = len(lines)
for num, line_ind, ind in num_line_ind:
    top_row = True if line_ind == 0 else False
    bottom_row = True if line_ind + 1 == input_length else False
    to_check_row_inds = [line_ind, line_ind - 1, line_ind + 1]
    if top_row: to_check_row_inds.remove(line_ind - 1)
    if bottom_row: to_check_row_inds.remove(line_ind + 1)

    nums = find_nums(ind, sorted(to_check_row_inds), lines)
    if len(nums) == 2:
        ratio_nums.append(nums)

ratios = [ratio_num[0] * ratio_num[1] for ratio_num in ratio_nums]
print(f'part 2: sum of gear ratios is {sum(ratios)}')
