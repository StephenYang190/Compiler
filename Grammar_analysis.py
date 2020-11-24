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
        self.alpha = l
        slef.gram = Grammer()

    def next_alpha(self):

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
        }
        print(error[t])

    def prog(self):
        if self.alpha == 'program':
            self.next_alpha()
            self.id()
            if self.alpha == ';':
                self.block()
            else:
                self.error_print(0)    
        else:
            self.error_print(1)

    def block(self):
        if self.gram.in_first(self.alpha, 'condecl'):
            self.condecl()
        
        if self.gram.in_first(self.alpha, 'vardecl'):
            self.vardecl()

        if self.gram.in_first(self.alpha, 'proc'):
            self.proc()
        
        self.body()

    def condecl(self):
        if self.alpha = 'const':
            self.next_alpha()
            self.const()

            while self.alpha == ',':
                self.next_alpha()
                self.const()
        else:
            self.error_print(2)

    def const(self):
        self.id()
        if self.alpha == ':=':
            self.next_alpha()
            self.integer()
        else:
            self.error_print(3)

    def vardecl(self):
        if self.alpha == 'var':
            self.next_alpha()
            self.id()
            while self.alpha == ',':
                self.next_alpha()
                self.id()
            if self.alpha == ';':
                self.next_alpha()
            else:
                self.error_print(0)
        else:
            self.error_print(4)

    def proc(self):
        if self.alpha == 'procedure':
            self.next_alpha()
            self.id()
            if self.alpha == '(':
                if self.gram.in_first(self.alpha, 'id'):
                    self.id()
                    while self.alpha == ',':
                        self.next_alpha()
                        self.id()
                if self.alpha == ')':
                    self.next_alpha()
                else:
                    self.error_print(7)
            else:
                self.error_print(6)

        else:
            self.error_print(5)  

                
                    


                    
                        
    