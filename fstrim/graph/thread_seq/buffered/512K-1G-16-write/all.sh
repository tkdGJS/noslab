python3 blktocsv.py ext4
python3 blktocsv.py f2fs
python3 blktocsv.py xfs
python3 blktocsv.py btrfs





python3 -W ignore blkgraph.py ext4 &

sleep 5

python3 -W ignore blkgraph.py f2fs &

sleep 5
python3 -W ignore blkgraph.py xfs &

sleep 5
python3 -W ignore blkgraph.py btrfs &
