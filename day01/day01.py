import re

with open('input.txt') as f:
    lines = f.read().splitlines()

# part 1
nums_only = [re.sub('[^0-9]', '', line) for line in lines]
sums = [int(num[0]+num[-1]) for num in nums_only]
print(f'part 1: {sum(sums)}')

# part 2: include digits spelled out with letters
spelled = {'one': '1',
           'two': '2',
           'three': '3',
           'four': '4',
           'five': '5',
           'six': '6',
           'seven': '7',
           'eight': '8',
           'nine': '9',
          }

def l2r_replace(in_str, replace_dict):
    for i in range(len(in_str) + 1):
        for key in spelled.keys():
            if in_str[:i].endswith(key):
                in_str = in_str[:i-len(key)] + replace_dict[key] + \
                in_str[i-len(key)+1:]
    return in_str

word_replaced = [l2r_replace(line, spelled) for line in lines]
nums_only = [re.sub('[^0-9]', '', line) for line in word_replaced]
sums = [int(num[0]+num[-1]) for num in nums_only]
print(f'part 2: {sum(sums)}')
