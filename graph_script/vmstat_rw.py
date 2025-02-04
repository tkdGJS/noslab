import os
import pandas as pd
import matplotlib.pyplot as plt
import re

import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter

# 디렉토리 경로 설정
directory_path = './'

# 파일 목록 가져오기
files = [f for f in os.listdir(directory_path) if f.endswith('.vmstat')]

btrfs_files = [f for f in files if '' in f]
ext4_files = [f for f in files if 'Warm' in f]
xfs_files = [f for f in files if 'Cold' in f]
jfs_files = [f for f in files if 'Mix' in f]

# 데이터를 저장할 딕셔너리 초기화
data_dict = {
    'Hot': {},
    'Warm': {},
    'Cold': {},
    'Mix': {},
}

# 파일 읽기 및 데이터프레임 생성 함수
def read_vmstat_file(filepath):
    with open(filepath, 'r') as file:
        log_content = file.readlines()
    columns = log_content[1].strip().split()
    data = [line.strip().split() for line in log_content[2:] if line.strip() and not line.startswith('procs')]

    # 데이터프레임 생성
    df = pd.DataFrame(data, columns=columns)

    # 데이터프레임에서 숫자로 변환할 수 없는 값이 있는 행을 제거
    df = df.apply(pd.to_numeric, errors='coerce').dropna()

    return df

# 파일별 데이터 읽기
for file in btrfs_files:
    filepath = os.path.join(directory_path, file)
    data_dict['Hot'][file] = read_vmstat_file(filepath)

for file in ext4_files:
    filepath = os.path.join(directory_path, file)
    data_dict['Warm'][file] = read_vmstat_file(filepath)

for file in xfs_files:
    filepath = os.path.join(directory_path, file)
    data_dict['Cold'][file] = read_vmstat_file(filepath)

for file in jfs_files:
    filepath = os.path.join(directory_path, file)
    data_dict['Mix'][file] = read_vmstat_file(filepath)
# 파일 읽기 및 데이터프레임 생성 함수
def read_vmstat_file(filepath):
    with open(filepath, 'r') as file:
        log_content = file.readlines()
    columns = log_content[1].strip().split()
    data = [line.strip().split() for line in log_content[2:] if line.strip() and not line.startswith('procs')]
    
    # 데이터프레임 생성
    df = pd.DataFrame(data, columns=columns)
    
    # 데이터프레임에서 숫자로 변환할 수 없는 값이 있는 행을 제거
    df = df.apply(pd.to_numeric, errors='coerce').dropna()
    
    return df



def save_plot_dual(df_list1, df_list2, ylabel1, ylabel2, title, filename):
    plt.figure(figsize=(12, 6))
    for df, label in df_list1:
        plt.plot(df.index.values, df[ylabel1].values, label=f"Read", color='blue')

    for df, label in df_list2:
        plt.plot(df.index.values, df[ylabel2].values, label=f"Write", linestyle="dashed", color='red')

    plt.xlabel('Time (sec)', fontsize=14)
    plt.ylabel(f'Throughput (block/sec)', fontsize=14)
    plt.title(title, fontsize=16)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{filename}.png', bbox_inches='tight')
    plt.close()

# 각 파일 시스템의 데이터를 결합한 리스트 생성
def create_df_list(metric):
    df_list = []
    for fs_type, fs_data in data_dict.items():
        for file, df in fs_data.items():
            if metric in df.columns:
                df_list.append((df, file))
    return df_list

def calculate_bo_mean(df):
    if 'bo' not in df.columns:
        return None
    if len(df) <= 60:
        return df['bo'].mean()  # 데이터가 적으면 전체 평균

    return df['bo'].iloc[30:-30].mean()

bo_means = {}

for fs_type, fs_data in data_dict.items():
    bo_means[fs_type] = {}
    for file, df in fs_data.items():
        bo_means[fs_type][file] = calculate_bo_mean(df)

# bo 평균값 출력
for fs_type, fs_files in bo_means.items():
    print(f"파일 시스템 유형: {fs_type}")
    for file, mean_value in fs_files.items():
        print(f"파일: {file}, bo 평균 처리량: {mean_value}")

df_list_bi = create_df_list('bi')
df_list_bo = create_df_list('bo')
save_plot_dual(df_list_bi, df_list_bo, 'bi', 'bo', 'File Systems Comparison - bi & bo', 'comparison_bi_bo')
