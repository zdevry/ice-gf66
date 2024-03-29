# Control centre for MSI GF66 Laptops running Linux

This program is a CLI that runs commands under the hood to control some system settings.

**DISCLAIMER**

This program is only written to work on my MSI laptop (MSI Katana GF66 11UE).
And most probably won't work on yours (especially the EC controller memory stuff).
See below if you still wish to use the program. But:  
**USING THIS PROGRAM ON ANOTHER LAPTOP MODEL, OR USING THIS PROGRAM IMPROPERLY
MAY CAUSE PERMANENT DAMAGE TO YOUR SYSTEM.  
YOU HAVE BEEN WARNED.**

I wrote this to be able to conveniently undervolt my Laptop and read/write
to EC memory to control stuff like performance and fan modes and also battery limits
(normally this would be done with MSI Center on Windows).
Technically this can be done with Bash scripts but I decided to do it the hard way instead.

This is currently a work in progress but it is enough for my setup to be able to
achieve lower temps when gaming on Linux.

Currently the program can:
* Set battery limit
* Set shift/performance mode
* Set fan mode
* Turn cooler boost on and off
* Set turbo boost ratios for Intel CPU
* Undervolt Intel CPU
* Set NVidia GPU clock limit
* Set NVidia GPU clock offset
    * The above two combined allows you to undervolt NVidia GPU

## Installation and Requirements

Copy the src folder to somewhere on your computer, e.g. `/usr/local/lib/`,
then create a symlink to main.py somewhere that is on your path, e.g. `/usr/local/bin/`
```sh
sudo cp src /usr/local/lib/ice-gf66
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

Examples:

```sh
ice-gf66 -u
```
Prints the current value of CPU undervolt

```sh
ice-gf66 -c
```
Toggles cooler boost

```sh
ice-gf66 -b 60
```
Sets battery charging limit to 60%
(Stops charging at 60, allows battery to drop to 50, then start charging again)

```sh
ice-gf66 -s sport -t 36 -u 88 -C 210,1695 -O 150
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
