def errorProcess(t):
    error = {
        0 : "Don't have = after :",
        1 : "Don't have this char in the grammer",
        2 : "Integer can not have letter",
    }

    print(error[t])



if __name__ == "main":
    in_file = ""
    out_file = ""
    state = 0

    with open(in_file, 'r') as in:
        out = open(out_file, 'w')
        lines = in.readlines()

        column = 0
        row = 0
        state = 0
        for line in lines:
            column = 0
            word = ""
            while column < line.size():
                char = line[column]

                #state: 0 haven't read any things / 1 read letter / 2 read integer
                if state == 0:
                    if char == ' ':
                        pass
                    elif char == ':':
                        if column + 1 < line.size() and line[column + 1] == '=':
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
                    elif (char >= '*' and char <= '+') or (char >= ';' and char <= '>') or char == '/':
                        out.write(char + '\n')
                    else:
                        errorProcess(1)
                    column = column + 1
                    
                elif state == 1:
                    if char >= 'a' and char <= 'z':
                        word = word + char
                        column = column + 1
                    elif char >= '0' and char <= '9':
                        word = word + char
                        column = column + 1
                    elif (char >= '*' and char <= '+') or (char >= ';' and char <= '>') or char == '/':
                        out.write(word + '\n')
                        state = 0
                    elif char == ':':
                        out.write(word + '\n')
                        state = 0
                    else:
                        out.write(word + '\n')
                        state = 0
                        errorProcess(1)
                        column = column + 1

                else:
                    if char >= '0' and char <= '9':
                        word = word + char
                        column = column + 1
                    elif char >= 'a' and char <= 'z':
                        errorProcess(2)
                        column = column + 1
                    elif (char >= '*' and char <= '+') or (char >= ';' and char <= '>') or char == '/':
                        out.write(word + '\n')
                        state = 0
                    elif char == ':':
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

                