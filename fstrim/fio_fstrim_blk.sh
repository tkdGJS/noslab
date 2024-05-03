#!/bin/bash
#echo 3 > /proc/sys/vm/drop_caches

fs="$1"
bs="$2"
size="$3"
num="$4"
rw="$5"

#실험 파일시스템에 대해 할당된 모든 블록을 초기화하기 위해 unmount, mount
sh $fs-mount.sh

sleep 300

fstrim -v -m 1 ./mnt

sleep 300

sync

sleep 300

mkdir ./graph/$bs-$size-$num-$rw/

#실험 시작
blktrace -d /dev/sda -o - | blkparse -i - -o ./graph/$bs-$size-$num-$rw/$fs-tracefile &
blk=$!
echo "blktrace is $blk"

sleep 300

#--buffered=0 \
#>>>fio_test_normal.sh 1 8 cervical randrw 
fio \
--name=fstrim1 \
--ioengine=libaio \
--directory=./mnt \
--bs=$bs \
--size=$size \
--direct=0 \
--buffered=1 \
--thread \
--group_reporting \
--per_job_logs=0 \
--numjobs=$num \
--rw=$rw 


sleep 300

sync

sleep 300

rm ./mnt/*

sleep 300

sync

sleep 300

time1=$(date +%s.%N)
fstrim -v -m 1 ./mnt
time2=$(date +%s.%N)

diff=$(echo "$time2 - $time1" | bc)

sleep 300
echo "$fs-$bs-$size-$num-$rw, fstrim time is : $diff" >> result
kill $blk
pkill -f blktrace
