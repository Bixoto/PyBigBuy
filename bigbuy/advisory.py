# -*- coding: utf-8 -*-

"""
bigbuy.advisory
~~~~~~~~~~~~~~~~

This module contains Warning classes for Bigbuy to specifically
alert the user about.

This mainly is because Python 2.7 > mutes DeprecationWarning and when
we deprecate a method or variable in Bigbuy, we want to use to see
the Warning but don't want ALL DeprecationWarnings to appear,
only BigbuyDeprecationWarnings.
"""


class BigbuyDeprecationWarning(DeprecationWarning):
    """Custom DeprecationWarning to be raised when methods/variables
    are being deprecated in Bigbuy. Python 2.7 > ignores DeprecationWarning
    so we want to specifcally bubble up ONLY Bigbuy Deprecation Warnings
    """
    pass
