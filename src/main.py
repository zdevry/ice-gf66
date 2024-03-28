#!/usr/bin/env python3

from argparse import ArgumentParser, SUPPRESS as ARG_SUPRESS
from os import geteuid
from sys import exit
import check

import modules.intel


BAT_LIMIT_NAME = 'bat_limit'
COOLER_BOOST_NAME = 'cooler_boost'
SHIFT_MODE_NAME = 'shift_mode'
FAN_MODE_NAME = 'fan_mode'

TURBO_BOOST_NAME = 'turbo_boost'
UNDERVOLT_NAME = 'undervolt'

NVCLOCK_LIMIT_NAME = 'nv_clock'
NVCLOCK_OFFSET_NAME = 'nv_offset'


parser = ArgumentParser()

syscmds = parser.add_argument_group('system options')

def add_rwarg(names, help, **kwargs):
    syscmds.add_argument(
        *names, nargs='?', help=help,
        default=ARG_SUPRESS, **kwargs
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
        metavar='LIMIT', type=check.bat_limit, dest=BAT_LIMIT_NAME)
    add_rwarg(('-c', '--cooler'),
        'gets or sets the state of the cooler boost fan speed',
        metavar=None, choices=['on', 'off'], dest=COOLER_BOOST_NAME)
    add_rwarg(('-s', '--shift'),
        'gets or sets the shift mode/performance mode',
        metavar=None, choices=['eco', 'comfort', 'sport', 'turbo'], dest=SHIFT_MODE_NAME)
    add_rwarg(('-f', '--fan'),
        'gets or sets the fan mode setting',
        metavar=None, choices=['auto', 'silent', 'advanced'], dest=FAN_MODE_NAME)

    add_rwarg(('-t', '--boost'),
        'gets or sets the turbo boost ratio of the Intel CPU',
        metavar='RATIO', type=check.turbo_ratio, dest=TURBO_BOOST_NAME)
    add_rwarg(('-u', '--uvolt'),
        'gets or sets the negative voltage offset of the Intel CPU in units '
        'of mV (get) or 1/1.024 ~ 0.977mV (set)',
        metavar='OFFSET', type=check.undervolt, dest=UNDERVOLT_NAME)

    add_warg(('-C', '--nvc'),
        'sets the minimum and maximum frequency of the NVidia GPU '
        'specified in the format MIN,MAX (MHz)',
        metavar='MIN,MAX', type=check.nvclock, dest=NVCLOCK_LIMIT_NAME)
    add_warg(('-O', '--nvo'),   
        'sets the clock offset of the NVidia GPU',
        metavar='OFFSET', type=check.nvoffset, dest=NVCLOCK_OFFSET_NAME)


def run(args):
    dry = args.dry
    quiet = args.quiet

    if TURBO_BOOST_NAME in args:
        ratios = getattr(args, TURBO_BOOST_NAME)
        if ratios is None:
            modules.intel.read_turbo_boost(dry)
        else:
            modules.intel.set_turbo_boost(ratios, dry, quiet)

    if UNDERVOLT_NAME in args:
        undervolt = getattr(args, UNDERVOLT_NAME)
        if undervolt is None:
            modules.intel.read_undervolt(dry)
        else:
            modules.intel.undervolt(undervolt, dry, quiet)

def main():
    add_args()

    args = parser.parse_args()

    if geteuid() != 0 and not args.dry:
        print('Must have root permissions to execute this program, unless a dry run is performed')
        exit(1)

    run(args)

if __name__ == '__main__':
    main()