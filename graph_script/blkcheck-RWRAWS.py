import pandas as pd
import matplotlib.pyplot as plt
import sys
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter

ymin, ymax = 0, 67108864/2
y_padding = 0.1 * (ymax - ymin)



def fio_graph(offset, length, time, offset2, length2, time2, offset3, length3, time3, offset4, length4, time4, fs):

    name = str(fs)+'RWRAWS'

    plt.figure(figsize=(30, 12))

    plt.subplots_adjust(top=0.85, bottom=0.2)
    plt.rc('font', size=30)        # 기본 폰트 크기
    plt.rc('axes', labelsize=30)   # x,y축 label 폰트 크기
    plt.rc('xtick', labelsize=20)  # x축 눈금 폰트 크기 
    plt.rc('ytick', labelsize=20)  # y축 눈금 폰트 크기

#    plt.rc('figure', titlesize=1000) # figure title 폰트 크기
    plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%g'))
    plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%g'))


    plt.title(fs + ' blktrace')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Sector Address')
    plt.ylim(ymin, ymax)
#    for i in range(len(offset)):
#        plt.plot([time[i], time[i]], [offset[i], length[i]], color='blue', linewidth=4)

    plt.plot(time, offset, 'x', markersize=4, color='blue')
    plt.plot(time2, length2, 'x', markersize=4, color='red')
    plt.plot(time3, offset3, 'o', markersize=4, color='blue')
    plt.plot(time4, length4, 'o', markersize=4, color='red')    
    plt.grid(True)
    plt.savefig(name+'.png')




def trace(fs, proc, event, rwbs, rwbs2, rwbs3, rwbs4, rwbs5):


    df = pd.read_csv('tracefile.csv')
    
    #print(df['Process'])
    
    #print(fio_df)
    
    #############################################
    #fio write 확인
    fio_df = df
    #fio_df = df[df['Process'] == f_proc]
    fio_ws = fio_df[fio_df['RWBS'] == rwbs]
    fio_ws2 = fio_df[fio_df['RWBS'] == rwbs2]
    
    fio_ws_d = fio_ws[fio_ws['Event'] == event]
    fio_ws_d2 = fio_ws2[fio_ws2['Event'] == event]
    
    all_ws_d = fio_ws_d['Length'].sum(skipna=True)
    all_ws_d2 = fio_ws_d2['Length'].sum(skipna=True)
    
    print("RA size : ", (((all_ws_d * 512)/1024)/1024)/1024, ' GiB')
    print("RA count : ", len(fio_ws_d))
    print("WS size : ", (((all_ws_d2 * 512)/1024)/1024)/1024, ' GiB')
    print("WS count : ", len(fio_ws_d2))
    #############################################

    fio_access_len = fio_ws_d['Offset'].dropna() + fio_ws_d['Length'].dropna()
    fio_access_len2 = fio_ws_d2['Offset'].dropna() + fio_ws_d2['Length'].dropna()
    
    fio_off = fio_ws_d['Offset'].values
    fio_ln = fio_access_len.values
    fio_time = fio_ws_d['Time'].values
    
    fio_off2 = fio_ws_d2['Offset'].values
    fio_ln2 = fio_access_len2.values
    fio_time2 = fio_ws_d2['Time'].values
    
#=========
    fio_ws3 = fio_df[fio_df['RWBS'] == rwbs3]
    fio_ws4 = fio_df[fio_df['RWBS'] == rwbs4]
    
    fio_ws_d3 = fio_ws3[fio_ws3['Event'] == event]
    fio_ws_d4 = fio_ws4[fio_ws4['Event'] == event]
    
    all_ws_d3 = fio_ws_d3['Length'].sum(skipna=True)
    all_ws_d4 = fio_ws_d4['Length'].sum(skipna=True)
    
    print("R size : ", (((all_ws_d3 * 512)/1024)/1024)/1024, ' GiB')
    print("R count : ", len(fio_ws_d3))
    print("W size : ", (((all_ws_d4 * 512)/1024)/1024)/1024, ' GiB')
    print("W count : ", len(fio_ws_d4))
    #############################################

    fio_access_len3 = fio_ws_d3['Offset'].dropna() + fio_ws_d3['Length'].dropna()
    fio_access_len4 = fio_ws_d4['Offset'].dropna() + fio_ws_d4['Length'].dropna()
    
    fio_off3 = fio_ws_d3['Offset'].values
    fio_ln3 = fio_access_len3.values
    fio_time3 = fio_ws_d3['Time'].values
    
    fio_off4 = fio_ws_d4['Offset'].values
    fio_ln4 = fio_access_len4.values
    fio_time4 = fio_ws_d4['Time'].values

#====================
    fio_ws5 = fio_df[fio_df['RWBS'] == rwbs5]
    
    fio_ws_d5 = fio_ws5[fio_ws5['Event'] == event]
    
    all_ws_d5 = fio_ws_d5['Length'].sum(skipna=True)
    
    print("WSM size : ", (((all_ws_d5 * 512)/1024)/1024)/1024, ' GiB')
    print("WSM count : ", len(fio_ws_d5))
    #############################################

    fio_access_len5 = fio_ws_d5['Offset'].dropna() + fio_ws_d5['Length'].dropna()
    
    fio_off5 = fio_ws_d5['Offset'].values
    fio_ln5 = fio_access_len5.values
    fio_time5 = fio_ws_d5['Time'].values

    
    #fio_graph(fio_off,fio_ln,fio_time,fio_off2,fio_ln2,fio_time2,fio_off3,fio_ln3,fio_time3,fio_off4,fio_ln4,fio_time4,fs)
    


trace(fs='f2fs', proc='0', event='D', rwbs='RA', rwbs2='WS', rwbs3='R', rwbs4='W', rwbs5='WSM')





