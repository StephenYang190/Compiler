from Grammar_analysis import Analysis
from Lexical_analysis import LexicalAnalysis

if __name__ == "__main__":

    PascalAnalysis = Analysis('in.txt', 'first.txt', 'follow.txt')
    PascalAnalysis.prog()