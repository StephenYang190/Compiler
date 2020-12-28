from stack import stack


class Item:
    def __init__(self, name, type=None, offset=None, value=None):
        self.name = name
        self.type = type
        self.offset = offset
        self.value = value

    def printitem(self, i):
        print('%d : %s, %s, %d' % (i, self.name, self.type, self.offset))


class table:
    def __init__(self, previous, id, idname):
        self.previous = previous
        self.width = 0
        self.items = []
        self.level = id
        self.name = idname
        self.quad = 0

    def enter(self, name, t, offset, value=0):
        self.items.append(Item(name, t, offset, value))

    def addwidth(self, offset):
        for item in self.items:
            if item.type == 'var':
                self.width += 1

    def setquad(self, quad):
        self.quad = quad

    def enterproc(self, name, newtable):
        self.items.append(Item(name, 'table', offset=newtable.width, value=newtable))

    def lookup(self, idname):
        for index, item in enumerate(self.items):
            if idname == item.name:
                if item.type == 'const':
                    return idname + '|c|' + str(item.value)
                return idname + '|v|' + str(index) + '|0'
        if self.previous is None:
            return None
        index = self.previous.lookup(idname)
        if index is not None:
            if index.split('|')[1] == 'c':
                return index
            else:
                l = index[-1]
                l = str(int(l) + 1)
                index = index[:-1] + l
        return index

    def printable(self):
        print('table name : %s' % self.name)
        print('table layer : %d' % self.level)
        print('table begin : %d' % self.quad)
        if self.previous is None:
            print('previous: None')
        else:
            print('previous: %d' % self.previous.level)
        print('width : %d' % self.width)
        for index, item in enumerate(self.items):
            item.printitem(index)


class table_manager:
    def __init__(self):
        self.tblpter = stack()
        self.tblpter_back = []
        self.first_tb = None

    def mktable(self, pre, idname, layer):
        newt = table(pre, layer, idname)
        self.tblpter.push(newt)
        self.tblpter_back.append(newt)
        if self.first_tb is None:
            self.first_tb = idname
        return newt

    def top(self):
        return self.tblpter.top()

    def pop(self):
        self.tblpter.pop()

    def setquad(self, quad):
        t = self.tblpter.top()
        t.setquad(quad)

    def tbval(self, idname):
        for t in self.tblpter_back:
            if t.name == idname:
                return t.width

    def iterlist(self):
        return self.tblpter_back

    def level(self, idname):
        for t in self.tblpter_back:
            if t.name == idname:
                return t.level - self.tblpter.top().level

    def probegin(self, idname):
        for t in self.tblpter_back:
            if t.name == idname:
                return t.quad

    def first(self):
        return self.first_tb


