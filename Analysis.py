from Grammar_analysis import Analysis

if __name__ == "__main__":

    PascalAnalysis = Analysis('in.txt', 'first.txt', 'follow.txt')
    PascalAnalysis.prog()