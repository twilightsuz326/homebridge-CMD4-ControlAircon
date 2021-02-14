# coding: utf-8

import sys
import json
import IRPost
import urllib.request

#logpath = "/home/mitulu/py/logtemp.json"
logpath = "logtemp.json"

class IR:
    def __init__(self):
        self.Active = 0
        self.CurrentHeaterCoolerState = 1
        self.TargetHeaterCoolerState = 0
        self.CurrentTemperature = 20.0
        self.LockPhysicalControls = 0
        self.SwingMode = 0
        self.CoolingThresholdTemperature = 28.0
        self.HeatingThresholdTemperature = 28.0
        self.TemperatureDisplayUnits = 0
        self.RotationSpeed = 1
    
    def readjson(self):
        f = open(logpath, "r")
        tempdic = json.load(f)
        for key, val in tempdic.items():
            setattr(self, key, val)
        return self

    def writejson(self):
        f = open(logpath, "w")
        f.write(json.dumps(self.__dict__, ensure_ascii=False, indent=4))
        f.close()

    def gettemp(self):
        url = 'http://192.168.3.53:3333'
        response = urllib.request.urlopen(url)
        content = json.loads(response.read().decode('utf8'))
        self.CurrentTemperature = content["temperature"]
        return

    def getvalue(self, input):
        return self.__dict__[input]

    def setvalue(self, input, val):
        setattr(self, input, val)
        # スイングだけ別行動
        if (input == "SwingMode"):
            IRPost.setval(self, posthex="f20d01fe21042")
        else:
            IRPost.setval(self)
        self.writejson()
        return val
        

if __name__ == "__main__":
    main = IR()
    main = main.readjson()
    if sys.argv[1] == "Get":
        if sys.argv[3] == "CurrentTemperature":
            main.gettemp()
        print(main.getvalue(sys.argv[3]))
    if sys.argv[1] == "Set":
        print(main.setvalue(sys.argv[3], sys.argv[4]))
    