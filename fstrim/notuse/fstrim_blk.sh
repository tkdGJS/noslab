#!/bin/bash
#echo 3 > /proc/sys/vm/drop_caches
#
#sleep 1

blktrace -d /dev/nvme0n1p2 -o - | blkparse -i - -o tracefile &
blk=$!
echo "blktrace is $blk"

sleep 5

#dd if=/dev/zero of=output_file bs=4M count=1 
#truncate -s 1G output_file
fallocate -l 1G output_file
sleep 10

sync

sleep 10

rm output_file

sleep 10

sync

sleep 10

fstrim -av -o 538774272 -l 512099600384 -m 8


sleep 10

kill $blk
pkill -f blktrace
