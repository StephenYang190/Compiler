class NonTer:

    def __init__(self, Non_ter):
        self.Non_ter = Non_ter
        self.candidates = set()
        self.first = set()
        self.follow = set()
    
    def append_candidate(self, candidate):
        self.candidates.add(candidate)

    def append_first(self, ter):
        self.first.add(ter)

    def append_follow(self, ter):
        if ter in self.follow:
            self.follow.add(ter)
            return True
        else:
            return False
    
    def get_first(self):
        return self.first

    def get_follow(self):
        return self.follow

    def get_candidate(self):
        return self.candidates


class Grammer:
    
    def __init__(self, nonters, ters, S):
        self.Nonters = {Non_ter : NonTer(Non_ter) for Non_ter in nonters}
        self.ters = ters
        self.S = S

    def NonTer_candidate(self, non_ter, alpha):
        self.Nonters[non_ter].append_candidate(alpha)

    def firstSet(self, alpha):
        if alpha[0] in self.ters:
            return alpha[0], False
        else:
            frstSet = self.Nonters[alpha[0]]
            if 'ε' in frstSet:
                if len(alpha) > 1:
                    frstSet, flag = firstSet(alpha[1:])
                    frstSet = frstSet | firstSet(alpha[1:])
                    frstSet = frstSet.remove('ε')
                    return frstSet, True
                else:
                    return frstSet, True
            else:
                return frstSet, False

    def recognize(self, filename):
        stack = [self.S]
        with open(filename, 'r') as in:
            lines = in.readlines()
            for alpha in lines:

    def in_first(self, alpha, nonter):
        first = self.Nonters[nonter].get_first()
        return (alpha in first)

class Analysis:
    def __init__(self, FilePath):
        self.lines = open(FilePath, 'r').readlines()
        self.alpha = self.lines[0]
        self.index = 0
        slef.gram = Grammer()

    def next_alpha(self):
        self.index = self.index + 1
        if self.index < len(self.lines):
            self.alpha = self.lines[self.index]
            return True
        else:
            print('Compilter all words.')
            return False

    def error_print(self, t):
        t = str(t)
        error = {
            '0' : 'There should have a ;',
            '1' : 'Program should begin with \'program\'',
            '2' : 'There should have \'const\'',
            '3' : 'There should be :=',
            '4' : 'There should be \'var\'',
            '5' : 'There should be \'procedure\'',
            '6' : 'Loss a \'(\'',
            '7' : 'Loss a \')\'',
            '8' : 'There should be \'begin\'',
            '9' : 'There should be \'end\'',
            '10' : 'There should be \'odd\' or an exp',
            '11' : 'There should be \'then\'',
            '12' : 'There should be \'do\'',
            '13' : 'Don\'t statisfy the requirement of \'statement\'',
            '14' : 'Don\'t statisfy the requirement of \'factor\'',
            '15' : 'It\'s not a \'lop\'',
            '16' : 'It\'s not a \'aop\'',
            '17' : 'It\'s not a \'mop\'',
            '18' : '\'id\' should begin with letter',
            '19' : '\'id\' have illegal character',
            '20' : '\'integer\' have illegal character',
            '21' : 'Program is missing \'id\' part',
            '22' : 'Program is missing \'const\' part',
            '23' : 'Program is missing \'body\' part',
            '24' : 'Program is missing \'block\' part',
            '25' : 'Program is missing \'integer\' part',
            '26' : 'Program is missing \'condecl\' part',
            '27' : 'Program is missing \'vardecl\' part',
            '28' : 'Program is missing \'proc\' part',
            '29' : 'Program is missing \'statement\' part',
        }
        print(error[t])

#prog
    def prog(self):
        if self.alpha == 'program':
            if not self.next_alpha():
                self.error_print(21)
                self.error_print(24)
                return False
        else:
            self.error_print(1)
        
        if not self.id():
            self.error_print(21)
            self.error_print(24)
            return False

        if self.alpha == ';':
            if not self.next_alpha():
                self.error_print(24)
                return False
        else:
            self.error_print(0)
        
        if not self.block():
            self.error_print(24)
            return False
        
        return True

#block
    def block(self):
        if self.gram.in_first(self.alpha, 'condecl'):
            if not self.condecl():
                self.error_print(26)
                self.error_print(23)
                return False
        
        if self.gram.in_first(self.alpha, 'vardecl'):
            if not self.vardecl():
                self.error_print(27)
                self.error_print(23)
                return False

        if self.gram.in_first(self.alpha, 'proc'):
            if not self.proc():
                self.error_print(28)
                self.error_print(23)
                return False
        
        if not self.body():
            self.error_print(23)
            return False
        return True

#condecl
    def condecl(self):
        if self.alpha = 'const':
            if not self.next_alpha():
                self.error_print(22)
                return False
        else:
            self.error_print(2)

        if not self.const():
            self.error_print(22)
            return False

        while self.alpha == ',':
            if not self.next_alpha():
                self.error_print(22)
                return False
            
            if not self.const():
                self.error_print(22)
                return False
        
        return True

#const
    def const(self):
        self.id()

        if self.alpha == ':=':
            if not self.next_alpha():
                self.error_print(25)
                return False
            if not self.integer():
                return False
        else:
            self.error_print(3)

        return True

#vardecl
    def vardecl(self):
        if self.alpha == 'var':
            if not self.next_alpha():
                self.error_print(21)
                return False
        else:
            self.error_print(4)

        if not self.id():
            self.error_print(21)
                return False

        while self.alpha == ',':
            if not self.next_alpha():
                self.error_print(21)
                return False
            if not self.id():
                self.error_print(21)
                return False

        if self.alpha == ';':
            if not self.next_alpha():
                return False
        else:
            self.error_print(0)

        return True

#proc
    def proc(self):
        if self.alpha == 'procedure':
            if not self.next_alpha():
                self.error_print(21)
                return False
        else:
            self.error_print(5)

        if not self.id():
            
            return False

        if self.alpha == '(':
            if not self.next_alpha():
                self.error_print(7)
                return False
        else:
            self.error_print(6)

        if self.gram.in_first(self.alpha, 'id'):
            if not self.id():
                self.error_print(21)
                return False
            while self.alpha == ',':
                if not self.next_alpha():
                    self.error_print(21)
                    return False
                if not self.id():
                    self.error_print(21)
                    return False
                    
        if self.alpha == ')':
            if not self.next_alpha():
                self.error_print(24)
                return False
        else:
            self.error_print(7)

        if self.alpha == ';':
            if not self.next_alpha():
                self.error_print(24)
                return False
        else:
            self.error_print(0)
        
        if not self.block():
            return False
        
        while self.alpha == ';':
            if not self.next_alpha():
                self.error_print(28)
                return False
            
            if not self.proc():
                return False
        
        return True

#body
    def body(self):
        if self.alpha == 'begin':
            if not self.next_alpha():
                self.error_print(29)
                return False
        else:
            self.error_print(8)
        
        if not self.statement():
            return False

        while self.alpha == ';':
            if not self.next_alpha():
                self.error_print(21)
                return False
            if not self.statement():
                return False
        
        if self.alpha == 'end':
            if not self.next_alpha():
                self.error_print(21)
                return False
        else:
            self.error_print(9)

        return True

    def lexp(self):
        if self.gram.in_first(self.alpha, 'exp'):
            self.exp()
            self.lop()
            self.exp()
        elif self.alpha == 'odd':
            if not self.next_alpha():
                self.error_print(21)
                return False
            self.exp()
        else:
            self.error_print(10)

    def exp(self):
        if self.alpha == '+' or self.alpha == '-':
            if not self.next_alpha():
                self.error_print(21)
                return False
        self.term()
        while self.gram.in_first(self.alpha, 'aop'):
            self.aop()
            self.term()
        
    def statement(self):
        if self.alpha == 'if':
            if not self.next_alpha():
                self.error_print(21)
                return False
            self.lexp()
            if self.alpha == 'then':
                if not self.next_alpha():
                self.error_print(21)
                return False
                self.statement()
                if self.alpha == 'else':
                    if not self.next_alpha():
                self.error_print(21)
                return False
                    self.statement()
            else:
                self.error_print(11)
        elif self.gram.in_first(self.alpha, 'id'):
            self.id()
            if self.alpha == ':=':
                if not self.next_alpha():
                self.error_print(21)
                return False
                self.exp()
            else:
                self.error_print(3)
        elif self.alpha == 'while':
            if not self.next_alpha():
                self.error_print(21)
                return False
            self.lexp()
            if self.alpha == 'do':
                if not self.next_alpha():
                self.error_print(21)
                return False
                self.statement()
            else:
                self.error_print(12)
        elif self.alpha == 'call':
            if not self.next_alpha():
                self.error_print(21)
                return False
            self.id()
            if self.alpha == '(':
                if not self.next_alpha():
                self.error_print(21)
                return False
            else:
                self.error_print(6)
            if self.gram.in_first(self.alpha, 'exp'):
                self.exp()
                while self.alpha == ',':
                    if not self.next_alpha():
                self.error_print(21)
                return False
                    self.exp()
                
            if self.alpha == ')':
                if not self.next_alpha():
                self.error_print(21)
                return False
            else:
                self.error_print(7)
        elif self.alpha == 'read':
            if not self.next_alpha():
                self.error_print(21)
                return False
            if self.alpha == '(':
                if not self.next_alpha():
                self.error_print(21)
                return False
            else:
                self.error_print(6)
            self.id()
            while self.alpha == ',':
                if not self.next_alpha():
                self.error_print(21)
                return False
                self.id()
            if self.alpha == ')':
                if not self.next_alpha():
                self.error_print(21)
                return False
            else:
                self.error_print(7)
        elif self.alpha == 'write':
            if not self.next_alpha():
                self.error_print(21)
                return False
            if self.alpha =='(':
                if not self.next_alpha():
                self.error_print(21)
                return False
            else:
                self.error_print(6)
            self.exp()
            while self.alpha == ',':
                if not self.next_alpha():
                self.error_print(21)
                return False
                self.exp()
            if self.alpha == ')':
                if not self.next_alpha():
                self.error_print(21)
                return False
            else:
                self.error_print(7)
        elif self.gram.in_first(self.alpha, 'body'):
            self.body()
        else:
            self.error_print(13)
    
    def term(self):
        self.factor()
        while self.gram.in_first(self.alpha, 'mop'):
            self.mop()
            self.factor()
        
    def factor(self):
        if self.gram.in_first(self.alpha, 'id'):
            self.id()
        elif self.gram.in_first(self.alpha, 'integer'):
            self.integer()
        elif self.alpha == '(':
            if not self.next_alpha():
                self.error_print(21)
                return False
            self.exp()
            if self.alpha == ')':
                if not self.next_alpha():
                self.error_print(21)
                return False
            else:
                self.error_print(7)
        else:
            self.error_print(14)

    def lop(self):
        lopList = ['=', '<>', '<', '<=', '>', '>=']
        if self.alpha in lopList:
            if not self.next_alpha():
                self.error_print(21)
                return False
        else:
            self.error_print(15)

    def aop(self):
        aopList = ['+', '-']
        if self.alpha in aopList:
            if not self.next_alpha():
                self.error_print(21)
                return False
        else:
            self.error_print(16)
    
    def mop(self):
        mopList = ['*', '/']
        if self.alpha in mopList:
            if not self.next_alpha():
                self.error_print(21)
                return False
        else:
            self.error_print(17)

    def id(self):
        for index, char in enumerate(self.alpha):
            if index == 0:
                if (self.alpha < 'Z' and self.alpha > 'A') or (self.alpha < 'z' and self.alpha > 'a'):
                    pass
                else:
                    self.error_print(18)
            else:
                if (self.alpha <= 'Z' and self.alpha >= 'A') or (self.alpha <= 'z' and self.alpha >= 'a'):
                    pass
                elif (self.alpha <= '9' and self.alpha >= '0'):
                    pass
                else:
                    self.error_print(19)
    
    def integer(self):
        for index, char in enumerate(self.alpha):
            if (self.alpha <= '9' and self.alpha >= '0'):
                pass
            else:
                self.error_print(20)
            
            
    