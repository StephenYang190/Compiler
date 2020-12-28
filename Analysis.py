from Grammar_analysis import Analysis
from Rearend_analysis import rear_analysis
from interpreter import interpreter


if __name__ == "__main__":

    PascalAnalysis = Analysis('in.txt', 'first.txt', 'follow.txt')
    arg = PascalAnalysis.prog()
    RearendAnalysis = rear_analysis(arg)
    code = RearendAnalysis.analysis()
    RearendAnalysis.print()
    inter = interpreter(code)
    inter.forward()