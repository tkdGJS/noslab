#!/bin/bash

# 사용법: ./send_email_msmtp.sh "수신자 이메일" "메일 제목" "메일 본문" "/path/to/image.jpg"

# 입력 인자 확인
if [ "$#" -ne 4 ]; then
    echo "사용법: $0 \"수신자 이메일\" \"메일 제목\" \"메일 본문\" \"사진 파일 경로\""
    exit 1
fi

# 변수 설정
RECIPIENT="$1"
SUBJECT="$2"
BODY="$3"
IMAGE_PATH="$4"

# 파일 존재 확인
if [ ! -f "$IMAGE_PATH" ]; then
    echo "오류: 지정한 파일이 존재하지 않습니다: $IMAGE_PATH"
    exit 1
fi

# MIME 바운더리 설정
BOUNDARY="boundary_$(date +%s)"

# 이메일 내용 생성 (MIME 형식)
EMAIL_CONTENT=$(cat <<EOF
From: Your Name <your-email@gmail.com>
To: $RECIPIENT
Subject: $SUBJECT
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="$BOUNDARY"

--$BOUNDARY
Content-Type: text/plain; charset="UTF-8"
Content-Transfer-Encoding: 7bit

$BODY

--$BOUNDARY
Content-Type: image/jpeg
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename="$(basename $IMAGE_PATH)"

$(base64 "$IMAGE_PATH")

--$BOUNDARY--
EOF
)

# 이메일 전송 (msmtp 사용)
echo "$EMAIL_CONTENT" | msmtp --debug --from=default -t "$RECIPIENT"

echo "📩 메일이 $RECIPIENT 로 전송되었습니다!"

