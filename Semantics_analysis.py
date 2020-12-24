from stack import stack
from table import table


class Semantics_analysis:
    def __init__(self):
        #table stack
        self.tblpter = stack()
        #offset stack
        self.offset = stack()
        self.first_table = None
        self.mcode = []
        self.nextquad = 0

    def mktable(self, pre):
        newt = table(pre)
        if pre is None:
            self.first_table = newt

        self.tblpter.push(newt)

    def prog(self):
        return True

    def M(self):
        t = self.mktable(None)
        self.tblpter.push(t)
        self.offset.push(0)

    def N(self):
        t = self.mktable(self.tblpter.top())
        self.tblpter.push(t)
        self.offset.push(0)

    def const(self, idname, integerc):
        t = self.tblpter.top()
        t.enter(idname, 'integer', self.offset.top(), integerc)
        self.mcode.append(idname + ' = ' + str(integerc))
        self.nextquad += 1
        self.offset.add(4)

    def vardecl(self, Aidlist):
        t = self.tblpter.top()
        for idname in Aidlist:
            t.enter(idname, 'integer', self.offset.top())
            self.offset.add(4)

    def proc(self, idname):
        t = self.tblpter.top()
        t.addwidth(self.offset.top())
        self.tblpter.pop()
        self.offset.pop()
        self.tblpter.top().enterproc(idname, t)

    def body(self, stnextlist, hquad):
        self.backpatch(stnextlist, hquad)

    def backpatch(self, nextlist, quad):
        for index in nextlist:
            code = self.mcode[index].split()
            code = code[0] + ' ' + code[1] + ' ' + code[2] + ' ' + quad
            self.mcode[index] = code

    def L(self, ch, stnextlist=None, hquad=None):
        if ch == 0:
            self.backpatch(stnextlist, hquad)
        else:
            pass

    def statement(self, ch, arg):
        if ch == 0:
            t = self.tblpter.top()
            p = t.lookup(arg.idname)
            if p is None:
                print('Error')
            else:
                self.mcode.append(arg.idname + '=' + arg.expplace)
                self.nextquad += 1
        elif ch == 1:
            self.backpatch(arg.letruelist, arg.hquad)
            nextlist = arg.lefalselist + arg.st1nextlist
            nextlist = list(set(nextlist))

            return nextlist
        elif ch == 2:
            self.backpatch(arg.letruelist, arg.hquad)
            self.backpatch(arg.lefalselist, arg.h1quad)
            nextlist = arg.inextlist + arg.st1nextlist + arg.st2nextlist
            nextlist = list(set(nextlist))

            return nextlist
        elif ch == 3:
            self.backpatch(arg.st1nextlist, arg.hquad)
            self.backpatch(arg.letruelist, arg.h1quad)
            nextlist = arg.lefalselist
            self.mcode.append('j - - ' + str(arg.hquad))
            self.nextquad += 1

            return nextlist

    def I(self):
        inextlist = [self.nextquad]
        self.mcode.append('j ' + '-' + '-' + '-')
        self.nextquad += 1
        return inextlist

    def H(self):
        hquad = self.nextquad
        return hquad

