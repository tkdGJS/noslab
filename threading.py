import threading
import time

shared_mem = []

def threadA():
    time.sleep(1)

    a=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    
    for i in a:
        shared_mem.append(i)

    while True:
        shared_mem.append('A')

    return 0

def threadB():
    
    time.sleep(1)

    a=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    
    for i in a:
        shared_mem.append(i)
    
    while True:
        shared_mem.append('a')
    
    return 0

def threadC():
    
    time.sleep(1)

    a = list(range(50))
    
    for i in a:
        shared_mem.append(i)
    
    while True:
        shared_mem.append(int(1))

    return 0

def threadD():
    
    if len(shared_mem) == int(14):
        print(shared_mem,"\t")
    else:
        print("not 14\t")

th=[]

thread_1 = threading.Thread(target=(threadA))
thread_2 = threading.Thread(target=(threadB))
thread_3 = threading.Thread(target=(threadC))
thread_4 = threading.Thread(target=(threadD))



th.append(thread_1)
th.append(thread_2)
th.append(thread_3)
th.append(thread_4)

for thread in th:
    thread.start()

time.sleep(10)

for thread in th:
    thread.join()
