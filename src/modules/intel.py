MSR_FILE_FORMAT = '/dev/cpu/{}/msr'

TURBO_REGISTER = 0x1AD
UNDERVOLT_REGISTER = 0x150

READ_BYTE = b'\x10'
WRITE_BYTE = b'\x11'

UVOLT_PLANE_BYTES = {
    'core': b'\x00',
    'igpu': b'\x01',
    'cache': b'\x02',
    'agent': b'\x03',
    'analog_io': b'\x04',
    'digital_io': b'\x05',
}


def wrmsr_on_all_cpus(reg, regval, num_cores):
    for i in range(num_cores):
        wrmsr_on_cpu(reg, i, regval)

def wrmsr_on_cpu(reg, cpu, regval):
    file = MSR_FILE_FORMAT.format(cpu)
    wrnum = int.from_bytes(regval, byteorder='little')
    print(f'Write {regval} (0x{wrnum:016x}) to register {reg:04x} : {file}')


def write_turbo_boosts(boosts, num_cores):
    tailing_boosts = 8 - len(boosts)
    all_boosts = boosts + boosts[-1:-2:-1] * tailing_boosts

    wrmsr_on_all_cpus(TURBO_REGISTER, bytes(all_boosts), num_cores)


def undervolt_bytes(uvolt):
    b = (-uvolt & 0x7FF) << 21
    return b.to_bytes(4, byteorder='little')

def write_undervolt(uvolts, num_cores):
    for plane in uvolts:
        if plane not in UVOLT_PLANE_BYTES:
            continue
        plane_byte = UVOLT_PLANE_BYTES[plane]
        uvolt = uvolts[plane]
        
        regval = undervolt_bytes(uvolt) + WRITE_BYTE + plane_byte + b'\x00\x80'

        wrmsr_on_all_cpus(UNDERVOLT_REGISTER, regval, num_cores)