import os
from scapy.all import *

work_dir = 'D:\\Wireshark'
os.chdir(work_dir)

pcap_dir = 'E:\\流量数据stream'
output_dir = 'E:\\流量数据stream1000'
edit = 'editcap -c 1000 '

for app_dir in os.listdir(pcap_dir):
    app_creatdir = os.path.join(output_dir, app_dir)
    if not os.path.exists(app_creatdir):
        os.mkdir(app_creatdir)
    app_path = os.path.join(pcap_dir, app_dir)
    i = 0
    for pcap_file in os.listdir(app_path):
        pcap_path = os.path.join(app_path, pcap_file)
        # print(pcap_path)
        editcommod = edit + pcap_path + ' ' +  app_creatdir + '\\' + app_dir + str(i) +'.pcap'
        print(editcommod)
        os.system(editcommod)
        i += 1



