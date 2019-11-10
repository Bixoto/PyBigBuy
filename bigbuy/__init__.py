"""
Bigbuy
-------

Bigbuy is a library for Python that wraps the Twitter API.

It aims to abstract away all the API endpoints, so that
additions to the library and/or the Twitter API won't
cause any overall problems.

Questions, comments? ryan@venodesigns.net
"""

__author__ = 'Lugh <jbc@mozaart.com>'
__version__ = '0.0.1'

from .api import BigBuy
from .exceptions import (
    BBError
)
