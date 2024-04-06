
for fs in "ext4" "f2fs"
    for bs in "512K"
	do
		for size in "1G"
		do
			for rw in "write"
			do
				for num in "1" "2" "4" "8" "16" "32" "64" "128"
				do
					sh fio_fstrim_blk.sh $fs $bs $size $num $rw
				done
			done
		done
	done
