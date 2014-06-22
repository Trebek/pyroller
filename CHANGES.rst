==================
PyRoller Changelog
==================

v1.1.0 (22-06-2014)
------------------

- Pyroller is now a proper installable package (at least when using PIP).
- Changed a number of methods & method names.
    - Changed ``Pyroller.make_bag`` to ``Pyroller.build_bag``, and you no longer have to call ``build_bag`` with an instance of ``Pyroller``, as it's a class method.
    - Did away with all of the ``Pyroller.get_<name>`` methods. Replaced a lot of them with class properties.
        - ``Pyroller.get_num_count`` is now ``Pyroller.count``.
        - ``Pyroller.get_notat`` is now the property ``Pyroller.notation``.
        - ``Pyroller.get_rolls`` is now the property ``Pyroller.roll_list``.
        - ``Pyroller.get_rolls_sums`` is now the property ``Pyroller.rolls_sums``.
        - ``Pyroller.get_sums`` is now the property ``Pyroller.sums``.
        - ``Pyroller.get_sum_avg`` is now ``Pyroller.sum_avg``.
        - ``Pyroller.get_tosses`` is now the property ``Pyroller.toss_list``.
- Fixed up & filled out the documentation a bit.

v1.0.0 (06-01-2014)
------------------

- Initial release.