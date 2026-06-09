"""
Authors: Dinesh Sinnathamby and Dhani Shah
Date: June 2nd, 2026
Description: This file handles user data persistence for Pearl Panic. It saves and loads the player's current selected level to a local text file.
"""

class DataHandler():

    def __init__(self):
        """Just sets up the DataHandler — nothing to configure here, it reads and writes files on demand."""
        pass

    def save_current_level(self, lvlnum):
        """Writes the player's chosen level to the save file so it's remembered next time they open the game."""
        max_unlocked = self.get_max_unlocked()
        # Open the file and write both the current level and the highest level ever reached
        with open("userdata.txt", "w") as file:
            file.write(str(lvlnum) + "\n")
            file.write(str(max_unlocked) + "\n")

    def save_max_unlocked(self, level):
        """Updates the record for the furthest level the player has ever reached without overwriting the current selection."""
        current = self.get_saved_level()
        # Rewrite the file, keeping the current level but bumping up the max unlocked number
        with open("userdata.txt", "w") as file:
            file.write(str(current) + "\n")
            file.write(str(level) + "\n")

    def get_saved_level(self):
        """Reads the save file and returns which level the player last selected, defaulting to 1 if nothing's been saved yet."""
        try:
            with open("userdata.txt", 'r') as file:
                lines = file.readlines()
                # Make sure there's actually something on the first line before we try to parse it
                if lines and lines[0].strip():
                    return int(lines[0].strip())
            return 1
        except (FileNotFoundError, ValueError):
            # If the file doesn't exist or the data is corrupted, just start from the beginning
            return 1

    def get_max_unlocked(self):
        """Returns the highest level number the player has ever beaten, this controls what shows up as clickable on the menu."""
        try:
            with open("userdata.txt", 'r') as file:
                lines = file.readlines()
                # The max unlocked level lives on the second line of the save file
                if len(lines) >= 2 and lines[1].strip():
                    return int(lines[1].strip())
                # Migration: if there's no second line yet, treat the current level as the baseline
                if lines and lines[0].strip():
                    return int(lines[0].strip())
            return 1
        except (FileNotFoundError, ValueError):
            # Something went wrong reading the file, so just return 1
            return 1
