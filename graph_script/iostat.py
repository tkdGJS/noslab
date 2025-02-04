import pandas as pd
import matplotlib.pyplot as plt
import re
import os
import glob

# 각 iostat 로그 파일 처리 함수
def process_iostat_file(file_path):
    # 파일 읽기
    with open(file_path, 'r') as file:
        log_data = file.readlines()

    # /dev/sda 데이터 필터링
    sda_data = []
    header = None
    pattern = re.compile(r'^\s*sda\s+')

    for line in log_data:
        if line.startswith('Device'):
            header = line
        elif pattern.match(line):
            sda_data.append(line)

    # 헤더와 sda 데이터를 결합
    if header:
        sda_data.insert(0, header)

    # DataFrame으로 변환
    df = pd.DataFrame([x.split() for x in sda_data[1:]], columns=sda_data[0].split())

    # 열을 숫자로 변환
    numeric_columns = ['wMB/s', 'rMB/s', '%util', 'r/s', 'rrqm/s', 'wrqm/s', 'r_await', 'w_await', 'rareq-sz', 'wareq-sz', 'aqu-sz', 'd/s']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df, os.path.basename(file_path)

# 파일 패턴별로 색상을 지정하는 함수
def get_color_by_pattern(label):
    if 'f2fs' in label:
        return 'orange'
    return 'black'  # 기본 색상

# 그래프 저장 함수 정의
def save_plot(df_list, ylabel, title, filename):
    plt.figure(figsize=(12, 6))
    for df, label in df_list:
        color = get_color_by_pattern(label)
        plt.plot(df.index.values, df[ylabel].values, label=label, color=color)
    plt.xlabel('Time (index)')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # 그래프 밖 오른쪽 중앙에 레전드 배치
    plt.grid(True)
    plt.savefig(f'{filename}.png', bbox_inches='tight')  # bbox_inches='tight'로 그래프와 레전드를 모두 포함하도록 설정
    plt.close()

# iostat 로그 파일이 있는 디렉토리 위치
file_dir = './'

# 파일 패턴별로 파일 찾기
f2fs_files = glob.glob(os.path.join(file_dir, 'o..iostat'))

# 모든 파일 리스트를 하나로 결합
all_files = f2fs_files

# 파일 처리 후 데이터 리스트 생성
df_list = []
for file_path in all_files:
    df, label = process_iostat_file(file_path)
    df_list.append((df, label))

def calculate_wMB_mean(df):
    if 'wMB/s' not in df.columns:
        return None
    return df['wMB/s'].mean()

wMB_means = {}

for df, label in df_list:
    wMB_means[label] = calculate_wMB_mean(df)

# 평균값 출력
for label, mean_value in wMB_means.items():
    print(f"파일: {label}, wMB/s 평균 처리량: {mean_value}")
def save_plot_dual(df_list, ylabel1, ylabel2, title, filename):
    plt.figure(figsize=(12, 6))

    for df, label in df_list:
        plt.plot(df.index.values, df[ylabel1].values, label=f"Read", color='blue')

    for df, label in df_list:
        plt.plot(df.index.values, df[ylabel2].values, label=f"Write", linestyle="dashed", color='red')

    plt.xlabel('Time (index)')
    plt.ylabel('Throughput (MB/s)')
    plt.title(title)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.savefig(f'{filename}.png', bbox_inches='tight')
    plt.close()

# 수정된 그래프 생성
save_plot_dual(df_list, 'rMB/s', 'wMB/s', 'Read & Write MB/s Comparison', 'Read_Write_mbs_comparison')



