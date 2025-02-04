#!/bin/bash

# 대상 디스크 경로
TARGET_DIR="/sys/fs/f2fs/sda1"

# 출력 파일 경로
OUTPUT_FILE=$1

# 파일 초기화
echo "" > "$OUTPUT_FILE"

# 디렉토리 내 모든 항목 순회
for ITEM in "$TARGET_DIR"/*
do
  # 파일인지 확인
  if [ -f "$ITEM" ]; then
    # 항목 이름 추출
    ITEM_NAME=$(basename "$ITEM")
    # 값 읽기
    ITEM_VALUE=$(cat "$ITEM" 2>/dev/null || echo "읽기 실패")
    # 결과 파일에 추가
    echo "$ITEM_NAME: $ITEM_VALUE" >> "$OUTPUT_FILE"
  fi
done

cat /sys/kernel/debug/f2fs/status >> "$OUTPUT_FILE"

