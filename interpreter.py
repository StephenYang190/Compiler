from stack import stack


class interpreter:
    def __init__(self, codes):
        self.codes = codes
        self.stack = stack()
        #present code
        self.I = 0
        #top of stack
        self.T = None
        #sp
        self.B = 0
        #next code
        self.P = None
        self.push(0)
        self.push(0)
        self.push(-1)
        self.push(0)

    def LIT(self, l, a):
        self.push(a)
        self.P = self.I + 1

    def OPR(self, l, a):
        if a == 6:
            num1 = self.pop()
            if num1 % 2:
                self.push(1)
            else:
                self.push(0)
            self.P = self.I + 1
        elif a == 0:
            k = self.stack[self.B + 3]
            orib = self.B
            self.P = self.stack[self.B + 2]
            self.I = self.stack[self.B + 2]
            self.B = self.stack[self.B + 1]
            while self.T != orib:
                self.pop()
            for i in range(k + 1):
                self.pop()
        else:
            num2 = self.pop()
            num1 = self.pop()
            if a == 2:
                self.push(num1 + num2)
            elif a == 3:
                self.push(num1 - num2)
            elif a == 4:
                self.push(num1 * num2)
            elif a == 5:
                self.push(num1 / num2)
            elif a == 8:
                if num1 == num2:
                    self.push(1)
                else:
                    self.push(0)
            elif a == 9:
                if num1 != num2:
                    self.push(1)
                else:
                    self.push(0)
            elif a == 10:
                if num1 < num2:
                    self.push(1)
                else:
                    self.push(0)
            elif a == 11:
                if num1 >= num2:
                    self.push(1)
                else:
                    self.push(0)
            elif a == 12:
                if num1 > num2:
                    self.push(1)
                else:
                    self.push(0)
            elif a == 13:
                if num1 <= num2:
                    self.push(1)
                else:
                    self.push(0)
            self.P = self.I + 1


    def LOD(self, l, a):
        add = self.B
        while l > 0:
            add = self.stack[add]
            l -= 1
        self.push(self.stack[add + a + 3 + self.stack[add + 3]])
        self.P = self.I + 1

    def STO(self, l, a):
        add = self.B
        while l > 0:
            add = self.stack[add]
            l -= 1
        value = self.pop()
        set = add + a + 3 + self.stack[add + 3]
        self.stack.set(add + a + 3 + self.stack[add + 3], value)
        self.P = self.I + 1

    def CAL(self, l, a):
        if l == '1':
            self.push(self.B)
        else:
            self.push(self.stack[self.B])
        self.push(self.B)
        self.B = self.T - 1
        self.push(self.I + 3)
        self.P = self.I + 1

    def INT(self, l, a):
        k = self.stack[self.T]
        for i in range(k):
            self.push(self.stack[self.B- k + i])
        for i in range(a - k - 4):
            self.push(0)
        self.T = self.B + a - 1
        self.P = self.I + 1

    def JMP(self, l, a):
        self.P = int(a)

    def JPC(self, l, a):
        if self.stack[self.T] == 1:
            self.P = int(a)
        else:
            self.P = self.I + 1

    def RED(self, l, a):
        x = input('enter : ')
        x = int(x)
        self.push(x)
        self.STO(l, a)
        self.P = self.I + 1

    def WRT(self, l, a):
        value = self.pop()
        print()
        print("output: %s" % value)
        print()
        self.P = self.I + 1

    def getFun(self, f):
        fun = getattr(self, f, None)
        return fun

    def forward(self):
        while True:
            F, L, A = self.codes[self.I].split()
            L = int(L)
            A = int(A)
            fun = self.getFun(F)
            fun(L, A)
            stack = self.stack.prints()
            print("%s : %s" % (self.codes[self.I], stack))
            # print("T %s : B %s" % (self.T, self.B))
            self.I = self.P
            if self.P == -1:
                break
            # input('wait')
        print('End')

    def push(self, value):
        if self.T is None:
            self.T = 0
            self.stack.push(value)
        else:
            self.T += 1
            self.stack.push(value)

    def pop(self):
        value = self.stack.pop()
        self.T -= 1
        return value
