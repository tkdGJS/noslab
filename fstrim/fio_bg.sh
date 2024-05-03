#!/bin/bash
bs="$1"
size="$2"
num="$3"
rw="$4"


fio \
--name=dump \
--ioengine=libaio \
--directory=./mnt \
--bs=10M \
--size=1G \
--direct=1 \
--buffered=0 \
--numjobs=128 \
--rw=write 


time1=$(date +%s.%N)
for i in {1..10}
do
	fio \
	--name=fio_dump \
	--ioengine=libaio \
	--directory=./mnt \
	--bs=$bs \
	--size=$size \
	--direct=0 \
	--buffered=1 \
	--numjobs=$num \
	--rw=$rw 


	sync
	rm ./mnt/fio_dump*
	sync

done
time2=$(date +%s.%N)

diff=$(echo "$time2 - $time1" | bc)

echo "script-direct-$bs-$size-$num-$rw-$discard, fio time is : $diff" >> result
sleep 300
