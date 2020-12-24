class Item:
    def __init__(self, name, type=None, offset=None, value=None):
        self.name = name
        self.type = type
        self.offset = offset
        self.value = value


class table:
    def __init__(self, previous):
        self.previous = previous
        self.width = 0
        self.items = []

    def enter(self, name, t, offset, value=0):
        self.items.append(Item(name, t, offset, value))

    def addwidth(self, offset):
        self.width = offset

    def enterproc(self, name, newtable):
        self.items.append(Item(name, 'table', value=newtable))

    def lookup(self, idname):
        if idname in self.name:
            return self.name.index(idname)
        else:
            return None
