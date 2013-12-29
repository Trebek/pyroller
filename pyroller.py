#===============================================================================
# PyRoller Dice Module
#-------------------------------------------------------------------------------
# Version: 0.1.0
# Updated: 28-12-2013
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
# DICE CLASS
#===============================================================================

class DiceObj(object):
    """A dice class, containing methods for constructing / manipulating 
    dice objects."""


    def __init__(self, notation=None, num=1, sides=6):
        """Dice constructor method. Defaults to d6. It will accept 
        standard dice notation (d6, 3d6, d20, etc.), as a string, 
        or you can assign the number of dice, and number of sides 
        directly, using the arguments 'num' and 'sides'."""

        self.numdice = int(num)
        self.sides = int(sides)

        self.notation = notation

        if notation is not None:
            self.parsenotat()

        self.rolls = []
        self.sums = []

        self.rolltotal = 0


    def makebag(self, dicelist):
        """Returns a 'dice bag'."""

        dicebag = {}
        count = 1
        for die in dicelist:
            for key in dicebag.keys():
                if die == key:
                    count += 1
            if count == 1:
                dicebag[die] = DiceObj(die)
            else:
                dicebag["{0}_{1}".format(die, count)] = DiceObj(die) 
        return dicebag


    def getcount(self, num):
        """Returns the count of a given roll, from self.rolls"""

        numcount = 0

        if self.numdice > 1:
            for roll in self.rolls:
                for rollnum in roll:
                    if rollnum == num:
                        numcount += 1
        else:
            for rollnum in self.rolls:
                if rollnum == num:
                    numcount += 1

        return numcount


    def getnotat(self):
        """Returns the name of the dice."""

        return self.notation


    def getrolls(self):
        """Returns the current roll(s)."""

        rolllen = len(self.rolls)
        if rolllen == 1:
            return self.rolls[0]
        elif rolllen > 1:
            return self.rolls
        else:
            return None


    def getrolltotal(self):
        """Returns the number of times the dice object has been rolled."""

        return self.rolltotal


    def getsums(self):
        """Returns the current sum(s)."""

        sumlen = len(self.sums)
        if sumlen == 0:
            self.sumrolls()
            return self.getsums()
        elif sumlen == 1:
            return self.sums[0]
        elif sumlen > 1:
            return self.sums


    def getsumavg(self, rounded=True, decplaces=2):
        """Returns the current average(s)."""

        sumlen = len(self.sums)
        sumsum = sum(self.sums)

        sumavg = float(sumsum) / sumlen

        if rounded:
            return round(sumavg, decplaces)
        else:
            return sumavg


    def getzips(self, index=None):
        """Returns the rolls and sums packaged together in tuples."""

        zipped = zip(self.rolls, self.sums)
        return zipped


    def parsenotat(self):
        """Parses di(c)e notation, separating number of dice from sides."""

        validchars = "d0123456789f"
        notatlen = len(self.notation)
        start = 0
        end = 1

        if self.notation != "coin":
            for char in self.notation:
                if char in validchars:
                    continue
                else:
                    print "Invalid notation. Defaulting to d6."
                    return
        while end < notatlen:
            if "d" in self.notation[start:end]:
                if start == 0 and end == 1:
                    self.numdice = 1
                else:
                    self.numdice = int(self.notation[start:end - 1])
                start = end + 1
            else:
                end += 1
        if self.notation[start:end] == "coin":
            self.sides = 2
        elif self.notation[start - 1:end] == "f":
            self.sides = "f"
        else:
            self.sides = int(self.notation[start - 1:end])


    def roll(self, count=1, rem=False):
        """Rolls the di(c)e once, or a specified number of times,
        and stores the roll in 'self.rolls'. Also returns the last roll."""

        rolls = []

        if not rem:
            self.rolls = []

        for i in range(count):
            roll = []
            self.rolltotal += 1 
            for i in range(self.numdice):
                if self.notation == "coin":
                    flip = random.randrange(2)
                    if flip == 0:
                        roll.append("Heads")
                    elif flip == 1:
                        roll.append("Tails")
                    else:
                        pass
                elif self.sides == "f":
                    fudge = random.randrange(3)
                    if fudge == 0:
                        roll.append("-")
                    elif fudge == 1:
                        roll.append("0")
                    elif fudge == 2:
                        roll.append("+")
                else:
                    roll.append(random.randrange(1, self.sides + 1))
            if len(roll) > 1:
                rolls.append(roll)
            else:
                rolls.append(roll[0])

        self.rolls.extend(rolls)

        return rolls[-1]


    def setnotat(self, notation=None):
        """Sets the notation of the dice, using standard dice notation.
        Can also be used to change a dice object's notation, and thus
        the dice."""

        if notation == None:
            if self.numdice > 1:
                self.notation = "{0}d{1}".format(self.numdice, self.sides)
            else:
                self.notation = "d{0}".format(self.sides)
        else:
            self.notation = notation

        self.parsenotat()


    def sumrolls(self, rem=False):
        """Sums the current roll(s), and stores the sums in 'self.sums'. 
        Also returns the last sum."""

        rollsums = []

        if not rem:
            self.sums = []

        if type(self.rolls[-1]) == list:
            for roll in self.rolls:
                rollsums.append(sum(roll))
            self.sums.extend(rollsums)
        else:
            rollsums.append(self.rolls[-1])
            self.sums = self.rolls
        
        return rollsums[-1]


    def reset(self, rolls=True, sums=True):
        """Resets the rolls, and sums to empty, and roll count to 0."""

        if rolls:
            self.rolls = []
        if sums:
            self.sums = []
        self.rolltotal = 0

#===============================================================================
# IF MAIN
#===============================================================================

if __name__ == '__main__':
    print "Please import PyRoller as a module."
