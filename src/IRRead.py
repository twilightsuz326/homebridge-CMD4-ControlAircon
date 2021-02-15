import json
import argparse

# IRRead.py 
# https://qiita.com/gorohash/items/598d69a63bd6b4308291
# 赤外線の信号をデコード。 IRを2進数出力するコードを追加しただけ。

# 実行:
# python -f ir.json ac:cool27

p = argparse.ArgumentParser()
p.add_argument("-f", "--file", help="Filename", required=True)
p.add_argument("id", nargs="+", type=str, help="IR codes")

args = p.parse_args()

with open(args.file, "r") as f:
  records = json.load(f)

for arg in args.id:
  if arg in records:
    code = records[arg]

    t = 0.0
    data = []
    for i in range(0, len(code) - 1, 2):
      if t * 7.0 < code[i]:  # 開始コード. 8T以上の時に新枠
        t = (code[i] + code[i + 1]) / 16.0  # 1Tを求める 16Tへ
        data.append("")
      elif code[i + 1] < t * 2.0:  # 奇数バイトが 1Tの場合は0
        data[-1] += "0"
      elif code[i + 1] < t * 6.0:  # 奇数バイトが 3Tの場合は1
        data[-1] += "1"

    
    print(data)
    for d in data:
      print(format(int(d, 2), "x"))