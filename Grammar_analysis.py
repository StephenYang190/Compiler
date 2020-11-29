from Analysis import Analysis

if __name__ == "__main__":

    PascalAnalysis = Analysis('out.txt', 'first.txt', 'follow.txt')
    PascalAnalysis.analysisFromFile()