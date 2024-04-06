#===========================================================================
#[S.L]
#cgroup 서브시스템에 shell을 이미 할당한 상태
#cpu core 사용 개수를 조작하는 코드
#$core = 조작할 core 개수, "0-n" 으로 표현
##==========================================================================
#echo 'base+q+th'
#for dataset in "covid"
#do
#	
#	echo "cash, memory drop start"
#	sudo sh drop_cache.sh
#	echo "cash, memory drop end"
#	rm -rf ./fio_test/$dataset-checkpoint
#	echo 'rm checkpoint'
#	mkdir ./fio_test/$dataset-checkpoint
#	echo 'mk checkpoint'
#	sleep 10
#	
#	echo "fio test start"
#	fio \
#	--name=64-test \
#	--ioengine=libaio \
#	--directory=../fio_test/fio_dump \
#	--runtime=80000 \
#	--bs=4k \
#	--size=1G \
#	--direct=0 \
#	--time_based=1 \
#	--randrepeat=0 \
#	--norandommap=1 \
#	--thread \
#	--group_reporting \
#	--per_job_logs=0 \
#	--allow_mounted_write=1 \
#	--numjobs=64 \
#	--rw=randrw & 
#	PID=$!
#	echo "fio test ,,,"
#	echo "$PID"
#	sleep 20
#
#	echo "python start $dataset"
#	python3 $dataset-base+q+th.py 1> $dataset-base+q+th.txt
#	ls -lh ./fio_test/$dataset-checkpoint/ > $dataset-base+q+th-vol.txt
#	echo "python end $dateset"
#	
#	echo "kill start $PID"
#	kill -9 $PID
#	echo "kill end $PID"
#	sleep 30
#
#done
#
#
echo "base+th"
for dataset in "covid"
do
	
	echo "cash, memory drop start"
	sudo sh drop_cache.sh
	echo "cash, memory drop end"
	rm -rf ./fio_test/$dataset-checkpoint
	echo 'rm checkpoint'
	mkdir ./fio_test/$dataset-checkpoint
	echo 'mk checkpoint'
	sleep 10

	echo "fio test start"
	fio \
	--name=64-test \
	--ioengine=libaio \
	--directory=../fio_test/fio_dump \
	--runtime=80000 \
	--bs=4k \
	--size=1G \
	--direct=0 \
	--time_based=1 \
	--randrepeat=0 \
	--norandommap=1 \
	--thread \
	--group_reporting \
	--per_job_logs=0 \
	--allow_mounted_write=1 \
	--numjobs=64 \
	--rw=randrw & 
	PID=$!
	echo "fio test ,,,"
	echo "$PID"
	sleep 20

	echo "python start $dataset"
	python3 $dataset-base+th.py 1> $dataset-base+th.txt
	ls -lh ./fio_test/$dataset-checkpoint/ > $dataset-base+th-vol.txt
	echo "python end $dateset"

	echo "kill start $PID"
	kill -9 $PID
	echo "kill end $PID"
	sleep 30  	

done


echo "base"
for dataset in "covid"
do
	
	echo "cash, memory drop start"
	sudo sh drop_cache.sh
	echo "cash, memory drop end"
	rm -rf ./fio_test/$dataset-checkpoint
	echo 'rm checkpoint'
	mkdir ./fio_test/$dataset-checkpoint
	echo 'mk checkpoint'
	sleep 10

	echo "fio test start"
	fio \
	--name=64-test \
	--ioengine=libaio \
	--directory=../fio_test/fio_dump \
	--runtime=80000 \
	--bs=4k \
	--size=1G \
	--direct=0 \
	--time_based=1 \
	--randrepeat=0 \
	--norandommap=1 \
	--thread \
	--group_reporting \
	--per_job_logs=0 \
	--allow_mounted_write=1 \
	--numjobs=64 \
	--rw=randrw & 
	PID=$!
	echo "fio test ,,,"
	echo "$PID"
	sleep 20

	echo "python start $dataset"
	python3 $dataset-base.py 1> $dataset-base.txt
	ls -lh ./fio_test/$dataset-checkpoint/ > $dataset-base-vol.txt
	echo "python end $dateset"

	echo "kill start $PID"
	kill -9 $PID
	echo "kill end $PID"
	sleep 30  	

done


echo "base+q"
for dataset in "covid"
do
	
	echo "cash, memory drop start"
	sudo sh drop_cache.sh
	echo "cash, memory drop end"
	rm -rf ./fio_test/$dataset-checkpoint
	echo 'rm checkpoint'
	mkdir ./fio_test/$dataset-checkpoint
	echo 'mk checkpoint'
	sleep 10

	echo "fio test start"
	fio \
	--name=64-test \
	--ioengine=libaio \
	--directory=../fio_test/fio_dump \
	--runtime=80000 \
	--bs=4k \
	--size=1G \
	--direct=0 \
	--time_based=1 \
	--randrepeat=0 \
	--norandommap=1 \
	--thread \
	--group_reporting \
	--per_job_logs=0 \
	--allow_mounted_write=1 \
	--numjobs=64 \
	--rw=randrw & 
	PID=$!
	echo "fio test ,,,"
	echo "$PID"
	sleep 20

	echo "python start $dataset"
	python3 $dataset-base+q.py 1> $dataset-base+q.txt
	ls -lh ./fio_test/$dataset-checkpoint/ > $dataset-base+q-vol.txt
	echo "python end $dateset"

	echo "kill start $PID"
	kill -9 $PID
	echo "kill end $PID"
	sleep 30  	

done
