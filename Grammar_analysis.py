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
    
    def __init__(self, Non_ters， ters, S):
        self.Non_ters = {Non_ter : NonTer(Non_ter) for Non_ter in Non_ters}
        self.ters = ters
        self.S = S

    def NonTer_candidate(self, non_ter, alpha):
        self.Non_ters[non_ter].append_candidate(alpha)

    def firstSet(self, alpha):
        if alpha[0] in self.ters:
            return alpha[0], False
        else:
            frstSet = self.Non_ters[alpha[0]]
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

class Analysis:
    def __init__(self, FilePath):
        self.lines = open(FilePath, 'r').readlines()
        self.alpha = l

    def next_alpha(self):

    def error_print(self, t):


    def prog(self):
        if alpha == "program":
            self.next_alpha()
            self.id()
            if alpha == ";":
                self.block()
            else:
                self.error_print()    
        else:
            self.error_print()

    def block(self):

    def condecl(self):
        if alpha 


                
                    


                    
                        
    