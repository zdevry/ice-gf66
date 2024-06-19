# Control centre script for MSI GF66 Laptops running Linux

This is a Python script that currently allows you set using a TOML config:
* Shift/Performance mode
* Fan mode (no fan curves yet)
* Intel CPU Turbo Boost clock speed
* Intel CPU undervolt
* NVIDIA GPU clock limit
* NVIDIA GPU clock offset (should work under Wayland)

Additionally, you can set battery limits and toggle the cooler boost
using the script directly.

**Are you using another system?** Please consult below before using!

Also note that this script has the bare minimum of error checking.  
**Review all configs carefully before using them.**

## Config and Profiles

The script reads the config.toml and profiles.toml from the `/etc/ice-gf66/` directory,
default configs are provided in the git repo.

## Using another Laptop?

This script was written to only work on an `MSI Katana GF66 11UE`.  
Anything interfacing with the Intel CPU and the NVIDIA GPU should
work since those use the `msr` kernel module and NVML library respectively.
(Undervolting may not work on 12th-Gen/Alder Lake and newer CPUs).
MSI has many versions of the EC memory layout, so anything else
will most likely not work correctly.

The `config.toml` file contains various options and resources that
you can use to ensure the script works correctly on your system.

## Usage

`profiles.toml` comes with the `gaming` profile. Use this to set the profile:
```
sudo ice-gf66 -p gaming
```
Note that the script requires root user permissions to run

| Command         | Function                            |
| --------------- | ----------------------------------- |
| `ice-gf66 -b N` | Sets battery limit charge to N      |
| `ice-gf66 -c`   | Toggles cooler boost                |
| `ice-gf66 -f F` | Sources a profile from the file F * |
| `ice-gf66 -h`   | Prints a help message               |

\* All the options in F should exist at the top level instead of
under a table with the name of the profile.

To create your own profile, refer to the `profiles.toml` file.

## References and sources for this project

* https://github.com/BeardOverflow/msi-ec
* https://github.com/dmitry-s93/MControlCenter
* https://github.com/mihic/linux-intel-undervolt
* https://github.com/intel/msr-tools
* https://www.intel.com/content/dam/develop/external/us/en/documents/335592-sdm-vol-4.pdf
* https://docs.nvidia.com/deploy/nvml-api/index.html