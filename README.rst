======================
PyRoller: Dice Package
======================

A relatively simple package containing a class & methods for simulating dice. Can also simulate coin tosses, and Fudge dice as well.

Install/Uninstall with PIP_
===========================

Install
-------
::

    pip install https://github.com/Trebek/pyroller/archive/master.zip

Uninstall
---------
::

    pip uninstall pyroller

Basic Usage
===========

Create & Roll a Die Object
--------------------------
::

    import pyroller

    d6 = pyroller.Pyroller("d6")

    result = d6.roll()

    print result

**Example output:**
::

    5

Create a "Bag" of Dice & Roll Them
----------------------------------
::

    from pyroller import Pyroller

    notations = ["d6", "3d6", "d20", "4dF", "coin"]

    bag = Pyroller.build_bag(notations)

    for key in bag:
        roll_str = str(bag[key].roll())
        print "%s = %s" % (key, roll_str)

**Example output:**
::

    d6 = 4
    d20 = 9
    3d6 = [4, 2, 5]
    coin = Tails
    4dF = [' ', ' ', '+', '-']

Relevant Links
============== 

| `Dice notation article on Wikipedia <http://en.wikipedia.org/wiki/Dice_notation>`_
| `Fudge dice information on Wikipedia <http://en.wikipedia.org/wiki/Fudge_%28role-playing_game_system%29#Fudge_dice>`_

.. _PIP: https://pypi.python.org/pypi/pip/