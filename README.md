# AVB-Disabler

A simple graphical utility to disable **Android Verified Boot (AVB)** by patching `vbmeta.img` files.

This tool eliminates the need to flash the vbmeta via fastboot with the flags 
`--disable-verity --disable-verification` and allows flashing the patched file using 
[SP Flash Tool](https://spflashtool.com/) or [MTKClient](https://github.com/bkerler/mtkclient).

