#bin/bash

sudo umount /dev/sda1
sudo rmmod f2fs
sudo make -j 24 M=fs/f2fs modules
sudo make -j 24 M=fs/f2fs modules_install
ls -l /lib/modules/$(uname -r)/extra/f2fs.ko
cp /lib/modules/$(uname -r)/extra/f2fs.ko /lib/modules/$(uname -r)/kernel/fs/f2fs/f2fs.ko

modprobe f2fs

