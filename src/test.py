import makeBinIR
import IRPost
import time

# 181808 CH2 消灯
# 181848 CH2 全灯
# 18184a CH1 全灯
# 181814 CH1 消灯
a = makeBinIR.convHextoBin("a55a38c7")
b = makeBinIR.convBintoIR(3, a, [16800, 8400], 1050, 3150, [1050,54214])
print(b)
IRPost.postIRKit(b)