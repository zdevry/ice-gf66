#!/usr/bin/env python3

from argparse import ArgumentParser, SUPPRESS as ARG_SUPRESS
from os import geteuid, path
from sys import exit
import check

import modules.intel
import modules.msi_ec
import modules.nvidia


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
    
    parser.add_argument('-d', '--dry',
        action='store_true',
        help='do a dry run; do not execute actual system read and writes, '
        'does not require sudo to run')

    add_rwarg(('-b',),
        'gets or sets the battery charge limit',
        metavar='LIMIT', type=check.bat_limit, dest=BAT_LIMIT_NAME)
    add_rwarg(('-c',),
        'sets the state of the cooler boost fan speed, toggles it if no option provided',
        metavar=None, choices=['on', 'off'], dest=COOLER_BOOST_NAME)
    add_rwarg(('-s',),
        'gets or sets the shift mode/performance mode',
        metavar=None, choices=['eco', 'comfort', 'sport', 'turbo'], dest=SHIFT_MODE_NAME)
    add_rwarg(('-f',),
        'gets or sets the fan mode setting',
        metavar=None, choices=['auto', 'silent', 'advanced'], dest=FAN_MODE_NAME)

    add_rwarg(('-t',),
        'gets or sets the turbo boost ratio of the Intel CPU',
        metavar='RATIO', type=check.turbo_ratio, dest=TURBO_BOOST_NAME)
    add_rwarg(('-u',),
        'gets or sets the negative voltage offset of the Intel CPU in units '
        'of mV (get) or 1/1.024 ~ 0.977mV (set)',
        metavar='OFFSET', type=check.undervolt, dest=UNDERVOLT_NAME)

    add_warg(('-C',),
        'sets the minimum and maximum frequency of the NVidia GPU '
        'specified in the format MIN,MAX (MHz)',
        metavar='MIN,MAX', type=check.nvclock, dest=NVCLOCK_LIMIT_NAME)
    add_warg(('-O',),
        'sets the clock offset of the NVidia GPU',
        metavar='OFFSET', type=check.nvoffset, dest=NVCLOCK_OFFSET_NAME)

def msi_ec_sys(args):
    dry = args.dry

    if not dry and not path.exists('/sys/kernel/debug/ec/ec0/io'):
        print('\x1b[1;91mWARN: ec_sys kernel module has not been loaded, '
            'anything interfacing with it will not execute\x1b[0m')
        return
    
    if BAT_LIMIT_NAME in args:
        limit = getattr(args, BAT_LIMIT_NAME)
        if limit is None:
            modules.msi_ec.get_bat_limit(dry)
        else:
            modules.msi_ec.set_bat_limit(limit, dry)

    if SHIFT_MODE_NAME in args:
        mode = getattr(args, SHIFT_MODE_NAME)
        if mode is None:
            modules.msi_ec.get_shift_mode(dry)
        else:
            modules.msi_ec.set_shift_mode(mode, dry)
    
    if FAN_MODE_NAME in args:
        mode = getattr(args, FAN_MODE_NAME)
        if mode is None:
            modules.msi_ec.get_fan_mode(dry)
        else:
            modules.msi_ec.set_fan_mode(mode, dry)
    
    if COOLER_BOOST_NAME in args:
        boost = getattr(args, COOLER_BOOST_NAME)
        if boost is None:
            modules.msi_ec.toggle_cooler_boost(dry)
        else:
            modules.msi_ec.set_cooler_boost(boost, dry)
    
    modules.msi_ec.close_ec_file()

def intel_msr(args):
    dry = args.dry

    if not dry and not path.exists('/dev/cpu/0/msr'):
        print('\x1b[1;91mWARN: msr kernel module has not been loaded, '
            'anything interfacing with it will not execute\x1b[0m')
        return

    if TURBO_BOOST_NAME in args:
        ratios = getattr(args, TURBO_BOOST_NAME)
        if ratios is None:
            modules.intel.read_turbo_boost(dry)
        else:
            modules.intel.set_turbo_boost(ratios, dry)

    if UNDERVOLT_NAME in args:
        undervolt = getattr(args, UNDERVOLT_NAME)
        if undervolt is None:
            modules.intel.read_undervolt(dry)
        else:
            modules.intel.undervolt(undervolt, dry)

def nvidia_clock(args):
    dry = args.dry

    nvc_limit = getattr(args, NVCLOCK_LIMIT_NAME)
    nvc_offset = getattr(args, NVCLOCK_OFFSET_NAME)

    if nvc_limit is not None:
        modules.nvidia.set_clock_limit(nvc_limit, dry)

    if nvc_offset is not None:
        modules.nvidia.set_clock_offset(nvc_offset, dry)


def run(args):
    msi_ec_sys(args)
    intel_msr(args)
    nvidia_clock(args)
    

def main():
    add_args()

    args = parser.parse_args()

    if geteuid() != 0 and not args.dry:
        print('Must have root permissions to execute this program, unless a dry run is performed')
        exit(1)

    run(args)

if __name__ == '__main__':
    main()