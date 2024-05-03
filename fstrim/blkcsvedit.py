import pandas as pd
import sys


fs = sys.argv[1]

def extract_records(fs, proc, event, rwbs, m_event, m_rwbs, f_proc, f_event, f_rwbs):
    # CSV 파일 읽기
    df = pd.read_csv(input_csv)

    # 조건에 맞는 레코드 추출
    fio = df[(df['Process'] == proc) & (df['Event'] == event) & (df['RWBS'] == rwbs)]
    
    discard = df[(df['Process'] == f_proc) & (df['Event'] == f_event) & (df['RWBS'] == f_rwbs)]
    
    meta = df[(df['Event'] == m_event) & (df['RWBS'] == m_rwbs)

    dfs = [fio, discard, meta]
    
    combined_df = pd.concat(dfs)
    # 새로운 CSV 파일로 저장
    combined_df.to_csv(fs + ".csv", index=False)

    


if fs=='ext4':

    extract_records(fs='ext4', proc='fio', event='D', rwbs='WS', m_event='C', m_rwbs='WM', f_proc='fstrim', f_event='I', f_rwbs='DS')


elif fs=='f2fs':

    extract_records(fs='f2fs', proc='fio', event='D', rwbs='WS', m_event='D', m_rwbs='WSM', f_proc='f2fs_discard-8:', f_event='I', f_rwbs='D')






