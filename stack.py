class stack:
    def __init__(self):
        self.param = []
        self.last = 0

    def top(self):
        return self.param[self.last]
    
    def push(self, t):
        self.param.append(t)
        self.last = self.last + 1

    def pop(self):
        self.last = self.last - 1
        return self.param.pop()

    def add(self, off):
        self.param[self.last] = self.param[self.last] + off