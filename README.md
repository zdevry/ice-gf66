# Control centre script for MSI GF66 Laptops running Linux

This is a simple Python script that currently
allows you set using a TOML config:
* Shift/Performance mode
* Fan mode (no fan curves yet)
* Intel CPU Turbo Boost clock speed
* Intel CPU undervolt
* NVIDIA GPU clock limit
* NVIDIA GPU clock offset (should work under Wayland now)

Additionally, you can set battery limits and toggle the cooler boost
using the script directly.

**Are you using another system?** Please consult below before using!

Also note that this script has the bare minimum of error checking.  
**Review all configs carefully before using them.**

## Installation

Clone the repository.
Then, since whole script is contained in the `ice-gf66` file,
copy it to somewhere on your path, then make it executable.
```
git clone https://github.com/zijkdefry/ice-gf66.git
cd ice-gf66
sudo cp ice-gf66 /usr/local/bin/ice-gf66
sudo chmod 755 /usr/local/bin/ice-gf66
```
The script sources its configs and profiles from the `/etc/ice-gf66/` directory.
Copy these config files there.
```
sudo mkdir /etc/ice-gf66
sudo cp config.toml /etc/ice-gf66/config.toml
sudo cp profiles.toml /etc/ice-gf66/profiles.toml
```
Note if a `config.toml` or `profiles.toml` are present in the current working directory,
then the script will source those instead.

The script has these dependencies:
* Proprietary NVIDIA drivers
* `ec_sys` kernel module with `write_support=1`
* `msr` kernel module

To load the kernel modules:
```
sudo modprobe ec_sys write_support=1
sudo modprobe msr
```

## Using another Laptop?

This script was written to only work on an `MSI Katana GF66 11UE`.  
Anything interfacing with the Intel CPU and the NVIDIA GPU should
work since those use the `msr` kernel module and NVML library respectively.
(Undervolting may not work on 12th-Gen/Alder Lake and newer CPUs).
MSI has many versions of the EC memory layout, so anything else
will most likely not work correctly.

The `config.toml` file contains various options and resources that
you can use to ensure the script works correctly on your system.

Quick guide to the options:
* `num_cores` under `[msr]`. Run `ls /dev/cpu` to verify how many cores you have.
* `libnvml` under `[nv]`. This is the library file that script loads for NVML.
I use `Arch Linux`, your distro may package this file in a different location.
* most things under `[ec]` will be different for your MSI laptop.
I have put a few resources there for you to create a config for your own laptop.

**Please make sure everything is correct on your system before using the script**  
**I do not know the consequences of corrupting EC memory on an MSI laptop**

## Usage

`profiles.toml` comes with the `gaming` profile. Use this to set the profile:
```
sudo ice-gf66 -p gaming
```
Note that the program requires root user permissions to run

Additional examples:
| Command         | Function                            |
| --------------- | ----------------------------------- |
| `ice-gf66 -b N` | Sets battery limit charge to N      |
| `ice-gf66 -c`   | Toggles cooler boost                |
| `ice-gf66 -f F` | Sources a profile from the file F * |
| `ice-gf66 -h`   | Prints a help message               |

\* All the options in F should exist at the top level instead of
under a table with the name of the profile.

To create your own profile, refer to the `profiles.toml` file.

## Notice

`ice-gf66` is licensed under the GPLv3. Additionally, I do/will not claim
any liability and/or responsibility for any damage you cause to your system
by using this script. Please review the all the resources provided carefully
before using this program.

## References and sources for this project

* https://github.com/BeardOverflow/msi-ec
* https://github.com/dmitry-s93/MControlCenter
* https://github.com/mihic/linux-intel-undervolt
* https://github.com/intel/msr-tools
* https://docs.nvidia.com/deploy/nvml-api/index.html