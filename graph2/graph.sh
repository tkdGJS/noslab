#!/bin/bash
#python3 vmstat_rw.py &
python3 iostat.py &

#grep "D" tracefile >> D_trace

python3 blktocsv.py

#python3 blkgraph-W.py

#python3 blkgraph-R.py

#python3 blkgraph-D.py

#python3 blkgraph-CD.py
#python3 blkgraph-RD.py
#python3 blkgraph-RA.py
#python3 blkgraph-RM.py
python3 blkgraph-RWRAWS.py
