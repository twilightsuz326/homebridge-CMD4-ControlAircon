# coding: utf-8

#
# homebridge-CMD4-ControlAirCon
# Author: TwilightSuz326
#
# IRPost.py
#  -> (汎用) IRKitへのIR送信クラス(受信も書けばよかった?)
#

import IRMake
import urllib.request
import json

def setval(postdic, posthex=""):
    irmake = IRMake.makeIR(postdic)

    # スイング用hex
    irmake.posthex = posthex

    binir = irmake.startmake()  # [8500,8500,1000…]
    binir_str = ",".join(map(str, binir)) # "8500,8500,1000…"

    # DEBUG
    # print(irmake.posthex)
    print(binir_str)

    postIRKit(binir_str)

    # 送信
    return


def postIRKit(postbin):
    url = "http://192.168.3.31/messages" 
    method = "POST"
    headers = {"X-Requested-With" : "curl"}

    # PythonオブジェクトをJSONに変換する
    obj = {"format" : "raw", "freq" : 38, "data": [postbin]} 
    json_data = json.dumps(obj).encode("utf-8")

    # httpリクエストを準備してPOST
    request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        # Response
        # print(response_body)



if __name__ == "__main__" :
    postIRKit("8450,8450")
    a = [0x9,0x0,0xc,0x1,0x8,0x0] 
    b = "1010"

    c = "1000,3000,1000,1000,1000,3000,1000,1000"
    d = "8755,8755,1000,3000…"
    
    print(sum(a))
    print(bin(sum(a)))
