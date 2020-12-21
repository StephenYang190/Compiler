def errorProcess(t, row, column, char = ''):
    error = {
        '0' : "Don't have = after : %s",
        '1' : "Don't have %s in the grammer",
        '2' : "Integer can not have letter %s",
    }

    print('Row %s Column %s : ' + error[str(t)] % row, column, char)


def LexicalAnalysis(line, row, column):
    state = 0
    anaFinish = False
    
    symbolList = [',', '/', '*', '+', '-', '=', '(', ')', ';']

    print('Star getting word.')    
    while column < len(line):
        char = line[column]

        #state: 0 haven't read any things / 1 read letter / 2 read integer
        if state == 0:
            if char == ' ' or char == '\n' or char == '\t':
                pass
            elif char == ':':
                if column + 1 < len(line) and line[column + 1] == '=':
                    column = column + 1
                    word = ':='
                    anaFinish = True
                else:
                    errorProcess(0, row, column)
            elif char >= '0' and char <= '9':
                word = char
                state = 2
            elif char >= 'a' and char <= 'z':
                word = char
                state = 1
            elif char in symbolList:
                word = char
                anaFinish = True
            elif char == '<':
                if column + 1 < len(line) and line[column + 1] == '=':
                    word = '<='
                    column = column + 1
                    anaFinish = True
                elif column + 1 < len(line) and line[column + 1] == '>':
                    word = '<>'
                    column = column + 1
                    anaFinish = True
                else:
                    word = '<'
                    anaFinish = True
            elif char == '>':
                if column + 1 < len(line) and line[column + 1] == '=':
                    word = '>='
                    column = column + 1
                    anaFinish = True
                else:
                    word = '>'
                    anaFinish = True
            else:
                errorProcess(1, row, column, char)
                anaFinish = True
            column = column + 1
            
            
        elif state == 1:
            if char >= 'a' and char <= 'z':
                word = word + char
                column = column + 1
            elif char >= 'A' and char <= 'Z':
                word = word + char
                column = column + 1
            elif char >= '0' and char <= '9':
                word = word + char
                column = column + 1
            elif char in symbolList:
                anaFinish = True
            elif char == ':' or char == '<' or char == '>' or char == ' ' or char == '\n':
                anaFinish = True
            else:
                anaFinish = True
                errorProcess(1, row, column, char)
                column = column + 1

        else:
            if char >= '0' and char <= '9':
                word = word + char
                column = column + 1
            elif char >= 'a' and char <= 'z':
                errorProcess(2, row, column)
                column = column + 1
            elif char >= 'A' and char <= 'Z':
                errorProcess(2, row, column)
                column = column + 1
            elif char in symbolList:
                anaFinish = True
            elif char == ':' or char == '<' or char == '>' or char == ' ' or char == '\n':
                anaFinish = True
            else:
                anaFinish = True
                errorProcess(2, row, column)
                column = column + 1
        if anaFinish:
            break

    print('Get : ', word)

    return word, column