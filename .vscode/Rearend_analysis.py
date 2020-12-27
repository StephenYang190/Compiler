from table import table_manager


class rear_analysis:
    def __init__(self, codes, tbmng):
        self.mcodes = codes
        self.codes = []
        self.tbmng = tbmng

    def analysis(self):
        paramlist = []
        for mcode in self.mcodes:
            mcodes = mcode.split()
            if mcodes[0] == 'write':
                self.codes.append()
                self.codes.append('WRT 0 0')

            elif mcodes[0] == 'read':
                _, l, a = mcodes[1].split('|')
                self.codes.append('RED %d %d' % (l, a))
            elif mcodes[0] == 'param':
                paramlist.append(mcodes)
            elif mcodes[0] == 'call':
                self.codes.append('INT %d' % mcodes[2])
                for param in paramlist:
                    _, l, a, t = param[1].split('|')
                    if t == 'const':


            elif mcodes[0] == 'j':

            elif 'j' in mcodes[0]:

            else:


