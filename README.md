# Control centre for MSI GF66 Laptops running Linux

This is mostly a thin but convenient interface for read/writing to the EC memory of
this MSI laptop model (basically MSI Centre for Linux) with a bonus of being
able to undervolt the Intel CPU and NVidia GPU.

This is currently a work in progress but it is enough for my setup to be able to
achieve lower temps when gaming on Linux.

**DISCLAIMER**

This program is only written to work on my MSI laptop (MSI Katana GF66 11UE).
And most probably won't work on yours (especially the EC controller memory stuff).
See below if you still wish to use the program. But:  
**USING THIS PROGRAM ON ANOTHER LAPTOP MODEL, OR USING THIS PROGRAM IMPROPERLY
MAY CAUSE PERMANENT DAMAGE TO YOUR SYSTEM.**

## Installation and Requirements

Copy the src folder to somewhere on your computer, e.g. `/usr/local/lib/`,
then create a symlink to main.py somewhere that is on your path, e.g. `/usr/local/bin/`
```sh
sudo cp -r src /usr/local/lib/ice-gf66
sudo ln -s /usr/local/lib/ice-gf66/main.py /usr/local/bin/ice-gf66
```

You also need these dependencies for the program to work:
* `ec_sys` with `write_support=1` and `msr` kernel modules are loaded
```sh
sudo modprobe ec_sys write_support=1
sudo modprobe msr
```
* `msr_tools` package (can probably be found from your distro's repos)
* proprietary NVidia drivers

## Usage

```sh
ice-gf66 -h
```
to get a list of options available

Example:
```sh
sudo ice-gf66 -s sport -t 36 -u 88 -C 210,1695 -O 150
```
* Sets the shift/performance mode to sport/high
* Sets turbo ratio to 36 for each number of cores under load
    * Effectively limits CPU clock to 3.6GHz
* Sets undervolt of ~86mV
* Limits GPU clock to minimum of 210MHz and maximum of 1695MHz
* Sets GPU clock offset to +150MHz
    * The above two effectively undervolts GPU

You can put the command containing all your settings into a bash script
to be able execute with hotkeys/button presses etc.

## Other laptop models

Modern enough Intel processors (undervolting may not work on 12th Gen Alder Lake and later)
and NVidia GPUs (must have proprietary drivers) will probably work with this.

MSI Laptops have varying EC Memory layouts. For now you could look into the resources below
and patch the Python code yourself.
The `--dry` option can be used to verify if the executed commands will be correct

**Please don't fiddle around with the EC stuff without
patching the program first if you don't have the same laptop as mine. I don't know the
consequences of corrupting the EC memory**

## Resources

* https://github.com/BeardOverflow/msi-ec
* https://github.com/dmitry-s93/MControlCenter
* https://github.com/mihic/linux-intel-undervolt
* https://www.intel.com/content/dam/develop/external/us/en/documents/335592-sdm-vol-4.pdf
* https://github.com/NVIDIA/open-gpu-kernel-modules/discussions/236#discussioncomment-3553564

## Does it work?

```sh
sudo ice-gf66 -s sport -t 36 -u 80 -C 210,1695 -O 150
```
**Elden Ring, 1080p, High:**
| | Stock | With above settings |
| ---: | :---: | :---: |
| FPS | 60 | 60 |
| Stutters | more | less |
| CPU Temp | 90~95C | 75~85C |
| GPU Temp | 75~85C | 60~75C |
| GPU Power | 75W avg. | 55~65W |
| Margit beaten<br>from new<br>game save? | No, laptop got<br>too damn hot | Yes, easily |

Note: Your mileage will definitely vary