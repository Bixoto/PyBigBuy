# -*- coding: utf-8 -*-

"""
bigbuy.exceptions
~~~~~~~~~~~~~~~~~~

This module contains Bigbuy specific Exception classes.
"""

from .endpoints import HTTP_STATUS_CODE


class BBError(Exception):
    """Generic error class, catch-all for most BigBuy issues.

    from bigbuy import BigBuyError

    """
    def __init__(self, msg, error_code=None, retry_after=None):
        self.error_code = error_code

        if error_code is not None and error_code in HTTP_STATUS_CODE:
            msg = 'BiguBuy API returned a %s (%s), %s' % \
                  (error_code,
                   HTTP_STATUS_CODE[error_code][0],
                   msg)

        super(BBError, self).__init__(msg)

    @property
    def msg(self):  # pragma: no cover
        return self.args[0]
