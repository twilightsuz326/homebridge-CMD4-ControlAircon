# coding: utf-8

#
# homebridge-CMD4-ControlAirCon
# Author: TwilightSuz326
#
# IRMake.py
#  -> 赤外線データ作成クラス
#
#  IRの間隔は下記で統一
#  Start: 8500
#  0: 1000 1000  1: 1000 3200
#  End: 10400
#

import makeBinIR

class makeIR:
    def __init__(self, postdic, posthex=""):
        self.posthex = posthex  # "f20d03fc0100c78046"
        self.bindata = []  # ["1111", "0010", "0000", "1101"…]
        self.binir = []  # [8500,8500,1000…]
        self.postdic = postdic

    def startmake(self):
        if (self.posthex == ""):
            self.makehex()
        
        self.bindata = makeBinIR.convHextoBin(self.posthex)
        # bintoIR(repeat, bincode, startcode, ontime, offtime, fincode):
        self.binir = makeBinIR.convBintoIR(2, self.bindata, [8500, 8500], 1000, 3200, [1000,10400])
        return self.binir

    def makehex(self):
        #self.posthex = "f20d03fc01d0c18090"
        self.posthex = "f20d03fc01"
        
        # 設定温度 (0~f) 自動運転は 中間値を採用
        if (self.postdic.TargetHeaterCoolerState == 0):
            settemp = (self.postdic.CoolingThresholdTemperature + self.postdic.HeatingThresholdTemperature) / 2
        if (self.postdic.TargetHeaterCoolerState == 1):
            settemp = self.postdic.HeatingThresholdTemperature
        if (self.postdic.TargetHeaterCoolerState == 2):
            settemp = self.postdic.CoolingThresholdTemperature
        
        settemp -= 17 # 17℃(0000)スタート
        self.posthex += self.transhex(settemp) + "0"

        # 風量 (オフ(選択されない), しずか(2), 1(4), 2(8), 3(c), 自動(0))
        speedlist = [0,2,4,8,12,0]
        setspeedval = self.postdic.RotationSpeed / 20
        setspeed = speedlist[int(setspeedval)]

        self.posthex += self.transhex(setspeed)

        # 運転モード (自動(0), 暖房(3), 冷房(1)) & 電源状態(OFF:7) 
        setHCState = self.postdic.TargetHeaterCoolerState
        if self.postdic.TargetHeaterCoolerState == 1:
            setHCState = 3
        if self.postdic.TargetHeaterCoolerState == 2:
            setHCState = 1
        if self.postdic.Active == 0:
            setHCState = 7
        self.posthex += self.transhex(setHCState) + "80"

        # チェックディジット (前半: 11,13,15バイト の総和 後4ビット ※13B-11B = 0,-1,-4,-5 … の場合は 13B-11B+15B)
        # 電源OFFは※対象外
        hex12 = int(self.posthex[12], 16)
        hex10 = int(self.posthex[10], 16)
        if(self.postdic.Active == 0 or hex12 >= hex10 and (hex12 - hex10) % 4 in [1,2]):
            check1 = hex10 + hex12 + int(self.posthex[14], 16)
        else:
            check1 = hex10 - hex12 + int(self.posthex[14], 16)
        check1 = str(format(check1, "04b"))[-4:]
        self.posthex += format(int(check1, 2), "x")

        # X NG X (後半: 14バイト - 10バイト ※14B < 10Bの場合は総和) 
        # 電源OFF: 6, 冷房: 0, 自動: 1, 暖房: 2 (たぶん)
        if(self.postdic.Active == 1):
            if(self.postdic.TargetHeaterCoolerState == 0):
                check2 = 1
            elif(self.postdic.TargetHeaterCoolerState == 2):
                check2 = 0
            elif(self.postdic.TargetHeaterCoolerState == 1):
                check2 = 2
        else:
            check2 = 6
        
        self.posthex += str(check2)


    # 10進数から16進数の値へ
    def transhex(self, val):
        return str( format(int(val), "0x") )