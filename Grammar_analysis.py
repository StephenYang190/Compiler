from Analysis import Analysis
from Lexical_analysis import LexicalAnalysis

if __name__ == "__main__":

    LexicalAnalysis()
    PascalAnalysis = Analysis('out.txt', 'first.txt', 'follow.txt')
    PascalAnalysis.analysisFromFile()