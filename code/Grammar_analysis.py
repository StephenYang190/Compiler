from grammer import Grammer
from Lexical_analysis import LexicalAnalysis
from Error_process import ErrorPro
from Semantics_analysis import Semantics_analysis


class Analysis:
    def __init__(self, FilePath, FirstPath, FollowPath=''):
        self.alpha = None
        self.lines = open(FilePath, 'r').readlines()
        self.row = 0
        self.column = 0
        self.anaf = False
        self.error = False
        self.semantics = Semantics_analysis()

        self.gram = Grammer(FirstPath)
        self.errp = ErrorPro()
        self.keyWord = ['program', 'const', 'var', 'procedure', 'begin', 'end',
                        'if', 'then', 'else', 'call', 'while', 'do', 'read', 'write']
        self.lopList = ['=', '<>', '<', '<=', '>', '>=']
        self.aopList = ['+', '-']
        self.mopList = ['*', '/']
        self.next_alpha()

    def next_alpha(self):
        if self.anaf is True:
            self.alpha = None
            return False
        line = self.lines[self.row]
        self.alpha, self.column = LexicalAnalysis(line, self.row, self.column)
        while True:
            if self.column == len(line):
                self.column = 0
                self.row = self.row + 1
                break
            char = line[self.column]
            if char == ' ' or char == '\n' or char == '\t':
                self.column += 1
            else:
                break
        if self.row == len(self.lines):
            print('Compilter all words.')
            self.anaf = True
        return True

    def in_first(self, nonter):
        if nonter == 'id':
            if self.alpha in self.keyWord:
                return False

        return self.gram.in_first(self.alpha, nonter)

    # prog
    def prog(self):
        self.semantics.offset.push(0)
        if self.alpha == 'program':
            self.next_alpha()
        else:
            if self.alpha in 'program':
                self.errorStop(21)
                self.next_alpha()
            elif not self.in_first('id'):
                self.errorStop(1)
                self.next_alpha()
            else:
                self.errorStop(1)
        idname = self.id()
        if self.alpha == ';':
            self.next_alpha()
        else:
            self.errorStop(0)
            if not self.in_first('block'):
                self.next_alpha()
        self.semantics.M(idname)
        self.block(idname)
        self.semantics.prog(idname)

        arg = {
            'mcode': self.semantics.mcode,
            'tbmng': self.semantics.tbmng,
            'stop': self.error
        }
        return arg

    # block
    def block(self, idname):
        if self.in_first('condecl'):
            self.condecl()

        if self.in_first('vardecl'):
            self.vardecl()

        if self.in_first('proc'):
            self.proc()
        hquad = self.semantics.H()
        self.semantics.tbmng.setquad(hquad)
        self.semantics.emit("%s" % idname)
        self.body()
        self.semantics.emit("end")

    # condecl
    def condecl(self):
        if self.alpha == 'const':
            self.next_alpha()
        else:
            self.errorStop(2)
            if not self.in_first('const'):
                self.next_alpha()

        self.const()

        while True:
            if self.alpha != ',':
                if self.in_first('const'):
                    self.errorStop(22)
                else:
                    break
            else:
                self.next_alpha()

            self.const()

        if self.alpha == ';':
            self.next_alpha()
        else:
            self.errorStop(0)

    # const
    def const(self):
        idname = self.id()
        if self.alpha == ':=':
            self.next_alpha()
        else:
            self.errorStop(3)

        intc = self.integer()
        self.semantics.const(idname, intc)

    # vardecl
    def vardecl(self):
        if self.alpha == 'var':
            self.next_alpha()
        else:
            self.errorStop(4)
            if not self.in_first('id'):
                self.next_alpha()

        idlist = [self.id()]

        while True:
            if self.alpha == ',':
                self.next_alpha()
            else:
                if self.in_first('id'):
                    self.errorStop(22)
                else:
                    break

            idlist.append(self.id())

        if self.alpha == ';':
            self.next_alpha()
        else:
            self.errorStop(0)

        self.semantics.vardecl(idlist)

    # proc
    def proc(self):
        self.semantics.layer += 1
        if self.alpha == 'procedure':
            self.next_alpha()
        else:
            self.errorStop(5)
            if not self.in_first('id'):
                self.next_alpha()

        idname = self.id()
        self.semantics.N(idname)

        if self.alpha == '(':
            self.next_alpha()
        else:
            self.errorStop(6)
            if not self.in_first('id') or self.alpha != ')':
                self.next_alpha()

        idlist = []
        if self.in_first('id'):
            idlist.append(self.id())
            while True:
                if self.alpha == ',':
                    self.next_alpha()
                else:
                    if self.in_first('id'):
                        self.errorStop(22)
                    else:
                        break

                idlist.append(self.id())

        if self.alpha == ')':
            self.next_alpha()
        else:
            self.errorStop(7)
            if self.alpha != ';':
                self.next_alpha()
        self.semantics.vardecl(idlist)

        if self.alpha == ';':
            self.next_alpha()
        else:
            self.errorStop(0)
            if not self.in_first('block'):
                self.next_alpha()

        self.block(idname)
        while True:
            if self.alpha == ';':
                self.next_alpha()
            else:
                if self.in_first('proc'):
                    self.errorStop(22)
                else:
                    break

            self.proc()

        self.semantics.proc(idname)
        self.semantics.layer -= 1

    # body
    def body(self):
        if self.alpha == 'begin':
            self.next_alpha()
        else:
            self.errorStop(8)
            if not self.in_first('statement'):
                self.next_alpha()

        stnextlist = self.statement()
        hquad = self.semantics.H()
        self.semantics.backpatch(stnextlist, hquad)

        while self.alpha == ';':
            if self.alpha == ';':
                self.next_alpha()
            else:
                if self.in_first('statement'):
                    self.errorStop(22)
                else:
                    break

            stnextlist = self.statement()
            hquad = self.semantics.H()
            self.semantics.backpatch(stnextlist, hquad)

        if self.alpha == 'end':
            self.next_alpha()
        else:
            self.errorStop(9)

    # lexp
    def lexp(self):
        if self.in_first('exp'):
            expplace = self.exp()
            lopc = self.lop()
            exp1place = self.exp()
            arg = {
                'expplace': expplace,
                'lopc': lopc,
                'exp1place': exp1place
            }
            truelist, falselist = self.semantics.lexp(0, arg)

        elif self.alpha == 'odd':
            self.next_alpha()

            expplace = self.exp()
            arg = {
                'expplace': expplace,
            }
            truelist, falselist = self.semantics.lexp(1, arg)

        else:
            self.errorStop(10)

        return [truelist, falselist]

    # exp
    def exp(self):
        ch = 0
        if self.alpha == '+' or self.alpha == '-':
            if self.alpha == '-':
                ch = 1
            self.next_alpha()

        termplace = self.term()
        if ch == 1:
            termplace = '-' + termplace

        while self.in_first('aop'):
            aopc = self.aop()
            term1place = self.term()
            expplace = self.semantics.newtemp()
            self.semantics.emit('%s = %s %s %s' % (expplace, termplace, aopc, term1place))
            termplace = expplace

        return termplace

    # statement
    def statement(self):
        if self.alpha == 'if':
            self.next_alpha()

            truelist, falselist = self.lexp()

            if self.alpha == 'then':
                self.next_alpha()

            else:
                self.errorStop(11)
                if not self.in_first('statement'):
                    self.next_alpha()

            hquad = self.semantics.H()
            st1nextlist = self.statement()
            self.semantics.backpatch(truelist, hquad)

            if self.alpha == 'else':
                self.next_alpha()
                inextlist, h1quad = self.semantics.I()
                st2nextlist = self.statement()
                self.semantics.backpatch(falselist, h1quad)
                stnextlist = self.semantics.merge([st1nextlist, st2nextlist, inextlist])
            else:
                stnextlist = self.semantics.merge([st1nextlist, falselist])

        elif self.in_first('id'):
            idname = self.id()

            if self.alpha == ':=':
                self.next_alpha()
            else:
                self.errorStop(3)
                if not self.in_first('exp'):
                    self.next_alpha()

            explist = self.exp()
            p = self.semantics.lookup(idname)
            if p is None:
                self.errorStop(23)
            else:
                self.semantics.emit(p + ' = ' + explist)
            stnextlist = None

        elif self.alpha == 'while':
            self.next_alpha()
            hquad = self.semantics.H()
            truelist, falselist = self.lexp()
            if self.alpha == 'do':
                self.next_alpha()
            else:
                self.errorStop(12)
                if not self.in_first('statement'):
                    self.next_alpha()
            h1quad = self.semantics.H()
            st1nextlist = self.statement()
            self.semantics.backpatch(st1nextlist, hquad)
            self.semantics.backpatch(truelist, h1quad)
            stnextlist = falselist
            self.semantics.emit('j  -  -  %d' % hquad)

        elif self.alpha == 'call':
            self.next_alpha()
            idname = self.id()
            if self.alpha == '(':
                self.next_alpha()
            else:
                self.errorStop(6)
                if not self.in_first('exp') or self.alpha != ')':
                    self.next_alpha()
            explist = []
            if self.in_first('exp'):
                explist.append(self.exp())
                while True:
                    if self.alpha == ',':
                        self.next_alpha()
                    else:
                        if self.in_first('exp'):
                            self.errorStop(22)
                        else:
                            break
                    explist.append(self.exp())

            if self.alpha == ')':
                self.next_alpha()
            else:
                self.errorStop(7)
            i = 0
            for exp in explist:
                self.semantics.emit('param ' + exp)
                i += 1
            l = self.semantics.tbmng.level(idname)
            self.semantics.emit('call %s %d %d' % (idname, i, l))
            stnextlist = None

        elif self.alpha == 'read':
            self.next_alpha()

            if self.alpha == '(':
                self.next_alpha()
            else:
                self.errorStop(6)
                if not self.in_first('id'):
                    self.next_alpha()

            readid = self.id()
            while True:
                if self.alpha == ',':
                    self.next_alpha()
                else:
                    if self.in_first('id'):
                        self.errorStop(22)
                    else:
                        break
                readid += ' ' + self.id()

            if self.alpha == ')':
                self.next_alpha()
            else:
                self.errorStop(7)

            readid = "".join(self.semantics.lookup(id) for id in readid)
            self.semantics.emit('read ' + readid)
            stnextlist = None

        elif self.alpha == 'write':
            self.next_alpha()
            if self.alpha == '(':
                self.next_alpha()
            else:
                self.errorStop(6)
                if not self.in_first('exp'):
                    self.next_alpha()

            writeexp = self.exp()

            while self.alpha == ',':
                if self.alpha == ',':
                    self.next_alpha()
                else:
                    if self.in_first('exp'):
                        self.errorStop(22)
                    else:
                        break
                writeexp += ' ' + self.exp()

            if self.alpha == ')':
                self.next_alpha()
            else:
                self.errorStop(7)
            self.semantics.emit('write ' + writeexp)
            stnextlist = None

        elif self.in_first('body'):
            self.body()
            stnextlist = None
        else:
            self.errorStop(13)
            stnextlist = None

        return stnextlist

    # term
    def term(self):
        lastplace = self.factor()
        if lastplace is None:
            return None
        while self.in_first('mop'):
            mopc = self.mop()
            fac1place = self.factor()
            if fac1place is None:
                break
            termplace = self.newtemp()
            self.semantics.emit('%s = %s %s %s' % (termplace, lastplace, mopc, fac1place))
            lastplace = termplace

        return lastplace

    # factor
    def factor(self):
        if self.in_first('id'):
            idname = self.id()
            p = self.semantics.lookup(idname)
            if p is None:
                return None
            else:
                return p

        elif self.in_first('integer'):
            intc = self.integer()
            return str(intc)

        elif self.alpha == '(':
            self.next_alpha()
            expplace = self.exp()
            if self.alpha == ')':
                self.next_alpha()
            else:
                self.errorStop(7)
            return expplace

        else:
            self.errorStop(14)
            return None

    # lop
    def lop(self):
        if self.alpha in self.lopList:
            lopc = self.alpha
            self.next_alpha()
        else:
            self.errorStop(15)

        return lopc

    # aop
    def aop(self):
        if self.alpha in self.aopList:
            aopc = self.alpha
            self.next_alpha()
        else:
            self.errorStop(16)
        return aopc

    # mop
    def mop(self):
        if self.alpha in self.mopList:
            mopc = self.alpha
            self.next_alpha()
        else:
            self.errorStop(17)

        return mopc

    # id
    def id(self):
        for index, char in enumerate(self.alpha):
            if index == 0:
                if (char <= 'Z' and char >= 'A') or (char <= 'z' and char >= 'a'):
                    pass
                else:
                    self.errorStop(18)
            else:
                if (char <= 'Z' and char >= 'A') or (char <= 'z' and char >= 'a'):
                    pass
                elif (char <= '9' and char >= '0'):
                    pass
                else:
                    self.errorStop(19)
                    return None
        idname = self.alpha
        self.next_alpha()
        return idname

    # integer
    def integer(self):
        for char in self.alpha:
            if (char <= '9' and char >= '0'):
                pass
            else:
                self.errorStop(20)
                return None

        intc = self.alpha
        self.next_alpha()
        return intc

    def errorStop(self, ch):
        self.errp.error_print(ch, self.row, self.column)
        self.error = True