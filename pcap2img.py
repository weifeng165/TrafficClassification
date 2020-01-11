import struct
from scapy.all import *
import numpy
from PIL import Image
import binascii
import os

STREAMLEN = 1000
PIN_SIZE = 40
PADDING = b'\x00'
STREAMDIR = 'D:\\流量数据stream'
OUTDIR = 'D:\\流量数据img'


def getMatrix(bpcap,width):
    while len(bpcap) < PIN_SIZE**2:
        bpcap += PADDING
    if len(bpcap) > PIN_SIZE**2:
        bpcap = bpcap[:PIN_SIZE**2]

    hexst = binascii.hexlify(bpcap)
    print(hexst)
    fh = numpy.array([int(hexst[i:i+2],16) for i in range(0, len(hexst), 2)])
    rn = len(fh)/width
    fh = numpy.reshape(fh[:int(rn*width)],(-1,width))
    fh = numpy.uint8(fh)
    return fh

def getLenAndTime(filename):
    pcaps = rdpcap(filename)

    len_array = []
    time_array = []
    for pcap in pcaps:
        len_array.append(len(pcap))
        time_array.append(pcap.time)
    return len_array, time_array


def getBinary(filename):

    len_array, time_array = getLenAndTime(filename)
    print(len_array)
    with open(filename, 'rb') as f:
        string_data = f.read()

    i = 24
    j = 0
    streamSet = []
    pcapSet = []
    while(i<len(string_data)):
        if j % STREAMLEN == 0:
            if j != 0:
                streamSet.append(pcapSet[:])
                pcapSet = []
        i += 16
        pcapSet.append(string_data[i: i+len_array[j]])
        i += len_array[j]
        j += 1
    streamSet.append(pcapSet)
    return streamSet

def matrix2Img(pmatrix, outappdir, i, appname):
    im = Image.fromarray(pmatrix)
    png_full = os.path.join(outappdir, appname + '_' + str(i) + '.png')
    im.save(png_full)

# u = b'\x08\x00\'\xc6\x00\xcdRT\x00\x125\x02\x08\x00E\x00\x00(\xc8E\x00\x00@\x06\x9a\x9dnL\x9c\x92\n\x00\x03\x0f\x00P\x84\xc1\x08"E\xb2\xaeK\x84OP\x10\xff\xff\x92f\x00\x00'
# v = b'RT\x00\x125\x02\x08\x00\'\xc6\x00\xcd\x08\x00E\x00\x02i\xc0\x02@\x00@\x06`\x9f\n\x00\x03\x0fnL\x9c\x92\x84\xc1\x00P\xaeK\x82\r\x08"E\xb2P\x18\xff(\x1aI\x00\x00GET /befe9a0cb8494baac5d7346b0ee067e7/5c47040d/video/m/22009850b92caf84d538d237c4b86b966fb11613f23700009736258d560f/?rc=anY6c21ka3RlajMzOmkzM0ApQHRAbzM1ODk1OjgzNDU1OzU0PDNAKXUpQGczdylAZmh1eXExZnNoaGRmOzRAM29oYWVtYDJwXy0tNS0wc3MtbyNvI0EyLy80LS4tLTAyLi8tLi9pOmItbyM6YC1vI3BiZnJoXitqdDojLy5e HTTP/1.1\r\nRange: bytes=0-10485760\r\nVpwp-Type: preloader\r\nVpwp-Key: 3F115596A283611845A3DE17E56C72E7\r\nVpwp-Raw-Key: v0300f870000bgsb5qchpahjdpk7rs6g_h264_540p_898130\r\nVpwp-Flag: 0\r\nAccept-Encoding: identity\r\nHost: v9-dy-y.ixigua.com\r\nConnection: Keep-Alive\r\nUser-Agent: okhttp/3.10.0.1\r\n\r\n'


if __name__ == "__main__":
    # testDir = 'D:\流量数据stream\抖音\\douyin1.pcap.TCP_10-0-3-15_33985_110-76-156-146_80.pcap'
    # # streamSet = getBinary(testDir)
    # arr = getMatrix(v, PIN_SIZE)
    #
    # print(arr.shape)

    for app_dir in os.listdir(STREAMDIR):
        app_path = os.path.join(STREAMDIR, app_dir)
        i = 0
        outappdir = os.path.join(OUTDIR, app_dir)
        os.makedirs(outappdir)
        for pcap in os.listdir(app_path):
            pcap_path = os.path.join(app_path, pcap)
            streamSet = getBinary(pcap_path)
            for pcapSet in streamSet:
                streampath = os.path.join(outappdir, str(i))
                os.makedirs(streampath)
                j = 0
                for bpcap in pcapSet:
                    pmatrix = getMatrix(bpcap, PIN_SIZE)
                    matrix2Img(pmatrix, streampath, j, app_dir)
                    j += 1
                i += 1


