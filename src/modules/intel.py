REGISTER_UNDERVOLT = '0x150'

CPU_DIGIT = '0'
CACHE_DIGIT = '2'

READ_DIGIT = '0'
WRITE_DIGIT = '1'

READ_CPU_UVOLT_ARG = f'0x80000{CPU_DIGIT}1{READ_DIGIT}00000000'
READ_CACHE_UVOLT_ARG = f'0x80000{CACHE_DIGIT}1{READ_DIGIT}00000000'

WRITE_CPU_UVOLT_PREFIX = f'0x80000{CPU_DIGIT}1{WRITE_DIGIT}'
WRITE_CACHE_UVOLT_PREFIX = f'0x80000{CACHE_DIGIT}1{WRITE_DIGIT}'

REGISTER_TURBO_BOOST = '0x1ad'

def read_turbo_boost(dry):
    print('\x1b[1;93mCurrent Turbo Boost ratios:\x1b[0m')

    if dry:
        print(f'\x1b[1;94mexec:\x1b[0m '
            f'rdmsr {REGISTER_TURBO_BOOST} '
            f'\x1b[1;95m(read as array of turbo boost ratios)\x1b[0m')
        return

def set_turbo_boost(ratios, dry, quiet):
    set_turbo_boost_arg = ''.join([ f'{r:02x}' for r in ratios ])
    
    # TODO: better msg
    if not quiet:
        print(f'\x1b[1;93mApplying Turbo Boost Ratios {ratios}...\x1b[0m')

    if dry:
        print(f'\x1b[1;94mexec:\x1b[0m '
            f'wrmsr {REGISTER_TURBO_BOOST} {set_turbo_boost_arg}')
        return


def read_plane_undervolt(plane_arg, plane_name, dry):
    if dry:
        print(f'\x1b[1;94mexec:\x1b[0m '
            f'wrmsr {REGISTER_UNDERVOLT} {plane_arg}')
        print(f'\x1b[1;94mexec:\x1b[0m '
            f'rdmsr {REGISTER_UNDERVOLT} '
            f'\x1b[1;95m(read as {plane_name} undervolt)\x1b[0m')
        return None
    return 80 # temp value

def read_cpu_uvolt(dry):
    return read_plane_undervolt(READ_CPU_UVOLT_ARG, 'CPU', dry)

def read_cache_uvolt(dry):
    return read_plane_undervolt(READ_CPU_UVOLT_ARG, 'cache', dry)

def read_undervolt(dry):
    print('\x1b[1;93mCurrent CPU undervolt:\x1b[0m')

    cpu_uvolt = read_cpu_uvolt(dry)
    cache_uvolt = read_cache_uvolt(dry)

    if dry: return
    
    print(f'CPU: {cpu_uvolt} (-{cpu_uvolt/1.024:.1f} mV)')
    print(f'Cache: {cache_uvolt} (-{cache_uvolt/1.024:.1f} mV)')


def offset_bytes(offset):
    b = (-offset & 0x7ff) << 21
    return f'{b:08x}'

def undervolt(offset, dry, quiet):
    uvolt_offset = offset_bytes(offset)
    cpu_uvolt_bytes = f'{WRITE_CPU_UVOLT_PREFIX}{uvolt_offset}'
    cache_uvolt_bytes = f'{WRITE_CACHE_UVOLT_PREFIX}{uvolt_offset}'

    if not quiet:
        print(f'\x1b[1;93mApplying CPU undervolt of {offset} units...\x1b[0m')

    if dry:
        print(f'\x1b[1;94mexec:\x1b[0m '
            f'wrmsr {REGISTER_UNDERVOLT} {cpu_uvolt_bytes}')
        print(f'\x1b[1;94mexec:\x1b[0m '
            f'wrmsr {REGISTER_UNDERVOLT} {cache_uvolt_bytes}')
        return
    
    # TODO: Actually do the undervolting here