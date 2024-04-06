import pandas as pd
import matplotlib.pyplot as plt
import sys
import matplotlib.ticker as ticker


if __name__ == "__main__":
    if len(sys.argv) !=2:
        print("Usage: python3 blktocsv.py <file system>")
        sys.exit(1)



fs = sys.argv[1]
print("file system : ", fs)

def draw_graph(fio_off, fio_ln, fio_time, fstrim_off, fstrim_ln, fstrim_time, meta_off, meta_ln, meta_time, fs):

    plt.figure(figsize=(40,5))
    
    plt.subplots_adjust(top=0.85, bottom=0.2)
    plt.rc('font', size=30)        # 기본 폰트 크기
    plt.rc('axes', labelsize=30)   # x,y축 label 폰트 크기
    plt.rc('xtick', labelsize=20)  # x축 눈금 폰트 크기 
    plt.rc('ytick', labelsize=20)  # y축 눈금 폰트 크기
#    plt.rc('figure', titlesize=1000) # figure title 폰트 크기
    plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%g'))
    plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%g'))

    plt.title(fs + ' blktrace')
    plt.xlabel('Sector Address')
    plt.ylabel('Time(sec)')




    for i in range(len(fio_off)):
        plt.plot([fio_off[i], fio_ln[i]],[fio_time[i], fio_time[i]], color='gray',linewidth=6)



    plt.plot(fio_off,fio_time,'o',markersize=8,color='black')

    plt.plot(fio_ln,fio_time,'o',markersize=8,color='red')


    for i in range(len(fstrim_off)):
        plt.plot([fstrim_off[i], fstrim_ln[i]],[fstrim_time[i], fstrim_time[i]], color='gray',linewidth=6)



    plt.plot(fstrim_off,fstrim_time,'o',markersize=8,color='black')

    plt.plot(fstrim_ln,fstrim_time,'o',markersize=8,color='blue')

    for i in range(len(meta_off)):
        plt.plot([meta_off[i], meta_ln[i]],[meta_time[i], meta_time[i]], color='gray',linewidth=6)

    plt.plot(meta_off,meta_time,'o',markersize=8,color='green')

    plt.plot(meta_ln,meta_time,'o',markersize=8,color='green')

    plt.savefig(fs+'.png')

def fio_graph(offset, length, time, fs):

    name = str(fs)+'fio-graph'

    plt.figure(figsize=(40,5))

    plt.subplots_adjust(top=0.85, bottom=0.2)
    plt.rc('font', size=30)        # 기본 폰트 크기
    plt.rc('axes', labelsize=30)   # x,y축 label 폰트 크기
    plt.rc('xtick', labelsize=20)  # x축 눈금 폰트 크기 
    plt.rc('ytick', labelsize=20)  # y축 눈금 폰트 크기
#    plt.rc('figure', titlesize=1000) # figure title 폰트 크기
    plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%g'))
    plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%g'))


    plt.title(fs + ' fio blktrace')
    plt.xlabel('Sector Address')
    plt.ylabel('Time(sec)')



    for i in range(len(offset)):
        plt.plot([offset[i], length[i]],[time[i], time[i]], color='gray',linewidth=6)



    plt.plot(offset,time,'o',markersize=8,color='black')

    plt.plot(length,time,'o',markersize=8,color='red')


    plt.savefig(name+'.png')

def fstrim_graph(offset, length, time, fs):

    name = str(fs)+'fstrim-graph'

    plt.figure(figsize=(40,5))

    plt.subplots_adjust(top=0.85, bottom=0.2)
    plt.rc('font', size=30)        # 기본 폰트 크기
    plt.rc('axes', labelsize=30)   # x,y축 label 폰트 크기
    plt.rc('xtick', labelsize=20)  # x축 눈금 폰트 크기 
    plt.rc('ytick', labelsize=20)  # y축 눈금 폰트 크기
#    plt.rc('figure', titlesize=1000) # figure title 폰트 크기
    plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%g'))
    plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%g'))


    plt.title(fs + ' fstrim blktrace')
    plt.xlabel('Sector Address')
    plt.ylabel('Time(sec)')



    for i in range(len(offset)):
        plt.plot([offset[i], length[i]],[time[i], time[i]], color='gray',linewidth=6)



    plt.plot(offset,time,'o',markersize=8,color='black')

    plt.plot(length,time,'o',markersize=8,color='blue')


    plt.savefig(name+'.png')


def trace(fs, proc, event, rwbs, m_event, m_rwbs, f_proc, f_event, f_rwbs):


    df = pd.read_csv(fs + '-tracefile.csv')
    
    #print(df['Process'])
    
    #print(fio_df)
    
    #############################################
    #fio write 확인
    fio_df = df[df['Process'] == proc]
    fio_ws = fio_df[fio_df['RWBS'] == rwbs]
    
    fio_ws_d = fio_ws[fio_ws['Event'] == event]
    
    all_ws_d = fio_ws_d['Length'].sum(skipna=True)
    
    print("fio write size : ", (((all_ws_d * 512)/1024)/1024)/1024, ' GiB')
    #############################################
    #fio metadate write 확인
    #fio_df = df[df['Process'] == 'fio']
    fio_wm = df[df['RWBS'] == m_rwbs]
    
    fio_wm_c = fio_wm[fio_wm['Event'] == m_event]
    
    all_wm_c = fio_wm_c['Length'].sum(skipna=True)
    
    print("fio metadata write size : ", (((all_wm_c * 512)/1024)/1024)/1024 ,' GiB')
    #############################################
    fstrim_df = df[df['Process'] == f_proc]
    fstrim_ds = fstrim_df[fstrim_df['RWBS'] == f_rwbs]
    
    fstrim_ds_i = fstrim_ds[fstrim_ds['Event'] == f_event]

    
    all_ds_i = fstrim_ds_i['Length'].sum(skipna=True)
    
    print("fstrim discard size : ", (((all_ds_i * 512)/1024)/1024)/1024 ,' GiB')
    #############################################
     
#    assert False

    fio_access_len = fio_ws_d['Offset'].dropna() + fio_ws_d['Length'].dropna()
    
    fio_min_addr = fio_ws_d['Offset'].min()
    fio_max_addr = fio_access_len.max()
    
#    print(fio_min_addr)
#    print(fio_max_addr)
    
    meta_access_len = fio_wm_c['Offset'].dropna() + fio_wm_c['Length'].dropna()
    
    meta_off = fio_wm_c['Offset'].values
    meta_ln = meta_access_len.values
    meta_time = fio_wm_c['Time'].values

    print(len(meta_off))
    print(len(meta_ln))
    print(len(meta_time))

#    assert False


#    print(meta_min_addr)
#    print(meta_max_addr)
    
    fstrim_access_len = fstrim_ds_i['Offset'].dropna() + fstrim_ds_i['Length'].dropna()
    
    fstrim_min_addr = fstrim_ds_i['Offset'].min()
    fstrim_max_addr = fstrim_access_len.max()
    
    fio_off = fio_ws_d['Offset'].values
    fio_ln = fio_access_len.values
    fio_time = fio_ws_d['Time'].values
    
    
    fstrim_off = fstrim_ds_i['Offset'].values
    fstrim_ln = fstrim_access_len.values
    fstrim_time = fstrim_ds_i['Time'].values
    
    
    draw_graph(fio_off,fio_ln,fio_time, fstrim_off,fstrim_ln,fstrim_time,meta_off, meta_ln, meta_time, fs)
    
    fio_graph(fio_off,fio_ln,fio_time,fs)
    
    fstrim_graph(fstrim_off,fstrim_ln,fstrim_time, fs)

if fs=='ext4':

    trace(fs='ext4', proc='fio', event='D', rwbs='WS', m_event='C', m_rwbs='WM', f_proc='fstrim', f_event='I', f_rwbs='DS')

elif fs=='xfs':

    trace(fs='xfs', proc='fio', event='D', rwbs='WS', m_event='C', m_rwbs='WM', f_proc='fstrim', f_event='I', f_rwbs='DS')

elif fs=='f2fs':

    trace(fs='f2fs', proc='fio', event='D', rwbs='WS', m_event='D', m_rwbs='WSM', f_proc='f2fs_discard-8:', f_event='I', f_rwbs='D')

elif fs=='btrfs':

    trace(fs='btrfs', proc='fio', event='D', rwbs='WS', m_event='D', m_rwbs='WSM', f_proc='fstrim', f_event='I', f_rwbs='DS')




