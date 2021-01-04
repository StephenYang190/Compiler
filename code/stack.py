class stack:
    def __init__(self):
        self.param = []
        self.last = None

    def top(self):
        return self.param[self.last]

    def push(self, t):
        self.param.append(t)
        if self.last is None:
            self.last = 0
        else:
            self.last = self.last + 1

    def pop(self):
        self.last = self.last - 1
        return self.param.pop()

    def add(self, off):
        self.param[self.last] = self.param[self.last] + off

    def lookup(self, idname, fun):
        for p in self.param:
            if fun(p) == idname:
                return p
        return None

    def set(self, index, value):
        self.param[index] = value

    def prints(self):
        stack = ""
        for i in self.param:
            stack += ' %d' % i
        return stack

    def __getitem__(self, i):
        return self.param[i]
