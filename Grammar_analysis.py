from grammer import Grammer
from Lexical_analysis import LexicalAnalysis
from Error_process import ErrorPro


class Analysis:
    def __init__(self, FilePath, FirstPath, FollowPath=''):
        self.lines = open(FilePath, 'r').readlines()
        self.row = 0
        self.column = 0
        self.next_alpha()
        self.tblptr = []

        self.gram = Grammer(FirstPath)
        self.errp = ErrorPro()
        self.keyWord = ['program', 'const', 'var', 'procedure', 'begin', 'end',
                        'if', 'then', 'else', 'call', 'while', 'do', 'read', 'write']

    def next_alpha(self):
        line = self.lines[self.row]
        self.alpha, self.column = LexicalAnalysis(line, self.row, self.column)
        if self.column == len(self.lines[self.row]):
            self.column = 0
            self.row = self.row + 1

        if self.row == len(self.lines):
            print('Compilter all words.')
            return False

    def in_first(self, nonter):
        if nonter == 'id':
            if self.alpha in self.keyWord:
                return False
        
        return self.gram.in_first(self.alpha, nonter)

#prog
    def prog(self):
        if self.alpha == 'program':
            self.next_alpha()
        else:
            if self.alpha in program:
                self.errp(21, self.row, self.column)
                self.next_alpha()
            elif not self.in_first('id'):
                self.errp(1, self.row, self.column)
                self.next_alpha()
            else:
                self.errp(1, self.row, self.column)
        
        self.id()

        if self.alpha == ';':
            self.next_alpha()
        else:
            self.errp(0, self.row, self.column)
            if not self.in_first('block'):
                self.next_alpha()
        
        self.block()
        
        return True

#block
    def block(self):
        if self.in_first( 'condecl'):
            if not self.condecl():
                return False
        
        if self.in_first( 'vardecl'):
            if not self.vardecl():
                return False

        if self.in_first( 'proc'):
            if not self.proc():
                return False
        
        if not self.body():
            return False
        return True

#condecl
    def condecl(self):
        if self.alpha == 'const':
            self.next_alpha()
                return False
        else:
            self.errp(2, self.row, self.column)
            if not self.in_first('const'):
                self.next_alpha()

        if not self.const():
            return False

        while True:
            if self.alpha != ',':
                if self.in_first('const'):
                    self.errp(22, self.row, self.column)
                else:
                    break
            else:
                self.next_alpha()
                    return False
            
            if not self.const():
                return False

        if self.alpha == ';':
            self.next_alpha()
                return False
        else:
            self.errp(0, self.row, self.column)

        return True

#const
    def const(self):
        self.id()
            return False

        if self.alpha == ':=':
            self.next_alpha()
                return False
            if not self.integer():
                return False
        else:
            self.errp(3, self.row, self.column)

        return True

#vardecl
    def vardecl(self):
        if self.alpha == 'var':
            self.next_alpha()
                return False
        else:
            self.errp(4, self.row, self.column)
            if not self.in_first('id'):
                self.next_alpha()

        self.id()
            return False

        while True:
            if self.alpha == ',':
                self.next_alpha()
                    return False
            else:
                if self.in_first('id'):
                    self.errp(22, self.row, self.column)
                else:
                    break

            self.id()
                return False

        if self.alpha == ';':
            self.next_alpha()
                return False
        else:
            self.errp(0, self.row, self.column)

        return True

#proc
    def proc(self):
        if self.alpha == 'procedure':
            self.next_alpha()
                return False
        else:
            self.errp(5, self.row, self.column)
            if not self.in_first('id'):
                self.next_alpha()

        self.id()
            return False

        if self.alpha == '(':
            self.next_alpha()
                return False
        else:
            self.errp(6, self.row, self.column)
            if not self.in_first('id') or self.alpha != ')':
                self.next_alpha()

        if self.in_first( 'id'):
            self.id()
                return False
            while True:
                if self.alpha == ',':
                    self.next_alpha()
                        return False
                else:
                    if self.in_first('id'):
                        self.errp(22, self.row, self.column)
                    else:
                        break
                
                self.id()
                    return False
                    
        if self.alpha == ')':
            self.next_alpha()
                return False
        else:
            self.errp(7, self.row, self.column)
            if self.alpha != ';':
                self.next_alpha()

        if self.alpha == ';':
            self.next_alpha()
                return False
        else:
            self.errp(0, self.row, self.column)
            if not self.in_first('block'):
                self.next_alpha()
        
        self.block()
            return False
        
        while True:
            if self.alpha == ';':
                self.next_alpha()
                    return False
            else:
                if self.in_first('proc'):
                    self.errp(22, self.row, self.column)
                else:
                    break
            
            if not self.proc():
                return False
        
        return True

#body
    def body(self):
        if self.alpha == 'begin':
            self.next_alpha()
                return False
        else:
            self.errp(8, self.row, self.column)
            if not self.in_first('statement'):
                self.next_alpha()
        
        if not self.statement():
            return False

        while self.alpha == ';':
            if self.alpha == ';':
                self.next_alpha()
                    return False
            else:
                if self.in_first('statement'):
                    self.errp(22, self.row, self.column)
                else:
                    break

            if not self.statement():
                return False
        
        if self.alpha == 'end':
            self.next_alpha()
                return False
        else:
            self.errp(9, self.row, self.column)

        return True

#lexp
    def lexp(self):
        if self.in_first( 'exp'):
            if not self.exp():
                return False

            if not self.lop():
                return False

            if not self.exp():
                return False

        elif self.alpha == 'odd':
            self.next_alpha()
                return False

            if not self.exp():
                return False

        else:
            self.errp(10, self.row, self.column)

        return True

#exp
    def exp(self):
        if self.alpha == '+' or self.alpha == '-':
            self.next_alpha()
                return False

        if not self.term():
            return False

        while self.in_first( 'aop'):
            if not self.aop():
                return False

            if not self.term():
                return False

        return True

#statement        
    def statement(self):
        if self.alpha == 'if':
            self.next_alpha()
                return False

            if not self.lexp():
                return False

            if self.alpha == 'then':
                self.next_alpha()
                    return False

            else:
                self.errp(11, self.row, self.column)
                if not self.in_first('statement'):
                    self.next_alpha()

            if not self.statement():
                    return False

            if self.alpha == 'else':
                self.next_alpha()
                    return False

                if not self.statement():
                    return False
            else:
                pass

        elif self.in_first( 'id'):
            self.id()
                return False

            if self.alpha == ':=':
                self.next_alpha()
                    return False
            else:
                self.errp(3, self.row, self.column)
                if not self.in_first('exp'):
                    self.next_alpha()
            
            if not self.exp():
                return False

        elif self.alpha == 'while':
            self.next_alpha()                
                return False
            
            if not self.lexp():
                return False

            if self.alpha == 'do':
                self.next_alpha()                    
                    return False
            else:
                self.errp(12, self.row, self.column)
                if not self.in_first('statement'):
                    self.next_alpha()
            
            if not self.statement():
                return False

        elif self.alpha == 'call':
            self.next_alpha()                
                return False
            
            self.id()
                return False

            if self.alpha == '(':
                self.next_alpha()
                    return False

            else:
                self.errp(6, self.row, self.column)
                if not self.in_first('exp') or self.alpha != ')':
                    self.next_alpha()

            if self.in_first( 'exp'):
                if not self.exp():
                    return False

                while True:
                    if self.alpha == ',':
                        self.next_alpha()
                            return False
                    else:
                        if self.in_first('exp'):
                            self.errp(22, self.row, self.column)
                        else:
                            break

                    if not self.exp():
                        return False
                
            if self.alpha == ')':
                self.next_alpha()                    
                    return False
            else:
                self.errp(7, self.row, self.column)

        elif self.alpha == 'read':
            self.next_alpha()                                
                return False

            if self.alpha == '(':
                self.next_alpha()                    
                    return False
            else:
                self.errp(6, self.row, self.column)
                if not self.in_first('id'):
                    self.next_alpha()

            self.id()
                return False

            while True:
                if self.alpha == ',':
                    self.next_alpha()
                        return False
                else:
                    if self.in_first('id'):
                        self.errp(22, self.row, self.column)
                    else:
                        break

                self.id()
                    return False

            if self.alpha == ')':
                self.next_alpha()                    
                    return False
            else:
                self.errp(7, self.row, self.column)

        elif self.alpha == 'write':
            self.next_alpha()                
                return False

            if self.alpha =='(':
                self.next_alpha()                    
                    return False
            else:
                self.errp(6, self.row, self.column)
                if not self.in_first('exp'):
                    self.next_alpha()

            if not self.exp():
                return False

            while self.alpha == ',':
                if self.alpha == ',':
                    self.next_alpha()
                        return False
                else:
                    if self.in_first('exp'):
                        self.errp(22, self.row, self.column)
                    else:
                        break

                if not self.exp():
                    return False

            if self.alpha == ')':
                self.next_alpha()                    
                    return False
            else:
                self.errp(7, self.row, self.column)

        elif self.in_first( 'body'):
            if not self.body():
                return False

        else:
            self.errp(13, self.row, self.column)

        return True
    
#term
    def term(self):
        if not self.factor():
            return False

        while self.in_first( 'mop'):
            if not self.mop():
                return False

            if not self.factor():
                return False
        
        return True

#factor        
    def factor(self):
        if self.in_first( 'id'):
            self.id()
                return False

        elif self.in_first( 'integer'):
            if not self.integer():
               return False

        elif self.alpha == '(':
            self.next_alpha()                
                return False

            if not self.exp():
               return False

            if self.alpha == ')':
                self.next_alpha()                    
                    return False
            else:
                self.errp(7, self.row, self.column)
        else:
            self.errp(14, self.row, self.column)

        return True

#lop
    def lop(self):
        lopList = ['=', '<>', '<', '<=', '>', '>=']
        if self.alpha in lopList:
            self.next_alpha()                
                return False

        else:
            self.errp(15, self.row, self.column)

        return True

#aop
    def aop(self):
        aopList = ['+', '-']
        if self.alpha in aopList:
            self.next_alpha()                
                return False
        else:
            self.errp(16, self.row, self.column)

        return True

#mop
    def mop(self):
        mopList = ['*', '/']
        if self.alpha in mopList:
            self.next_alpha()                
                return False
        else:
            self.errp(17, self.row, self.column)
        
        return True

#id
    def id(self):
        for index, char in enumerate(self.alpha):
            if index == 0:
                if (char <= 'Z' and char >= 'A') or (char <= 'z' and char >= 'a'):
                    pass
                else:
                    self.errp(18, self.row, self.column)
            else:
                if (char <= 'Z' and char >= 'A') or (char <= 'z' and char >= 'a'):
                    pass
                elif (char <= '9' and char >= '0'):
                    pass
                else:
                    self.errp(19, self.row, self.column)

        self.next_alpha()            
            return False

        return True
    
#integer
    def integer(self):
        for char in self.alpha:
            if (char <= '9' and char >= '0'):
                pass
            else:
                self.errp(20, self.row, self.column)

        self.next_alpha()            
            return False

        return True