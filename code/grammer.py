class NonTer:

    def __init__(self, Non_ter):
        self.Non_ter = Non_ter
        self.first = set()
        self.follow = set()

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


class Grammer:
    
    def __init__(self, FilePath):
        infile = open(FilePath, 'r')
        lines = infile.readlines()
        self.Nonters = {}
        for line in lines:
            words = line.split()
            self.Nonters[words[0]] = NonTer(words[0])
            for index, word in enumerate(words):
                if index == 0:
                    self.Nonters[word] = NonTer(word)
                else:
                    self.Nonters[words[0]].append_first(word)


    def in_first(self, alpha, nonter):
        first = self.Nonters[nonter].get_first()
        crit1 = False
        crit2 = False

        if 'd' in first:
            crit2 = (alpha >= '0' and alpha <= '9')

        if 'l' in first:
            crit1 = ((alpha >= 'a' and alpha <= 'z') or (alpha >= 'A' and alpha <= 'Z'))        

        return (alpha in first and alpha != 'd' ) or crit1 or crit2