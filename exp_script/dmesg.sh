#!bin/bash
filename=$1
dmesg -C

while true; do
	dmesg -c >> $filename-dmesg.txt
	sleep 1
done
