from argparse import ArgumentTypeError
import re

def bat_limit(s):
    if not str.isnumeric(s):
        raise ArgumentTypeError(f'{s} is not an integer value')
    v = int(s)
    
    if not 50 <= v <= 100:
        raise ArgumentTypeError(f'battery limit must be 50 to 100')
    return v

def turbo_ratio(s: str):
    if not re.match(r'^\d+(,\d+)*$', s):
        raise ArgumentTypeError(f'Must be comma separated list of integers (no spaces)')
    
    ratios = [int(r) for r in s.split(',')]
    if len(ratios) > 8:
        raise ArgumentTypeError(f'Can only specify 8 turbo boost ratio values')

    remaining_ratios = 8 - len(ratios)

    return [ratios[0]] * remaining_ratios + ratios

def undervolt(s):
    return int(s)

def nvclock(s):
    if not re.match(r'^\d+,\d+$', s):
        raise ArgumentTypeError(f'Must be valid clock values (format: MIN,MAX)')
    return s

def nvoffset(s):
    return int(s)