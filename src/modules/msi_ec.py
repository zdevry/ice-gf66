EC_FILE = '/sys/kernel/debug/ec/ec0/io'

ADDR_COOLER_BOOST = 0x98
ADDR_SHIFT_MODE = 0xd2
ADDR_FAN_MODE = 0xd4
ADDR_BAT_LIMIT = 0xd7

SHIFT_MODES_NAME_TO_BYTE = {
    'eco': 0xc2,
    'comfort': 0xc1,
    'sport': 0xc0,
    'turbo': 0xc4,
}

SHIFT_MODES_BYTE_TO_NAME = {
    0xc2: 'eco',
    0xc1: 'comfort',
    0xc0: 'sport',
    0xc4: 'turbo'
}

FAN_MODES_NAME_TO_BYTE = {
    'auto': 0x0d,
    'silent': 0x1d,
    'advanced': 0x8d
}

FAN_MODES_BYTE_TO_NAME = {
    0x0d: 'auto',
    0x1d: 'silent',
    0x8d: 'advanced'
}


def read_ec_byte(addr, dry):
    if dry:
        print(f'\x1b[1;94mread:\x1b[0m '
            f'{EC_FILE}, addr: 0x{addr:02x}')
        return None

def write_ec_byte(addr, val, dry):
    if dry:
        print(f'\x1b[1;94mwrite:\x1b[0m '
            f'{EC_FILE}, addr: 0x{addr:02x}, byte: 0x{val:02x}')


def get_shift_mode(dry):
    print('\x1b[1;93mShift mode:\x1b[0m ', end='')

    mode = read_ec_byte(ADDR_SHIFT_MODE, dry)
    if dry: return

def set_shift_mode(mode, dry, quiet):
    if not quiet:
        print(f'\x1b[1;93mSetting shift mode to {mode}...\x1b[0m')
    
    write_ec_byte(ADDR_SHIFT_MODE, SHIFT_MODES_NAME_TO_BYTE[mode], dry)


def get_fan_mode(dry):
    print('\x1b[1;93mFan mode:\x1b[0m ', end='')

    mode = read_ec_byte(ADDR_FAN_MODE, dry)
    if dry: return

def set_fan_mode(mode, dry, quiet):
    if not quiet:
        print(f'\x1b[1;93mSetting fan mode to {mode}...\x1b[0m')
    
    write_ec_byte(ADDR_FAN_MODE, FAN_MODES_NAME_TO_BYTE[mode], dry)


def get_bat_limit(dry):
    print('\x1b[1;93mBattery limit:\x1b[0m ', end='')

    mode = read_ec_byte(ADDR_BAT_LIMIT, dry)
    if dry: return

def set_bat_limit(limit, dry, quiet):
    if not quiet:
        print(f'\x1b[1;93mSetting battery limit to {limit}...\x1b[0m')
    
    write_ec_byte(ADDR_BAT_LIMIT, limit + 128, dry)


def toggle_cooler_boost(dry, quiet):
    if not quiet:
        print(f'\x1b[1;93mToggling cooler boost...\x1b[0m')
    
    # Scary! (it will definitely delete your root fs)
    original = read_ec_byte(ADDR_COOLER_BOOST, dry)
    if dry:
        print(
            '\x1b[90mNote: cooler boost toggle requires reading the EC memory first '
            'to get the original cooler boost state. '
            'The below value given in the dry run is not accurate '
            'and should actually be the read byte at 0x98 xor\'d with 0x80\x1b[0m'
        )
        write_ec_byte(ADDR_COOLER_BOOST, 0x80, dry)
        return

def set_cooler_boost(boost, dry, quiet):
    if not quiet:
        print(f'\x1b[1;93mSetting cooler boost {boost}...\x1b[0m')

    original = read_ec_byte(ADDR_COOLER_BOOST, dry)
    if dry:
        msg = 'the read byte or\'d with 0x80' if boost == 'on'\
            else 'the read byte and\'d with 0x7f'

        print(
            '\x1b[90mNote: cooler boost set requires reading the EC memory first '
            'to get the original byte at the cooler boost address 0x98. '
            'The below value given in the dry run is not accurate '
            f'and should actually be {msg}\x1b[0m'
        )
        write_ec_byte(
            ADDR_COOLER_BOOST,
            0x80 if boost == 'on' else 0x00,
            dry
        )
        return