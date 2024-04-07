import modules.msi_ec
import modules.intel

def write_msi_ec_profile(prof, conf):
    ec = modules.msi_ec.open_ec_file(conf)
    try:
        if 'shift' in prof:
            modules.msi_ec.write_shift(ec, prof['shift'], conf)
        if 'fanmode' in prof:
            modules.msi_ec.write_fanmode(ec, prof['fanmode'], conf)
    finally:
        # ec.close()
        pass

def write_intel_profile(prof, num_cores):
    if 'undervolt' in prof:
        modules.intel.write_undervolt(prof['undervolt'], num_cores)
    if 'turbo' in prof:
        modules.intel.write_turbo_boosts(prof['turbo'], num_cores)

def write_profile(prof, conf):
    if 'msi_ec' in prof:
        write_msi_ec_profile(prof['msi_ec'], conf['ec'])
    if 'intel' in prof:
        write_intel_profile(prof['intel'], conf['msr']['num_cores'])