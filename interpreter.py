from stack import stack


class interpreter:
    def __init__(self, codes):
        self.codes = codes
        self.stack = stack()
        #present code
        self.I = None
        #top of stack
        self.T = None
        #sp
        self.B = None
        #next code
        self.P = None

    def LIT(self, l, a):
        self.stack.push(a)
        if self.T is None:
            self.T = 0
        else:
            self.T += 1

    def OPR(self, l, a):
        num1 = self.stack[self.T]
        num2 = self.stack[self.T - 1]

    def LOD(self, l, a):
        add = self.B
        while l > 0:
            add = self.stack[add]
            l -= 1
        self.stack.push(self.stack[add + a])

    def STO(self, l, a):
        add = self.B
        while l > 0:
            add = self.stack[add]
            l -= 1
        self.stack.set(add + a, self.stack.top())

    def CAL(self, l, a):
        return True

    def INT(self, l, a):
        self.B = self.T + 1
        self.T += a

    def JMP(self, l, a):
        self.P = a

    def JPC(self, l, a):
        if self.stack[self.T] == 1:
            self.P = a
        else:
            self.P = self.I + 1

    def RED(self, l, a):
        x = input()
        add = self.B
        while l > 0:
            add = self.stack[add]
            l -= 1
        self.stack.set(add + a, x)

    def WRT(self, l, a):
        print(self.stack[self.T])

    def getFun(self, f):
        fun = getattr(self, f, None)

    def forward(self):
        while True:
            F, L, A = self.codes[self.I].split()
            fun = self.getFun(F)
            fun(L, A)

