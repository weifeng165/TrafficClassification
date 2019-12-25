import os

work_dir = 'E:\\流量分类\\DeepTraffic-master\\1.malware_traffic_classification\\2.PreprocessedTools(USTC-TK2016)\\0_Tool\\SplitCap_2-1'
os.chdir(work_dir)

pcap_dir = 'E:\\流量数据pcap'
output_dir = 'E:\\流量数据stream'
output = ' -o '
split = 'splitcap -r '

for app_dir in os.listdir(pcap_dir):
    app_creatdir = os.path.join(output_dir, app_dir)
    if not os.path.exists(app_creatdir):
        os.mkdir(app_creatdir)
    app_path = os.path.join(pcap_dir, app_dir)
    for pcap_file in os.listdir(app_path):
        pcap_path = os.path.join(app_path, pcap_file)
        commod_t = split + pcap_path + output + app_creatdir
        print(commod_t)
        os.system(commod_t)





