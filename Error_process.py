class ErrorPro:
    def __init__(self):
        self.Gramerror = {
            '0' : 'There should have a ;',
            '1' : 'Program should begin with \'program\'',
            '2' : 'There should have \'const\'',
            '3' : 'There should be :=',
            '4' : 'There should be \'var\'',
            '5' : 'There should be \'procedure\'',
            '6' : 'Loss a \'(\'',
            '7' : 'Loss a \')\'',
            '8' : 'There should be \'begin\'',
            '9' : 'There should be \'end\'',
            '10' : 'There should be \'odd\' or an exp',
            '11' : 'There should be \'then\'',
            '12' : 'There should be \'do\'',
            '13' : 'Don\'t statisfy the requirement of \'statement\'',
            '14' : 'Don\'t statisfy the requirement of \'factor\'',
            '15' : 'It\'s not a \'lop\'',
            '16' : 'It\'s not a \'aop\'',
            '17' : 'It\'s not a \'mop\'',
            '18' : '\'id\' should begin with letter',
            '19' : '\'id\' have illegal character',
            '20' : '\'integer\' have illegal character',
            '21' : 'Program spell mistake',
            '22' : 'Loss ,',
        }

    def error_print(self, t, row, column):
            t = str(t)
            
            print('Row %s Column %s: ' % (row, column))
            print(self.Gramerror[t])