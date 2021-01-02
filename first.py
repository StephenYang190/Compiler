f = open('first.txt')
lines = f.readlines()
for line in lines:
    for index, char in enumerate(line.split()):
        if index == 0:
            word = '<%s> = {' % char
        else:
            word += '\'%s\',' % char

    word = word[:-1] + '}'
    print(word)