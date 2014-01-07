#===============================================================================
# PyRoller Dice Module
#-------------------------------------------------------------------------------
# Version: 1.0.1
# Updated: 06-01-2014
# Author: Alex Crawford
# License: MIT
#===============================================================================

"""
A module containing a class for creating dice instances, containing methods 
for manipulating the dice instances (roll, sum). Can also simulate coin 
tosses, and Fudge dice.

"""

#===============================================================================
# IMPORTS
#===============================================================================

import random

#===============================================================================
# PYROLLER CLASS
#===============================================================================

class Pyroller(object):
    """
    A dice class, containing methods for constructing / manipulating 
    dice objects.

    """
    def __init__(self, notation=None, num=1, sides=6):
        """
        Dice constructor method. Defaults to d6. It will accept 
        standard dice notation (d6, 3d6, d20, etc.), as a string, 
        or you can assign the number of dice, and number of sides 
        directly, using the arguments 'num' and 'sides'.

        """
        self.dice_count = int(num)
        self.dice_sides = int(sides)

        self.notation = notation

        if notation is not None:
            self.parse_notat()

        self.rolls = []
        self.sums = []

        self.roll_total = 0

    def make_bag(self, dicelist):
        """
        Takes a list of dice notations, and returns a 'dice bag',
        containing dice objects with those notations.

        """
        dice_bag = {}
        dupe_count = 1

        for die in dicelist:
            for key in dice_bag.keys():
                if die == key:
                    dupe_count += 1
            if dupe_count == 1:
                dice_bag[die] = Pyroller(die)
            else:
                dice_bag["{0}_{1}".format(die, dupe_count)] = Pyroller(die) 
        return dice_bag

    def get_num_count(self, num):
        """
        Returns the number of ocurrences of a given number, 
        in 'self.rolls'
        """
        num_count = 0

        if self.dice_count > 1:
            for roll in self.rolls:
                for roll_num in roll:
                    if roll_num == num:
                        num_count += 1
        else:
            for roll_num in self.rolls:
                if roll_num == num:
                    num_count += 1

        return num_count

    def get_notat(self):
        """Returns the notation of the dice."""

        return self.notation

    def get_rolls(self, start=0, end=0):
        """
        Returns a list of the current rolls, or a slice from the
        list of rolls, or a single roll from the list, depending on
        the arguments used.

        """
        roll_len = len(self.rolls)

        if roll_len == 1:
            return self.rolls[0]
        elif roll_len > 1:
            if start == 0 and end == 0:
                return self.rolls
            elif start > 0 and end == 0:
                return self.rolls[start]
            else:
                return self.rolls[start:end]
        else:
            return None

    def get_roll_total(self):
        """
        Returns the total number of times the dice object 
        has been rolled.

        """
        return self.roll_total

    def get_rolls_sums(self):
        """Returns the rolls and sums packaged together in tuples."""

        zipped = zip(self.rolls, self.sums)
        return zipped

    def get_sums(self, start=0, end=0):
        """Returns the current sum(s)."""

        sum_len = len(self.sums)

        if sum_len == 0:
            self.sum_rolls()
            return self.get_sums(start, end)
        elif sum_len == 1:
            return self.sums[0]
        elif sum_len > 1:
            if start == 0 and end == 0:
                return self.sums
            elif start > 0 and end == 0:
                return self.sums[start]
            else:
                return self.sums[start:end]
        else:
            return None

    def get_sum_avg(self, rounded=True, places=2):
        """Returns the current average(s)."""

        sum_len = len(self.sums)
        sums_sum = sum(self.sums)

        sum_avg = float(sums_sum) / sum_len

        if rounded:
            return round(sum_avg, places)
        else:
            return sum_avg

    def get_tosses(self, start=0, end=0):
        """Just a wrapper for the 'get_rolls' method."""
        return self.get_rolls(start, end)

    def parse_notat(self):
        """Parses di(c)e notation, separating number of dice from sides."""

        valid_chars = "df0123456789"
        notat_len = len(self.notation)
        start = 0
        end = 1

        if self.notation != "coin":
            for char in self.notation:
                if char in valid_chars:
                    continue
                else:
                    print "Invalid notation. Defaulting to d6."
                    return
        while end < notat_len:
            if "d" in self.notation[start:end]:
                if start == 0 and end == 1:
                    self.dice_count = 1
                else:
                    self.dice_count = int(self.notation[start:end - 1])
                start = end + 1
            else:
                end += 1
        if self.notation[start:end] == "coin":
            self.dice_sides = 2
        elif self.notation[start - 1:end] == "f":
            self.dice_sides = "f"
        else:
            self.dice_sides = int(self.notation[start - 1:end])

    def reset(self, rolls=True, sums=True):
        """Resets the rolls, and sums to empty, and roll count to 0."""

        if rolls:
            self.rolls = []
        if sums:
            self.sums = []
        self.roll_total = 0

    def roll(self, count=1, rem=False):
        """
        Rolls the di(c)e once, or a specified number of times,
        and stores the roll in 'self.rolls'. Also returns the last roll.

        """
        rolls = []

        if not rem:
            self.rolls = []

        for i in range(count):
            roll = []
            self.roll_total += 1 
            for i in range(self.dice_count):
                if self.notation == "coin":
                    flip = random.randrange(2)
                    if flip == 0:
                        roll.append("Heads")
                    elif flip == 1:
                        roll.append("Tails")
                    else:
                        pass
                elif self.dice_sides == "f":
                    fudge = random.randrange(3)
                    if fudge == 0:
                        roll.append("-")
                    elif fudge == 1:
                        roll.append("0")
                    elif fudge == 2:
                        roll.append("+")
                else:
                    roll.append(random.randrange(1, self.dice_sides + 1))
            if len(roll) > 1:
                rolls.append(roll)
            else:
                rolls.append(roll[0])

        self.rolls.extend(rolls)

        return rolls[-1]

    def set_notat(self, notation=None):
        """
        Sets the notation of a pyroller object, using standard dice 
        notation. Can be used to change a dice object's notation at any 
        time, and thus the dice it represents.

        """
        if notation == None:
            if self.dice_count > 1:
                self.notation = "{0}d{1}".format(
                        self.dice_count, 
                        self.dice_sides
                        )
            else:
                self.notation = "d{0}".format(self.dice_sides)
        else:
            self.notation = notation

        self.parse_notat()

    def sum_rolls(self, rem=False):
        """
        Sums the current roll(s), and stores the sums in 'self.sums'. 
        Also returns the last sum.

        """
        roll_sums = []

        if not rem:
            self.sums = []

        if type(self.rolls[-1]) == list:
            for roll in self.rolls:
                roll_sums.append(sum(roll))
            self.sums.extend(roll_sums)
        else:
            roll_sums.append(self.rolls[-1])
            self.sums = self.rolls
        
        return roll_sums[-1]

    def toss(self, count=1, rem=False):
        """Just a wrapper for the 'roll' method."""
        return self.roll(count, rem)

#===============================================================================
# IF __NAME__ == '__MAIN__'
#===============================================================================

if __name__ == '__main__':
    print "Please import PyRoller as a module."
