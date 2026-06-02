"""
Authors: Dinesh Sinnathamby and Dhani Shah
Date: June 2nd, 2026
Description: This file handles user data persistence for Pearl Panic. It saves and loads the player's current selected level to a local text file.
"""

class DataHandler():
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
