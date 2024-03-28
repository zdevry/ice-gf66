
def set_persistence_mode(dry, quiet):
    if not quiet:
        print('\x1b[1;93mEnabling persistence mode...\x1b[0m')

    if dry:
        print('\x1b[1;94mexec:\x1b[0m '
            'nvidia-smi -pm 1')
        dry_run_persistence = True
        return

def set_clock_limit(limit, dry, quiet):
    if not quiet:
        print(f'\x1b[1;93mSetting GPU clock limit to {limit} MHz...\x1b[0m')
    
    if dry:
        print('\x1b[1;94mexec:\x1b[0m '
            f'nvidia-smi -lgc {limit}')
        return

def set_clock_offset(offset, dry, quiet):
    if not quiet:
        print(f'\x1b[1;93mSetting GPU clock offset to +{offset}MHz...\x1b[0m')
    
    if dry:
        print('\x1b[1;94mexec:\x1b[0m '
            f'nvidia-settings -a [gpu:0]/GPUGraphicsClockOffsetAllPerformanceLevels={offset}')
        return