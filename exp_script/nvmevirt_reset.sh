#bin/bash

umount /dev/nvme1n1p1

lsmod | grep "nvmev"

rmmod "nvmev"

lsmod | grep "nvmev"

insmod /lib/modules/5.15.0/nvmevirt/nvmev.ko memmap_start=14G memmap_size=16G cpus=7,8

sleep 5

lsblk | grep "nvme1n1"

lsmod | grep "nvmev"
