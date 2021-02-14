import json
import argparse

## 読み込んだIRを2進数・16進数に変換
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
      if t * 7.0 < code[i]:  # 開始コード. なぜ7？
        t = (code[i] + code[i + 1]) / 16.0  # 1Tを求める 16Tへ
        data.append("")
      elif code[i + 1] < t * 2.0:  # 奇数バイトが 1Tの場合は0
        data[-1] += "0"
      elif code[i + 1] < t * 6.0:  # 奇数バイトが 3Tの場合は1
        data[-1] += "1"

    
    print(data)
    for d in data:
      print(format(int(d, 2), "x"))