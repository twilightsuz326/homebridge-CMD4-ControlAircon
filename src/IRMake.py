# coding: utf-8

class makeIR:
    def __init__(self, postdic):
        self.posthex = ""  # "f20d03fc0100c78046"
        self.bindate = []  # ["1111", "0010", "0000", "1101"…]
        self.binir = []  # [8500,8500,1000…]
        self.postdic = postdic

    def startmake(self):
        if (self.posthex == ""):
            self.makehex()
        
        self.makebindate()
        print(self.bindate)
        self.makeBinIR()

        
        return self.binir

    def makehex(self):
        self.posthex = "f20d03fc01d0c18090"
        print(self.posthex)

    def makebindate(self):
        hexlist = list(self.posthex)
        for val in hexlist:
            self.bindate.append(format(int(val,16), "04b"))
        return

    def makeBinIR(self):
        for k in range(2):
            for i in range(2):
                self.binir.append(8500)
            for i in self.bindate:
                for n in list(i):
                    if(n == "0"):
                        self.binir.append(1000)
                        self.binir.append(1000)
                    if(n == "1"):
                        self.binir.append(1000)
                        self.binir.append(3200)
            self.binir.append(1000)
            self.binir.append(10400)
                

