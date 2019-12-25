# import os
#
# inputDir = 'E:\流量数据stream1000'
#
# nonVideo = ['jingdong', 'pinduoduo', 'taobao', 'QQ', 'weibo', '百度贴吧', '豆瓣', '今日头条']
#
# videonum = 0
# nonvideonum = 0
#
# for appDir in os.listdir(inputDir):
#     appPath = os.path.join(inputDir, appDir)
#     count = len(os.listdir((appPath)))
#     print(appDir, count)
#     if appDir in nonVideo:
#         nonvideonum += count
#     else:
#         videonum += count
#
# print('video', videonum)
# print('nonvideo', nonvideonum)



import csv

headers = ['maxInterval', 'minInterval', 'avgInterval', 'stdInterval', 'maxSize', 'minSize', 'avgSize', 'stdSize', 'maxupInterval', 'minupInterval', 'avgupInterval', 'stdupInterval',
                     'maxdownInterval', 'mindownInterval', 'avgdownInterval', 'stddownInterval', 'maxupSize', 'minupSize', 'avgupSize', 'stdupSize', 'maxdownSize', 'mindownSize', 'avgdownSize',
                     'stddownSize', 'allRate', 'upRate', 'downRate', '字节总数', '包的数量', '应用名称', '是否为视频']

rows = [
        [1,'xiaoming','male',168,23],
        [1,'xiaohong','female',162,22],
        [2,'xiaozhang','female',163,21],
        [2,'xiaoli','male',158,21]
    ]

with open('test1.csv','w')as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)