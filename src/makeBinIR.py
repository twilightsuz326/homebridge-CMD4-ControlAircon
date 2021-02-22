# coding: utf-8
#
# homebridge-CMD4-ControlAirCon
# Author: TwilightSuz326
#
# makeBinIR.py
#  -> (汎用) 16進数のデータを2進数・赤外線送信データへ変換
#
#

# 16進数テキスト -> 2進数リストへ
def convHextoBin(hexcode):
    bindata = []
    hexlist = list(hexcode)
    for val in hexlist:
        bindata.append(format(int(val,16), "04b"))
    return bindata

# 2進数リスト -> 赤外線送信データへ
def convBintoIR(repeat, bincode, startcode, ontime, offtime, fincode):
    binir = []
    for k in range(repeat):
        for i in startcode:
            binir.append(i)
        for i in bincode:
            for n in list(i):
                if(n == "0"):
                    binir.append(ontime) # 1000
                    binir.append(ontime) # 1000
                if(n == "1"):
                    binir.append(ontime) # 1000
                    binir.append(offtime) # 3200
        for i in fincode:
            binir.append(i) #1000 10400
    return binir