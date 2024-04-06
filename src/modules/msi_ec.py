def open_ec_file(conf):
    return None

def write_ec_byte(ec, addr, val):
    print(f'Write 0x{val:02x} to 0x{addr:02x}')

def write_shift(ec, shift, conf):
    shift_conf = conf['shift']
    addr = shift_conf['addr']
    shift_values = shift_conf['enum']

    write_ec_byte(ec, addr, shift_values[shift])

def write_fanmode(ec, fanmode, conf):
    fanmode_conf = conf['fanmode']
    addr = fanmode_conf['addr']
    fanmode_values = fanmode_conf['enum']

    write_ec_byte(ec, addr, fanmode_values[fanmode])