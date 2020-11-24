class Generate:

    def __init__(self, Non_ter):
        self.Non_ter = Non_ter
        self.candidates = set()
        self.first = set()
        self.follow = set()
    
    def append_candidate(self, candidate):
        self.candidates.add(candidate)

    def append_first(self, ter):
        self.first.add(ter)

    def merge_first(self, non_frst):
        if non_frst in self.first:
            return False
        else:
            self.first = self.first | non_frst
            return True

    def append_follow(self, ter):
        if ter in self.follow:
            self.follow.add(ter)
            return True
        else:
            return False

    def merge_follow(self, non_fllw):
        self.follow = self.follow | non_fllw
    
    def get_first(self):
        return self.first

    def get_follow(self):
        return self.follow

    def get_candidate(self):
        return self.candidates


class Grammer:
    
    def __init__(self, Non_ters， ters, S):
        self.Non_ters = {Non_ter : Generate(Non_ter) for Non_ter in Non_ters}
        self.ters = ters
        self.S = S

    def generate_candidate(self, non_ter, alpha):
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

        
    def generate_first(self):
        #Init all first sets
        for i in self.Non_ters:
            for index, alpha in enumerate(i.get_candidate()):
                if alpha[0] in self.ters:
                    i.append_first(alpha[0])
                else:
                    continue

        #Merge the first set to former
        ChangeState = True
        while ChangeState:
            ChangeState = False
            for i in self.Non_ters:
                for index, alpha in enumerate(i.get_candidate()):
                    if alpha[0] in self.Non_ters:
                        Non_frst = self.Non_ters[alpha[0]].get_first()
                        if i.merge_first(Non_frst):
                            ChangeState = True
                    else:
                        continue

    def generate_follow(self):
        ChangeState = True
        while ChangeState:
            ChangeState = False
            for non_ter in self.Non_ters:
                for index, candidate in enumerate(non_ter.get_candidate()):
                    for i, char in enumerate(candidate):
                        if char in self.ters:
                            continue
                        else:
                            if i + 1 < len(candidate) and candidate[i + 1] in self.ters:
                                if self.Non_ters[char].append_follow(candidate[i + 1]):
                                    ChangeState = True
                            elif i + 1 < len(candidate) and candidate[i + 1] in self.Non_ters:
                                if self.Non_ters[candidate[i + 1]].get_follow() not in self.Non_ters[char].get_follow():
                                    self.Non_ters[char].merge_follow(self.Non_ters[candidate[i + 1]].get_follow())
                                    ChangeState = True
                                else:
                                    continue
                            else:
                                continue

    def recognize(self, alpha):
        stack = [S]
        for char in alpha:
            if stack[0] in self.non_ter:
            
            else:
                if stack[0] == char:
                    


                    
                        
    