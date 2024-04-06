import tomllib
import modules.msi_ec

def write_msi_ec_profile(prof):
    f_conf = open('msi-ec.toml', 'rb')
    conf = tomllib.load(f_conf)
    f_conf.close()

    ec = modules.msi_ec.open_ec_file(conf)
    try:
        if 'shift' in prof:
            modules.msi_ec.write_shift(ec, prof['shift'], conf)
        if 'fanmode' in prof:
            modules.msi_ec.write_fanmode(ec, prof['fanmode'], conf)
    finally:
        # ec.close()
        pass

def write_profile(prof):
    if 'msi_ec' in prof:
        write_msi_ec_profile(prof['msi_ec'])