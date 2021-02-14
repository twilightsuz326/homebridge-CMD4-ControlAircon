# homebridge-CMD4-ControlAircon

homebridge-CMD4 を使ってIRKit経由で冷暖房の操作をするプログラムです。  
  
使用プラグイン: HeaterCooler  
対象エアコン: TOSHIBA RAS-3614D  

```
        {
            "platform":                       "Cmd4",
            "name":                           "Cmd4",
            "accessories" : [
                {
                    "type":                     "HeaterCooler",
                    "displayName":              "My_HeaterCooler",
                    "active":                   "ACTIVE",
                    "currentHeaterCoolerState": "HEATING",
                    "targetHeaterCoolerState":  "AUTO",
                    "currentTemperature":        20.0,
                    "lockPhysicalControls":     "CONTROL_LOCK_DISABLED",
                    "name":                     "My_HeaterCooler",
                    "props": {
                        "HeatingThresholdTemperature": {
                            "maxValue": 30,
                            "minValue": 17,
                            "minStep": 1
                        },
                        "CoolingThresholdTemperature": {
                            "maxValue": 30,
                            "minValue": 17,
                            "minStep": 1
                        },
                        "RotationSpeed": {
                            "maxValue": 100,
                            "minValue": 0,
                            "minStep": 20
                        }
                    },
                    "state_cmd": "python3 IRHeetCool.py ",
                    "swingMode":                "SWING_ENABLED",
                    "coolingThresholdTemperature":
                                                26,
                    "heatingThresholdTemperature":
                                                28,
                    "temperatureDisplayUnits":  "CELSIUS",
                    "rotationSpeed":             100,
                    "manufacturer":             "Somebody",
                    "model":                    "Anything",
                    "serialNumber":             "12345",
                    "stateChangeResponseTime":   3
                }
            ]
        }
```
