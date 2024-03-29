from subprocess import run

persistence_mode = False # Assumed

def check_persistence_mode(dry):
    global persistence_mode
    if persistence_mode: return
    
    print('\x1b[1;93mEnabling persistence mode...\x1b[0m')

    persistence_mode = True

    if dry:
        print('\x1b[1;94mexec:\x1b[0m '
            'nvidia-smi -pm 1')
        return
    
    run(['nvidia-smi', '-pm', '1'])

def set_clock_limit(limit, dry):
    check_persistence_mode(dry)
    print(f'\x1b[1;93mSetting GPU clock limit to {limit} MHz...\x1b[0m')
    
    if dry:
        print('\x1b[1;94mexec:\x1b[0m '
            f'nvidia-smi -lgc {limit}')
        return
    
    run(['nvidia-smi', '-lgc', limit])

def set_clock_offset(offset, dry):
    check_persistence_mode(dry)
    print(f'\x1b[1;93mSetting GPU clock offset to +{offset}MHz...\x1b[0m')
    
    if dry:
        print('\x1b[1;94mexec:\x1b[0m '
            f'nvidia-settings -a [gpu:0]/GPUGraphicsClockOffsetAllPerformanceLevels={offset}')
        return
    
    run(['nvidia-settings', '-a', f'[gpu:0]/GPUGraphicsClockOffsetAllPerformanceLevels={offset}'])