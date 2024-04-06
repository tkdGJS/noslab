#===========================================================================
#[S.L]
#cgroup 서브시스템에 shell을 이미 할당한 상태
#cpu core 사용 개수를 조작하는 코드
#$core = 조작할 core 개수, "0-n" 으로 표현
##==========================================================================
echo 'test start'
echo "cash, memory drop start"
#sudo sync && echo 3 >> /proc/sys/vm/drop_caches
echo "cash, memory drop end"
for dataset in "cervical"
do
	rm -rf ./fio_test/$dataset-checkpoint
	echo 'rm checkpoint'
	mkdir ./fio_test/$dataset-checkpoint
	echo 'mk checkpoint'
	sleep 20

	echo "python start $dataset"
	python3 $dataset-uniform_batch24.py 1> $dataset-thread.txt
	ls -lh ./fio_test/$dataset-checkpoint/ > $dataset-thread-vol.txt
	echo "python end $dateset"
done



