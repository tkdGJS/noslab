#!/bin/bash

# MySQL 접속 정보
DB_HOST="localhost"
DB_PORT="3306"
DB_NAME="testdb"
DB_USER="root"
DB_PASS="1234"
MYSQL_CMD="mysql -u$DB_USER -p$DB_PASS -h$DB_HOST -P$DB_PORT"

# YCSB 경로
YCSB_BIN="/home/tkdgjs/workspace/YCSB/bin/ycsb"
YCSB_WORKLOAD="/home/tkdgjs/workspace/YCSB/workloads/workloada"
YCSB_JDBC_DRIVER="/home/tkdgjs/workspace/YCSB/lib/mysql-connector-java-8.0.33.jar"
DB_HOST="localhost"
DB_PORT="3306"
DB_NAME="testdb"
DB_USER="root"
DB_PASS="1234"
MYSQL_CMD="mysql -u$DB_USER -p$DB_PASS -h$DB_HOST -P$DB_PORT"

echo "Dropping existing database (if any)..."
$MYSQL_CMD -e "DROP DATABASE IF EXISTS $DB_NAME;"


echo "Creating database..."
$MYSQL_CMD -e "CREATE DATABASE $DB_NAME;"
$MYSQL_CMD -D $DB_NAME -e "CREATE TABLE usertable (
    YCSB_KEY VARCHAR(255) PRIMARY KEY,
    FIELD0 TEXT,
    FIELD1 TEXT,
    FIELD2 TEXT,
    FIELD3 TEXT,
    FIELD4 TEXT,
    FIELD5 TEXT,
    FIELD6 TEXT,
    FIELD7 TEXT,
    FIELD8 TEXT,
    FIELD9 TEXT
);"


# 데이터 로드 함수
load_data() {
  echo "Loading data into MySQL..."
  $YCSB_BIN load jdbc -P $YCSB_WORKLOAD \
    -p db.driver=com.mysql.cj.jdbc.Driver \
    -p db.url=jdbc:mysql://$DB_HOST:$DB_PORT/$DB_NAME \
    -p db.user=$DB_USER \
    -p db.passwd=$DB_PASS \
    -cp $YCSB_JDBC_DRIVER
  echo "Data load complete."
}

# 성능 테스트 함수
run_test() {
  echo "Running YCSB test..."
  $YCSB_BIN run jdbc -P $YCSB_WORKLOAD \
    -p db.driver=com.mysql.cj.jdbc.Driver \
    -p db.url=jdbc:mysql://$DB_HOST:$DB_PORT/$DB_NAME \
    -p db.user=$DB_USER \
    -p db.passwd=$DB_PASS \
    -cp $YCSB_JDBC_DRIVER
  echo "Test complete."
}

# 메인 실행 순서
echo "Starting experiment..."
#initialize_database
load_data
run_test
#run_test >> result_mysql+ycsb
echo "Experiment complete."

