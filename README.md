# Control centre for MSI GF66 Laptops running Linux

Currently doing a total rewrite on this branch.
- [ ] Totally changing the interface to use TOML (or JSON?)
files for configuration and profiles
- [ ] Putting everything in one file? (idk, and another(?))
- [ ] Rewriting the NVIDIA module to use NVML so that it works on Wayland
(or rather does not require Xorg ran as root to set clock offsets)
- [ ] Manually writing to MSR registers to remove msr-tools dependency