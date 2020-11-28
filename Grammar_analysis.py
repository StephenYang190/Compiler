from grammer import Grammer

class Analysis:
    def __init__(self, FilePath, FirstPath, FollowPath=''):
        self.lines = open(FilePath, 'r').readlines()
        self.alpha = self.lines[0]
        self.index = 0
        self.gram = Grammer(FirstPath)

    def next_alpha(self):
        self.index = self.index + 1
        if self.index < len(self.lines):
            self.alpha = self.lines[self.index]
            return True
        else:
            print('Compilter all words.')
            return False

    def analysisFromFile(self):
        self.prog()

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
        if self.alpha == 'const':
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

#lexp
    def lexp(self):
        if self.gram.in_first(self.alpha, 'exp'):
            if not self.exp():
                return False

            if not self.lop():
                return False

            if not self.exp():
                return False

        elif self.alpha == 'odd':
            if not self.next_alpha():
                self.error_print(21)
                return False

            if not self.exp():
                return False

        else:
            self.error_print(10)

        return True

#exp
    def exp(self):
        if self.alpha == '+' or self.alpha == '-':
            if not self.next_alpha():
                self.error_print(21)
                return False

        if not self.term():
            return False

        while self.gram.in_first(self.alpha, 'aop'):
            if not self.aop():
                return False

            if not self.term():
                return False

        return True

#statement        
    def statement(self):
        if self.alpha == 'if':
            if not self.next_alpha():
                self.error_print(21)
                return False

            if not self.lexp():
                return False

            if self.alpha == 'then':
                if not self.next_alpha():
                    self.error_print(21)
                    return False

            else:
                self.error_print(11)

            if not self.statement():
                    return False

            if self.alpha == 'else':
                if not self.next_alpha():
                    self.error_print(21)
                    return False

                if not self.statement():
                    return False
            else:
                pass

        elif self.gram.in_first(self.alpha, 'id'):
            if not self.id():
                return False

            if self.alpha == ':=':
                if not self.next_alpha():
                    self.error_print(21)
                    return False
            else:
                self.error_print(3)
            
            if not self.exp():
                return False

        elif self.alpha == 'while':
            if not self.next_alpha():
                self.error_print(21)
                return False
            
            if not self.lexp():
                return False

            if self.alpha == 'do':
                if not self.next_alpha():
                    self.error_print(21)
                    return False
            else:
                self.error_print(12)
            
            if not self.statement():
                return False

        elif self.alpha == 'call':
            if not self.next_alpha():
                self.error_print(21)
                return False
            
            if not self.id():
                return False

            if self.alpha == '(':
                if not self.next_alpha():
                    self.error_print(21)
                    return False

            else:
                self.error_print(6)

            if self.gram.in_first(self.alpha, 'exp'):
                if not self.exp():
                    return False

                while self.alpha == ',':
                    if not self.next_alpha():
                        self.error_print(21)
                        return False

                    if not self.exp():
                        return False
                
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

            if not self.id():
                return False

            while self.alpha == ',':
                if not self.next_alpha():
                    self.error_print(21)
                    return False
                if not self.id():
                    return False

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

            if not self.exp():
                return False

            while self.alpha == ',':
                if not self.next_alpha():
                    self.error_print(21)
                    return False

                if not self.exp():
                    return False

            if self.alpha == ')':
                if not self.next_alpha():
                    self.error_print(21)
                    return False
            else:
                self.error_print(7)

        elif self.gram.in_first(self.alpha, 'body'):
            if not self.body():
                return False

        else:
            self.error_print(13)

        return True
    
#term
    def term(self):
        if not self.factor():
            return False

        while self.gram.in_first(self.alpha, 'mop'):
            if not self.mop():
                return False

            if not self.factor():
                return False
        
        return True

#factor        
    def factor(self):
        if self.gram.in_first(self.alpha, 'id'):
            if not self.id():
                return False

        elif self.gram.in_first(self.alpha, 'integer'):
            if not self.integer():
               return False

        elif self.alpha == '(':
            if not self.next_alpha():
                self.error_print(21)
                return False

            if not self.exp():
               return False

            if self.alpha == ')':
                if not self.next_alpha():
                    self.error_print(21)
                    return False
            else:
                self.error_print(7)
        else:
            self.error_print(14)

        return True

#lop
    def lop(self):
        lopList = ['=', '<>', '<', '<=', '>', '>=']
        if self.alpha in lopList:
            if not self.next_alpha():
                self.error_print(21)
                return False

        else:
            self.error_print(15)

        return True

#aop
    def aop(self):
        aopList = ['+', '-']
        if self.alpha in aopList:
            if not self.next_alpha():
                self.error_print(21)
                return False
        else:
            self.error_print(16)

        return True

#mop
    def mop(self):
        mopList = ['*', '/']
        if self.alpha in mopList:
            if not self.next_alpha():
                self.error_print(21)
                return False
        else:
            self.error_print(17)
        
        return True

#id
    def id(self):
        for index, char in enumerate(self.alpha):
            if index == 0:
                if (char < 'Z' and char > 'A') or (char < 'z' and char > 'a'):
                    pass
                else:
                    self.error_print(18)
            else:
                if (char <= 'Z' and char >= 'A') or (char <= 'z' and char >= 'a'):
                    pass
                elif (char <= '9' and char >= '0'):
                    pass
                else:
                    self.error_print(19)

        if not self.next_alpha():
            self.error_print(21)
            return False

        return True
    
#integer
    def integer(self):
        for char in self.alpha:
            if (char <= '9' and char >= '0'):
                pass
            else:
                self.error_print(20)

        if not self.next_alpha():
            self.error_print(21)
            return False

        return True
            
            
if __name__ == "__main__":

    PascalAnalysis = Analysis('out.txt', 'first,txt', 'follow.txt')
    PascalAnalysis.analysisFromFile()
