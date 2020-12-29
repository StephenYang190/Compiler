from Grammar_analysis import Analysis
from Rearend_analysis import rear_analysis
from interpreter import interpreter


if __name__ == "__main__":

    PascalAnalysis = Analysis('in.txt', 'first.txt', 'follow.txt')
    arg = PascalAnalysis.prog()

    if arg['stop'] is not True:
        f = open('out.txt', 'w')
        for index, c in enumerate(arg["mcode"]):
            f.write('%d : %s' % (index, c))
            f.write('\n')

        RearendAnalysis = rear_analysis(arg)
        code = RearendAnalysis.analysis()

        for index, c in enumerate(code):
            f.write('%d : %s' % (index, c))
            f.write('\n')
        f.close()

        inter = interpreter(code)
        inter.forward()
    else:
        print('Have error, stop!')

