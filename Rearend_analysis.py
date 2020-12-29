class rear_analysis:
    def __init__(self, arg):
        self.mcodes = arg['mcode']
        self.tbmng = arg['tbmng']
        self.nextline = 0
        self.ori2now = {}
        self.backlist = []
        self.codes = []
        self.op = {
            '+': 2,
            '-': 3,
            '*': 4,
            '/': 5,
            'odd': 6,
            '=': 8,
            '<>': 9,
            '<': 10,
            '>=': 11,
            '>': 12,
            '<=': 13,
        }
        self.backlist.append(self.nextline)
        target = self.tbmng.probegin(self.tbmng.first())
        self.gencode('JMP 0 %d' % target)

    def analysis(self):
        paramlist = []
        for lnindex, mcode in enumerate(self.mcodes):
            self.ori2now[str(lnindex)] = str(self.nextline)
            mcodes = mcode.split()
            if mcodes[0] == 'write':
                for num in mcodes:
                    if num == 'write':
                        continue
                    else:
                        self.genNum(num)
                    self.gencode('WRT 0 0')

            elif mcodes[0] == 'read':
                for num in mcodes:
                    if num == 'read':
                        continue
                    else:
                        _, _, a, l = num.split('|')
                        self.gencode('RED %s %s' % (l, a))

            elif mcodes[0] == 'param':
                paramlist.append(mcodes)

            elif mcodes[0] == 'call':
                tarpro = self.tbmng.probegin(mcodes[1])
                for param in paramlist:
                    self.genNum(param[1])
                paramlist = []
                self.backlist.append(self.nextline)
                self.gencode('CAL %s %s' % (mcodes[3], tarpro))
                self.genNum(mcodes[2])
                self.backlist.append(self.nextline)
                self.gencode('JMP 0 %s' % (tarpro))

            elif mcodes[0] == 'j':
                tarpro = mcodes[3]
                self.backlist.append(self.nextline)
                self.gencode('JMP 0 %s' % (tarpro))

            elif 'j' in mcodes[0] and '|' not in mcodes[0]:
                tarpro = mcodes[3]
                num1 = mcodes[1]
                self.genNum(num1)
                num2 = mcodes[2]
                self.genNum(num2)
                op = mcodes[0][1:]
                self.gencode('OPR 0 %s' % self.op[op])
                self.backlist.append(self.nextline)
                self.gencode('JPC %d %s' % (0, tarpro))

            elif len(mcodes) == 1:
                if mcodes[0] == 'end':
                    self.gencode('OPR 0 0')
                else:
                    n = self.tbmng.tbval(mcodes[0])
                    self.gencode('INT 0 %s' % str(4 + n))
            else:
                if len(mcodes) == 3:
                    self.genNum(mcodes[2])
                    self.genSTO(mcodes[0])
                else:
                    num1 = mcodes[2]
                    self.genNum(num1)
                    num2 = mcodes[4]
                    self.genNum(num2)
                    self.gencode('OPR 0 %s' % self.op[mcodes[3]])
                    self.genSTO(mcodes[0])
        self.backpatch()
        return self.codes

    def genNum(self, num):
        if '|' in num:
            nums = num.split('|')
            if nums[1] == 'c':
                self.gencode('LIT 0 %s' % nums[2])
            else:
                self.gencode('LOD %s %s' % (nums[3], nums[2]))
        else:
            if 't' in num:
                pass
            else:
                self.gencode('LIT 0 %s' % num)

    def genSTO(self, tar):
        if '|' in tar:
            self.gencode('STO %s %s' % (tar.split('|')[3], tar.split('|')[2]))
        else:
            pass

    def print(self):
        for index, code in enumerate(self.codes):
            print("%d : %s" % (index, code))
        for ori, tar in self.ori2now.items():
            print("%s-->%s" % (ori, tar))

    def gencode(self, code):
        self.codes.append(code)
        self.nextline += 1

    def backpatch(self):
        for l in self.backlist:
            codes = self.codes[l].split()
            codes[2] = self.ori2now[codes[2]]
            self.codes[l] = "%s %s %s" % (codes[0], codes[1], codes[2])