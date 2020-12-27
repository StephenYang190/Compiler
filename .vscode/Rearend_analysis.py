from table import table_manager


class rear_analysis:
    def __init__(self, codes):
        self.mcodes = codes
        self.codes = []

    def analysis(self):
        paramlist = []
        for mcode in self.mcodes:
            mcodes = mcode.split()
            if mcodes[2] == 'write':
                self.codes.append()
                self.codes.append('WRT 0 0')

            elif mcodes[2] == 'read':
                _, l, a = mcodes[3].split('|')
                self.codes.append('RED %d %d' % (l, a))
            elif mcodes[2] == 'param':
                paramlist.append(mcodes)
            elif mcodes[2] == 'call':
                self.codes.append('INT %d' % mcodes[4])
                for param in paramlist:


            elif mcodes[2] == 'j':

            elif 'j' in mcodes[2]:

            else:
