# with open('E:\\Skype.pcap', 'rb') as f:
#     string_data = f.read()
#
# pcap_header = {}
# pcap_header['magic_number'] = string_data[0:4]
# pcap_header['version_major'] = string_data[4:6]
# pcap_header['version_minor'] = string_data[6:8]
# pcap_header['thiszone'] = string_data[8:12]
# pcap_header['sigfigs'] = string_data[12:16]
# pcap_header['snaplen'] = string_data[16:20]
# pcap_header['linktype'] = string_data[20:24]

import struct
with open('E:\\Skype.pcap', 'rb') as f:
    string_data = f.read()

i = 24

while(i < len(string_data)):
    pcap_packet_header = {}
    pcap_packet_header['GMTtime'] = string_data[i:i + 4]
    pcap_packet_header['MicroTime'] = string_data[i + 4:i + 8]
    pcap_packet_header['caplen'] = string_data[i + 8:i + 12]
    pcap_packet_header['len'] = string_data[i + 12:i + 16]
    # GMTtime = string_data[i:i + 4]
    # MicroTime = string_data[i + 4:i + 8]
    # print(struct.unpack('I', GMTtime), struct.unpack('I', MicroTime))
    i += 16
    srcdir = struct.unpack('BBBB', string_data[i + 26: i + 30])
    print(srcdir)

    packet_len = struct.unpack('I', pcap_packet_header['caplen'])[0]

    i = i + packet_len




