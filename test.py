import threading
import time
from multiprocessing import cpu_count
import os
import csv
import numpy as np


csvfile = open('E:\\test\\1.csv', 'w', newline='')
writer = csv.writer(csvfile)


lock = threading.Lock()

def fun():
    print(threading.current_thread().getName())
    global writer
    matrix = []
    header = [threading.current_thread().getName()]
    time.sleep(5)
    matrix.append(header)
    for i in range(100):
        ls = np.random.rand(10)
        matrix.append(ls)
    # lock.acquire()
    writer.writerows(matrix)
    # lock.release()

    # i = 0
    # for _i in range(10):
    #     i+=1
    #     print(threading.current_thread().getName(), i)


start = time.clock()
t = []
for i in range(cpu_count()):
    t. append(threading.Thread(target=fun))
for _t in t:
    _t.start()
for _t in t:
    _t.join()

end = time.clock()
print(start)
print(end)
print(end - start)

