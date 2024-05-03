
for fs in "ext4" "f2fs"
do
    for bs in "1M"
	do
		for size in "128M"
		do
			for rw in "randwrite"
			do
				for num in "1000"
				do
					for discard in "discard" "nodiscard"
					do
						sync && echo 3 >> /proc/sys/vm/drop_caches
						sleep 10
						echo "drop caches"
						sh fio_100_replay.sh $fs $bs $size $num $rw $discard

						sleep 300
					done
				done
			done
		done
	done
done

sync && echo 3 >> /proc/sys/vm/drop_caches
sleep 10
sh fio_100_fstrim.sh ext4 1M 128M randwrite 1000 nodiscard
sleep 300
sync && echo 3 >> /proc/sys/vm/drop_caches
sleep 10
sh fio_100_fstrim.sh f2fs 1M 128M randwrite 1000 nodiscard
sleep 300
