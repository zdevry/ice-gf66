#!/usr/bin/env python3

import argparse
import check


parser = argparse.ArgumentParser()

syscmds = parser.add_argument_group('system options')

def add_rwarg(names, help, **kwargs):
    syscmds.add_argument(
        *names, nargs='?', const='READ',
        help=help, **kwargs
    )

def add_warg(names, help, **kwargs):
    syscmds.add_argument(*names, help=help, **kwargs)

def add_rarg(names, help, **kwargs):
    syscmds.add_argument(*names, action='store_true', help=help, **kwargs)

def add_args():

    parser.add_argument('-q', '--quiet',
        action='store_true',
        help='do not output feedback after writing to a system option')
    
    parser.add_argument('-d', '--dry',
        action='store_true',
        help='do a dry run; do not execute actual system read and writes, '
        'does not require sudo to run')

    add_rwarg(('-b', '--bat'),
        'gets or sets the battery charge limit',
        metavar='LIMIT', type=check.bat_limit)
    add_rwarg(('-c', '--cooler'),
        'gets or sets the state of the cooler boost fan speed',
        metavar=None, choices=['on', 'off'])
    add_rwarg(('-s', '--shift'),
        'gets or sets the shift mode/performance mode',
        metavar=None, choices=['eco', 'comfort', 'sport', 'turbo'])
    add_rwarg(('-f', '--fan'),
        'gets or sets the fan mode setting',
        metavar=None, choices=['auto', 'silent', 'advanced'])

    add_rwarg(('-t', '--boost'),
        'gets or sets the turbo boost ratio of the Intel CPU',
        metavar='RATIO', type=check.turbo_ratio)
    add_rwarg(('-u', '--uvolt'),
        'gets or sets the negative voltage offset of the Intel CPU in units '
        'of mV (get) or 1/1.024 ~ 0.977mV (set)',
        metavar='OFFSET', type=check.undervolt)

    add_warg(('-C', '--nvc'),
        'sets the minimum and maximum frequency of the NVidia GPU '
        'specified in the format MIN,MAX (MHz)',
        metavar='MIN,MAX', type=check.nvclock)
    add_warg(('-O', '--nvo'),
        'sets the clock offset of the NVidia GPU',
        metavar='OFFSET', type=check.nvoffset)

def main():
    add_args()

    args = parser.parse_args()
    print(args)

if __name__ == '__main__':
    main()