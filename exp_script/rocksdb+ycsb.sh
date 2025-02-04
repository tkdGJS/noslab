#!/bin/bash
workload=$1
recordcount=$2

# MySQL 접속 정보

# YCSB 경로
YCSB_BIN="/home/tkdgjs/workspace/YCSB/bin/ycsb"
YCSB_WORKLOAD="/home/tkdgjs/workspace/YCSB/workloads/workloada"


load_data() {
  echo "Loading data into MySQL..."
  $YCSB_BIN load rocksdb -P workloads/workload$workload \
    -P db.properties \
    -p recordcount=$recordcount
  echo "Data load complete."
}

run_test() {
  echo "Run data into MySQL..."
  $YCSB_BIN run rocksdb -P workloads/workload$workload \
    -P db.properties \
    -p recordcount=$recordcount
  echo "Data run complete."
}

echo "Starting experiment..."
#initialize_database
load_data
run_test
#run_test >> result_mysql+ycsb
echo "Experiment complete."

