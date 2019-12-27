from scapy.all import *
import os
import numpy as np
import csv
import threading
from multiprocessing import cpu_count
import time

threadNums = cpu_count() - 1
# threadNums = 6

inputDir = 'E:\\流量数据stream1000'

nonVideo = ['jingdong', 'pinduoduo', 'taobao', 'QQ', 'weibo', '百度贴吧', '豆瓣', '今日头条']

headers = ['maxInterval', 'minInterval', 'avgInterval', 'stdInterval', 'maxSize', 'minSize', 'avgSize', 'stdSize',
           'maxupInterval', 'minupInterval', 'avgupInterval', 'stdupInterval',
           'maxdownInterval', 'mindownInterval', 'avgdownInterval', 'stddownInterval', 'maxupSize', 'minupSize',
           'avgupSize', 'stdupSize', 'maxdownSize', 'mindownSize', 'avgdownSize',
           'stddownSize', 'allRate', 'upRate', 'downRate', '字节总数', '包的数量', '应用名称', '是否为视频']

lock = threading.Lock()



def feature(pcapPath, appDir):
    pcaps = rdpcap(pcapPath)

    allTime = []
    upTime = []
    downTime = []
    allByte = []
    upByte = []
    downByte = []
    for i in range(len(pcaps)):
        if (i == 0):
            allTime.append(pcaps[i].time)
        else:
            allTime.append(pcaps[i].time - pcaps[i - 1].time)
        allByte.append(pcaps[i].len)

        if pcaps[i].payload.sport > 10000:
            upByte.append(pcaps[i].len)
            upTime.append(pcaps[i].time)
        else:
            downByte.append(pcaps[i].len)
            downTime.append(pcaps[i].time)

    if len(allTime) == 0:
        maxInterval = 0
        minInterval = 0
        avgInterval = 0
        stdInterval = 0
    else:
        maxInterval = max(allTime)
        minInterval = min(allTime)
        avgInterval = sum(allTime) / len(allTime)
        stdInterval = np.std(allTime)

    if len(allByte) == 0:
        maxSize = 0
        minSize = 0
        avgSize = 0
        stdSize = 0
    else:
        maxSize = max(allByte)
        minSize = min(allByte)
        avgSize = sum(allByte) / len(allByte)
        stdSize = np.std(allByte)

    if len(upTime) == 0:
        maxupInterval = 0
        minupInterval = 0
        avgupInterval = 0
        stdupInterval = 0
    else:
        maxupInterval = max(upTime)
        minupInterval = min(upTime)
        avgupInterval = sum(upTime) / len(upTime)
        stdupInterval = np.std(upTime)

    if len(downTime) == 0:
        maxdownInterval = 0
        mindownInterval = 0
        avgdownInterval = 0
        stddownInterval = 0
    else:
        maxdownInterval = max(downTime)
        mindownInterval = min(downTime)
        avgdownInterval = sum(downTime) / len(downTime)
        stddownInterval = np.std(downTime)

    if len(upByte) == 0:
        maxupSize = 0
        minupSize = 0
        avgupSize = 0
        stdupSize = 0
    else:
        maxupSize = max(upByte)
        minupSize = min(upByte)
        avgupSize = sum(upByte) / len(upByte)
        stdupSize = np.std(upByte)

    if len(downByte) == 0:
        maxdownSize = 0
        mindownSize = 0
        avgdownSize = 0
        stddownSize = 0
    else:
        maxdownSize = max(downByte)
        mindownSize = min(downByte)
        avgdownSize = sum(downByte) / len(downByte)
        stddownSize = np.std(downByte)

    if sum(allTime):
        allRate = sum(allByte) / sum(allTime)
    else:
        allRate = 0
    if sum(upTime):
        upRate = sum(upByte) / sum(upTime)
    else:
        upRate = 0
    if sum(downTime):
        downRate = sum(downByte) / sum(downTime)
    else:
        downRate = 0

    singleFeature = (
        maxInterval, minInterval, avgInterval, stdInterval, maxSize, minSize, avgSize, stdSize, maxupInterval,
        minupInterval, avgupInterval, stdupInterval,
        maxdownInterval, mindownInterval, avgdownInterval, stddownInterval, maxupSize, minupSize, avgupSize, stdupSize,
        maxdownSize, mindownSize, avgdownSize,
        stddownSize, allRate, upRate, downRate, sum(allByte), len(allByte), appDir, 0 if appDir in nonVideo else 1)

    print(singleFeature)
    return singleFeature



def action(appList, writer1, writer2):

    for appDir in appList:
        appPath = os.path.join(inputDir, appDir)

        trainFeatures = []
        testFeatures = []
        i = 0
        for pcapFile in os.listdir(appPath):
            pcapcount = len(os.listdir(appPath))
            nonVideopcapcount = pcapcount / 3
            if appDir in nonVideo:
                if i >= nonVideopcapcount / 3:
                    break
            i += 1
            print(threading.current_thread().getName(), appDir, i, end=', ')
            pcapPath = os.path.join(appPath, pcapFile)
            if (appDir not in nonVideo and i <= pcapcount * 0.7) or (
                    appDir in nonVideo and i <= nonVideopcapcount * 0.7):
                trainFeatures.append(feature(pcapPath, appDir))
            else:
                testFeatures.append(feature(pcapPath, appDir))
        lock.acquire()
        writer1.writerows(trainFeatures)
        writer2.writerows(testFeatures)
        lock.release()



if __name__ == "__main__":

    start = time.clock()

    trainfile = open('E:\\流量特征csv\\train2.csv', 'w', newline='')
    writer1 = csv.writer(trainfile)
    writer1.writerow(headers)

    testfile = open('E:\\流量特征csv\\test2.csv', 'w', newline='')
    writer2 = csv.writer(testfile)
    writer2.writerow(headers)

    t = []
    dirList = os.listdir(inputDir)
    num = len(dirList) // threadNums
    r = len(dirList) % threadNums
    for _i in range(threadNums):
        appList = []
        for _j in range(num):
            appList.append(dirList[_i*num+_j])
        if r:
            appList.append(dirList[num*threadNums+r-1])
            r -= 1
        t.append(threading.Thread(target=action, args=(appList, writer1, writer2)))

    for _t in t:
        _t.start()
    for _t in t:
        _t.join()


    trainfile.close()
    testfile.close()

    end = time.clock()

    print("使用时间：", end - start)

