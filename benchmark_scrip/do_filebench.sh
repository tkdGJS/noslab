#!/bin/bash

# 인자를 각각 변수로 받음
workload=$1
filesize=${2:-1m}     # 기본값 1m
nfiles=${3:-4000}     # 기본값 4000
nthreads=${4:-20}     # 기본값 20
iosize=${5:-512k}     # 기본값 512k
dir=${6:-./mnt}       # 기본값 ./mnt

# filebench 명령 실행
sudo filebench << EOF
load $workload
set \$filesize=$filesize
set \$nfiles=$nfiles
set \$nthreads=$nthreads
set \$iosize=$iosize
set \$dir=$dir
run 60
EOF

