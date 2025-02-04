# 파일 내 특정 로그 개수 세기 및 출력
def count_logs(file_path, keyword):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # keyword를 포함한 라인의 개수 카운팅
        count = sum(1 for line in lines if keyword in line)

        # 결과 출력
        print(f"'{keyword}'를 포함하는 로그의 개수: {count}")

    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
# 사용 예시
file_path = "mix-dmesg.txt"  # 로그 파일 경로를 입력
keyword = "[NVMEVIRT] do_gc call"
count_logs(file_path, keyword)
