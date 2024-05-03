#!/bin/bash
#echo 3 > /proc/sys/vm/drop_caches

fs="$1"
bs="$2"
size="$3"
num="$4"
rw="$5"
discard="$6"

#실험 파일시스템에 대해 할당된 모든 블록을 초기화하기 위해 unmount, mount
sh $fs-mount.sh $discard

sleep 300

fstrim -v -m 1 ./mnt

sleep 300

sync

sleep 300

mkdir ./graph/$fs-$bs-$size-$num-$rw-fstrim/

#실험 시작
blktrace -d /dev/sda -o - | blkparse -i - -o ./graph/$fs-$bs-$size-$num-$rw-fstrim/$fs-tracefile &
blk=$!
echo "blktrace is $blk"

sleep 300

time1=$(date +%s.%N)
./fio_bg_fstrim.sh $bs $size $num $rw
time2=$(date +%s.%N)

diff=$(echo "$time2 - $time1" | bc)

sleep 300
echo "$fs-$bs-$size-$num-$rw-fstrim-direct, fio time is : $diff" >> result
kill $blk
pkill -f blktrace
