from stack import stack
from table import table_manager


class Semantics_analysis:
    def __init__(self):
        #table stack
        self.tbmng = table_manager()
        #offset stack
        self.offset = stack()
        self.mcode = []
        self.nextquad = 0
        self.temp = 0
        self.layer = 0

    def mktable(self, pre, idname):
        newt = self.tbmng.mktable(pre, idname, self.layer)
        return newt

    def emit(self, code):
        self.mcode.append(code)
        self.nextquad += 1

    def newtemp(self):
        temp = 't' + str(self.temp)
        self.temp += 1
        return temp

    def merge(self, lists):
        l = []
        for list in lists:
            l = l + list

        l = list(set(l))
        return l

    def prog(self, idname):
        t = self.tbmng.top()
        t.addwidth(self.offset.top())
        self.tbmng.pop()
        self.offset.pop()

        for index, code in enumerate(self.mcode):
            print('%d : %s' % (index, code))

        print()
        for t in self.tbmng.tblpter_back:
            t.printable()
            print()

    def M(self, idname):
        t = self.mktable(None, idname)
        self.offset.push(0)

    def N(self, idname):
        t = self.mktable(self.tbmng.top(), idname)
        self.offset.push(0)

    def const(self, idname, integerc):
        t = self.tbmng.top()
        t.enter(idname, 'const', self.offset.top(), integerc)
        idplace = self.lookup(idname)
        self.offset.add(4)

    def vardecl(self, Aidlist, type='var'):
        t = self.tbmng.top()
        for idname in Aidlist:
            t.enter(idname, type, self.offset.top())
            self.offset.add(4)

    def proc(self, idname):
        t = self.tbmng.top()
        t.addwidth(self.offset.top())
        self.tbmng.pop()
        self.offset.pop()
        self.tbmng.top().enterproc(idname, t)

    def body(self, stnextlist, hquad):
        self.backpatch(stnextlist, hquad)

    def backpatch(self, nextlist, quad):
        if nextlist is None:
            return False
        for index in nextlist:
            code = self.mcode[index].split()
            code = code[0] + ' ' + code[1] + ' ' + code[2] + ' ' + str(quad)
            self.mcode[index] = code
        return True

    def L(self, ch, stnextlist=None, hquad=None):
        if ch == 0:
            self.backpatch(stnextlist, hquad)
        else:
            pass

    def statement(self, ch, arg):
        if ch == 0:
            t = self.tbmng.top()
            p = t.lookup(arg['idname'])
            if p is None:
                print('Error')
            else:
                self.emit(arg['idname'] + ' = ' + arg['expplace'])
        elif ch == 1:
            self.backpatch(arg['letruelist'], arg['hquad'])
            nextlist = arg['lefalselist'] + arg['st1nextlist']
            nextlist = list(set(nextlist))

            return nextlist
        elif ch == 2:
            self.backpatch(arg['letruelist'], arg['hquad'])
            self.backpatch(arg['lefalselist'], arg['h1quad'])
            nextlist = arg['inextlist'] + arg['st1nextlist'] + arg['st2nextlist']
            nextlist = list(set(nextlist))

            return nextlist
        elif ch == 3:
            self.backpatch(arg['st1nextlist'], arg['hquad'])
            self.backpatch(arg['letruelist'], arg['h1quad'])
            nextlist = arg['lefalselist']
            self.emit('j - - ' + str(arg['hquad']))

            return nextlist
        elif ch == 4:
            for p in arg['fplacelist']:
                self.emit('param ' + p)
            self.emit('call ' + arg['idname'])

    def I(self):
        inextlist = [self.nextquad]
        self.emit('j - - -')
        hquad = self.nextquad
        return inextlist, hquad

    def H(self):
        hquad = self.nextquad
        return hquad

    def lexp(self, ch, arg):
        letruelist = [self.nextquad]
        lefalselist = [self.nextquad + 1]
        if ch == 0:
            self.emit('j' + arg['lopc'] + ' ' + arg['expplace'] + ' ' + arg['exp1place'] + ' 0')
        else:
            self.emit('jodd' + ' ' + arg['expplace'] + ' - 0')
        self.emit('j - - 0')

        return [letruelist, lefalselist]

    def factor(self, ch, arg):
        if ch == 0:
            t = self.tbmng.top()
            p = t.lookup(arg['idname'])
            facplace = p
        elif ch == 1:
            facplace = arg['intc']
        else:
            facplace = arg['expplace']

        return facplace

    def A(self, arg):
        aidlist = arg['bidlist'] + arg['idname']
        aidlist = list(set(aidlist))

        return aidlist

    def lookup(self, idname):
        t = self.tbmng.top()
        p = t.lookup(idname)
        return p





