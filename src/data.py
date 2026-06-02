class datahandler():
    def __init__(self):
        pass
    def save_current_level(self, lvlnum):
        with open("userdata.txt", "w") as file:
            file.write(str(lvlnum) + "\n")
    def get_saved_level(self):
        try:
            with open("userdata.txt", 'r') as file:
                lines = file.readlines()
                if lines:
                    return int(lines[0].strip())
            return 1
        except FileNotFoundError:
            return 1
