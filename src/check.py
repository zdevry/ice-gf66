from argparse import ArgumentTypeError
import re

def bat_limit(s):
    if not str.isnumeric(s):
        raise ArgumentTypeError(f'{s} is not an integer value')
    v = int(s)
    
    if not 50 <= v <= 100:
        raise ArgumentTypeError(f'battery limit must be 50 to 100')
    return v

def turbo_ratio(s):
    return int(s)

def undervolt(s):
    return int(s)

def nvclock(s):
    if not re.match(r'^\d+,\d+$', s):
        raise ArgumentTypeError(f'Must be valid clock values (format: MIN,MAX)')
    return s

def nvoffset(s):
    return int(s)