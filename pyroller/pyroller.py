#===============================================================================
# PyRoller: Dice Package
#-------------------------------------------------------------------------------
# Version: 1.1.0
# Updated: 22-06-2014
# Author: Alex Crawford
# License: MIT
#===============================================================================

"""
A package containing a class & methods for simulating dice. Can also simulate 
coin tosses, and Fudge dice.

"""

# The MIT License (MIT)

# Copyright (c) 2014 Alex Crawford

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

#===============================================================================
# Imports
#===============================================================================

import random
import re

#===============================================================================
# Pyroller Class
#===============================================================================

class Pyroller(object):
    """
    A dice class, containing methods for constructing / manipulating 
    dice objects.

    """
    COIN_HASH = {0: "Heads", 1: "Tails"}
    FUDGE_HASH = {0: "-", 1: "-", 2: " ", 3: " ", 4: "+", 5: "+"}

    def __init__(self, notation=None, num=1, sides=6):
        """
        Dice constructor method. Defaults to d6. It will accept 
        standard dice notation (d6, 3d6, d20, etc.), as a string, 
        or you can assign the number of dice, and number of sides 
        directly, using the arguments 'num' and 'sides'.

        :param notation: A standard dice notation.
        :param num: For specifying number of dice directly.
        :param num: For specifying number of sides directly.

        """
        self._dice_count = int(num)
        self._dice_sides = int(sides)        
        self._dice_type = None
        self._memory = False
        self._notation = None
        self._roll_total = 0
        self._rolls = []
        self._sums = []       

        self.parse_notat(notation)

    @classmethod
    def build_bag(self, notations):
        """
        Takes a list of dice notations, and builds a dictionary of dice 
        instances, using the notations in the list. The key for each 
        instance is the same as it's notation. If two keys(notations) are 
        the same, then "_x" is added to the end of the key, where 'x' is 
        the number of instances in the dictionary with that notation.

        Duplicate example:
        ["d6","d6","d6"] -> dict["d6"], dict["d6_2"], dict["d6_3"]

        :param notations: A list of dice notations.

        :returns: A dict of dice objects.

        """
        dice_bag = {}

        for die in notations:
            dice_count = 1
            for key in dice_bag.keys():
                dupe_name = "{0}_{1}".format(die, dice_count)
                if die == key or dupe_name == key:
                    dice_count += 1
            if dice_count == 1:
                dice_bag[die] = Pyroller(die)
            else:
                new_name = "{0}_{1}".format(die, dice_count)
                dice_bag[new_name] = Pyroller(die)

        return dice_bag

    def count(self, num):
        """
        Counts the number of ocurrences of a given number, fudge side ("+", 
        "-", or " "), or coin side ("heads", or "tails") in 'self._rolls'.

        :param num: A number/fudge side to count the ocurrences of.

        :returns: The number of ocurrences of a given number, 
            in 'self._rolls'

        """
        num_count = 0

        if self._dice_count > 1:
            for roll_list in self._rolls:
                num_count += roll_list.count(num)
        else:
            num_count += self._rolls.count(num)

        return num_count

    @property
    def memory(self):
        """:returns: The state of the dice objects memory (True or False)"""

        return self._memory

    def memory_toggle(self):
        """
        Toggles the memory on (True) or off (False), depending on
        `self._memory`'s current state.

        """
        self._memory = not self._memory

    @property
    def notation(self):
        """:returns: The notation of the dice object."""

        return self._notation

    def parse_notat(self, notation=None):
        """
        Parses/checks for valid di(c)e notation, in 'self._notation',
        and sets '_dice_count' and '_dice_sides' to their  respective 
        values, based on the notation, and then calls `set_notat` to 
        set the dice objects notation.

        :param notation: A dice notation.

        """
        if notation:

            pattern = re.compile(r"^([0-9]*)d([0-9]*|[fF])$|^(coin)$")
            matches = pattern.match(notation)

            if matches:
                if matches.group(1):
                    self._dice_count = int(matches.group(1))
                else:
                     self._dice_count = 1
                if matches.group(2):
                    if matches.group(2) in ["f", "F"]:
                        self._dice_type = "fudge"
                        self._dice_sides = 6
                    else:
                        self._dice_type = "standard"
                        self._dice_sides = int(matches.group(2))
                elif matches.group(3) == "coin":
                    self._dice_type = "coin"
                    self._dice_sides = 2
                else: 
                    self._dice_sides = 6
            else:
                raise ValueError("Invalid dice notation")

        self.set_notat()

    def reset(self, rolls=True, sums=True, total=True):
        """
        Resets 'self._rolls', 'self._sums', and 'self._roll_total'.

        :param rolls: Whether or not to reset ``self._rolls``.
        :param sums: Whether or not to reset ``self._sums``.
        :param total: Whether or not to reset ``self._roll_total``.

        """
        if rolls:
            self._rolls = []
        if sums:
            self._sums = []
        if total:
            self._roll_total = 0

    def roll(self, count=1):
        """
        Rolls the dice (or flips a coin). 

        :param count: The number of times to roll.

        :returns: The last roll.

        """
        roll_count_range = range(count)
        dice_count_range = range(self._dice_count)

        rolls = []

        if not self._memory:
            self._rolls = []

        for i in roll_count_range:
            roll = []
            self._roll_total += 1 
            for i in dice_count_range:
                if self._dice_type == "coin":
                    rand_num = random.randrange(self._dice_sides)
                    roll.append(self.COIN_HASH[rand_num])
                elif self._dice_type == "fudge":
                    rand_num = random.randrange(self._dice_sides)
                    roll.append(self.FUDGE_HASH[rand_num])
                else:
                    roll.append(random.randrange(1, self._dice_sides + 1))
            if len(roll) > 1:
                rolls.append(roll)
            else:
                rolls.append(roll[0])

        self._rolls.extend(rolls)

        return rolls[-1]

    @property
    def roll_list(self):
        """
        Returns a list of all of the past rolls. Must toggle memory to 
        ``True``, using the ``memory_toggle`` method first, before the 
        dice object will remember past rolls. Can turn it off by calling
        ``memory_toggle`` again, and vice versa.

        :returns: A list of all of the past rolls.

        """
        roll_len = len(self._rolls)

        if roll_len == 1:
            return self._rolls[0]
        elif roll_len > 1:
            return self._rolls
        else:
            return None

    @property
    def rolls_sums(self):
        """
        Packages the rolls and their sums together into tuples.

        :returns: The rolls and sums packaged together in tuples.

        """
        zipped = zip(self._rolls, self._sums)
        return zipped

    def set_notat(self, notation=None):
        """Sets ``self._notation`` to a given notation."""

        if not notation:
            if self._dice_count > 1:
                if self._dice_type != "fudge":
                    self._notation = "{0}d{1}".format(
                            self._dice_count, 
                            self._dice_sides
                            )
                else:
                    self._notation = "{0}dF".format(self._dice_count)
            else:
                if self._dice_type != "coin":
                    self._notation = "d{0}".format(self._dice_sides)
                else:
                    self._notation = "coin".format(self._dice_sides)
        else:
            self._notation = None

    def sum_avg(self, rounded=True, places=2):
        """
        Figures the average of the sums in ``self._sums``.

        :param rounded: Whether to round off the result.
        :param places: The number of decimal places to round to.

        :returns: The average of the currently summed rolls.

        """
        self.sum_rolls()

        sum_len = len(self._sums)
        sums_sum = sum(self._sums)

        sum_avg = float(sums_sum) / sum_len

        if rounded:
            return round(sum_avg, places)
        else:
            return sum_avg

    def sum_rolls(self):
        """
        Sums the current roll(s), and stores the sums in 'self.sums'. 
        Also returns the last sum.

        :returns: The last sum.

        """
        roll_sums = []

        if not self._memory:
            self._sums = []

        if self._dice_type != "coin" and self._dice_type != "fudge":
            if self._dice_count > 1:
                for roll_list in self._rolls:
                    roll_sums.append(sum(roll_list))
                self._sums = roll_sums
            else:
                roll_sums.append(self._rolls[-1])
                self._sums = self._rolls
        elif self._dice_type == "fudge":
            if self._dice_count > 1:
                for roll_list in self._rolls:
                    count = 0
                    for roll in roll_list:
                        if roll == "+":
                            count += 1
                        elif roll == "-":
                            count -= 1
                    roll_sums.append(count)
                self._sums = roll_sums
        else:
            return None
        
        return roll_sums[-1]

    @property
    def sums(self):
        """
        Calls ``self.sum_rolls`` to sum the rolls in ``self._rolls``.

        :returns: The current sum(s).

        """
        self.sum_rolls()
        return self._sums

    def toss(self, count=1):
        """
        Just a wrapper for the 'roll' method.

        :param count: The number of times to toss the coin.

        :returns: The result of the "toss".

        """
        return self.roll(count)

    @property
    def toss_list(self):
        """
        Just a wrapper for the `roll_list` method.

        :returns: A list of all of the past "tosses".

        """
        return self.roll_list

    @property
    def total_rolls(self):
        """
        Returns the total number of times the dice object has 
        been rolled, since it's construction/last reset.

        :returns: The total number of times the dice object has 
            been rolled

        """
        return self._roll_total

#===============================================================================
# Main Check
#===============================================================================

if __name__ == '__main__':
    pass
