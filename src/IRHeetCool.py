# coding: utf-8

#
# homebridge-CMD4-ControlAirCon
# Author: TwilightSuz326
#
# IRHeetCool.py
#  -> CMD4からのパラメーターの送受信 メインクラス
#

import sys
import os
import json
import IRPost
import IRMake
import urllib.request

if os.name == "nt":
    logpath = "logtemp.json"
else:
    logpath = "/home/mitulu/py/logtemp.json"

class IR:
    def __init__(self):
        self.Name = "HeaterCooler"
        self.Active = 1
        self.CurrentHeaterCoolerState = 1
        self.TargetHeaterCoolerState = 0
        self.CurrentTemperature = 20.0
        self.LockPhysicalControls = 0
        self.SwingMode = 0
        self.CoolingThresholdTemperature = 17.0
        self.HeatingThresholdTemperature = 21.0
        self.TemperatureDisplayUnits = 0
        self.RotationSpeed = 100

    def readjson(self):
        if os.path.exists(logpath):
            f = open(logpath, "r")
            tempdic = json.load(f)
            for key, val in tempdic.items():
                setattr(self, key, val)
            f.close()
        else:
            self.writejson()
        return self

    def writejson(self):
        f = open(logpath, "w")
        f.write(json.dumps(self.__dict__, ensure_ascii=False, indent=4))
        f.close()

    # 温度取得は別で実装 & JSON取得
    def gettemp(self):
        url = 'http://192.168.3.53:3333'
        response = urllib.request.urlopen(url)
        content = json.loads(response.read().decode('utf8'))
        self.CurrentTemperature = content["temperature"]
        return

    def getvalue(self, input):
        return self.__dict__[input]

    def setvalue(self, input, val):
        if val.isdecimal():
            multival = int(val)
        else:
            multival = float(val)

        # スイングだけ別行動
        if (input == "SwingMode"):
            self.execIR(posthex="f20d01fe21042")
            return multival
        # 電源OFF時に風量リセット
        if self.Active == 0:
            self.RotationSpeed = 100
        # 自動運転の風量を固定
        if self.TargetHeaterCoolerState == 0:
            if input == "RotationSpeed":
                multival = 100
            self.RotationSpeed = 100
        
        # IRKit 帯域節約のため 既に設定済みの値はスルー
        if getattr(self, input) == multival:
            # print("SKIP")
            return multival
        
        setattr(self, input, multival)

        # Send IR
        self.execIR()

        return multival

    def execIR(self, posthex=""):
        irmake = IRMake.makeIR(self, posthex=posthex)

        binir = irmake.startmake()  # [8500,8500,1000…]
        binir_str = ",".join(map(str, binir)) # "8500,8500,1000…"
        IRPost.postIRKit(binir_str)

        self.writejson()


if __name__ == "__main__":
    main = IR()
    main = main.readjson()
    if sys.argv[1] == "Get":
        if sys.argv[3] == "CurrentTemperature":
            main.gettemp()
        print(main.getvalue(sys.argv[3]))
    if sys.argv[1] == "Set":
        print(main.setvalue(sys.argv[3], sys.argv[4]))

