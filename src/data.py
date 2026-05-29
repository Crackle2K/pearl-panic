import levels
class data():
    def __init__(self, lvlnum):
        self.current_lvl = lvlnum
        self.data = open("userdata.txt", 'a')
        lines = self.data.readlines()
        self.data.write(str(self.current_lvl) + '\n')
        self.data.close()
        if lines[0].strip() == '1':
            levels.level1()
        elif lines[0].strip() == '2': 
            levels.level2()
        elif lines[0].strip() == '3':
            levels.level3()