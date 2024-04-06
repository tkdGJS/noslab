#!/bin/bash
#echo 3 > /proc/sys/vm/drop_caches

fs="$1"

#실험 파일시스템에 대해 할당된 모든 블록을 초기화하기 위해 unmount, mount
sh $fs-mount.sh

sleep 5

fstrim -v -m 1 ./mnt

sleep 5

sync

sleep 5

#실험 시작
blktrace -d /dev/sda -o - | blkparse -i - -o $fs-tracefile &
blk=$!
echo "blktrace is $blk"

sleep 5

#>>>fio_test_normal.sh 1 8 cervical randrw 
fio \
--name=fstrim1 \
--ioengine=libaio \
--directory=./mnt \
--bs=512k \
--size=1G \
--direct=1 \
--thread \
--group_reporting \
--per_job_logs=0 \
--numjobs=1 \
--rw=write &
PID=$!
echo "FIO is $PID"

sleep 10

sync

sleep 10

rm ./mnt/fstrim1.0.0

sleep 10

sync

sleep 10

fstrim -v -m 1 ./mnt


sleep 10

kill $blk
pkill -f blktrace
