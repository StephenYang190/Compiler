def errorProcess(t, char = ''):
    error = {
        '0' : "Don't have = after : %s",
        '1' : "Don't have %s in the grammer",
        '2' : "Integer can not have letter %s",
    }

    print(error[str(t)] % char)


in_file = "in.txt"
out_file = "out.txt"
state = 0

symbolList = [',', '/', '*', '+', '-', '=', '(', ')', ';']

with open(in_file, 'r') as infile:
    print('Begin')
    out = open(out_file, 'w')
    lines = infile.readlines()

    column = 0
    row = 0
    state = 0
    for line in lines:
        column = 0
        word = ""
        while column < len(line):
            char = line[column]

            #state: 0 haven't read any things / 1 read letter / 2 read integer
            if state == 0:
                if char == ' ' or char == '\n':
                    pass
                elif char == ':':
                    if column + 1 < len(line) and line[column + 1] == '=':
                        out.write(':=\n')
                        column = column + 1
                    else:
                        errorProcess(0)
                elif char >= '0' and char <= '9':
                    word = char
                    state = 2
                elif char >= 'a' and char <= 'z':
                    word = char
                    state = 1
                elif char in symbolList:
                    out.write(char + '\n')
                elif char == '<':
                    if column + 1 < len(line) and line[column + 1] == '=':
                        out.write('<=\n')
                        column = column + 1
                    elif column + 1 < len(line) and line[column + 1] == '>':
                        out.write('<>\n')
                        column = column + 1
                    else:
                        out.write('<\n')
                elif char == '>':
                    if column + 1 < len(line) and line[column + 1] == '=':
                        out.write('>=\n')
                        column = column + 1
                    else:
                        out.write('>\n')
                else:
                    errorProcess(1, char)
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
                    out.write(word + '\n')
                    state = 0
                elif char == ':' or char == '<' or char == '>' or char == ' ' or char == '\n':
                    out.write(word + '\n')
                    state = 0
                else:
                    out.write(word + '\n')
                    state = 0
                    errorProcess(1, char)
                    column = column + 1

            else:
                if char >= '0' and char <= '9':
                    word = word + char
                    column = column + 1
                elif char >= 'a' and char <= 'z':
                    errorProcess(2)
                    column = column + 1
                elif char >= 'A' and char <= 'Z':
                    errorProcess(2)
                    column = column + 1
                elif char in symbolList:
                    out.write(word + '\n')
                    state = 0
                elif char == ':' or char == '<' or char == '>' or char == ' ' or char == '\n':
                    out.write(word + '\n')
                    state = 0
                else:
                    out.write(word + '\n')
                    state = 0
                    errorProcess(2)
                    column = column + 1
            
        out.write(word + '\n')
        state = 0
        row = row + 1

    out.close()
    print('End')       