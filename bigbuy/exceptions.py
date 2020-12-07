# -*- coding: utf-8 -*-

"""
bigbuy.exceptions
~~~~~~~~~~~~~~~~~~

This module contains Bigbuy specific Exception classes.
"""

from .endpoints import HTTP_STATUS_CODE
import ujson


class BBError(Exception):
    """Generic error class, catch-all for most BigBuy issues.

    from bigbuy import BigBuyError

    """

    def __init__(self, msg, error_code=None, retry_after=None, post_mortem=None):
        self.error_code = error_code
        self.post_mortem = post_mortem
        self.BBCode = None
        self.BBMessage = None
        self.msg = msg
        if post_mortem["content"]:
            data = ujson.loads(post_mortem["content"])
            self.BBCode = data["code"]
            self.BBMessage = data["message"]

        if error_code is not None and error_code in HTTP_STATUS_CODE:
            msg = 'BiguBuy API returned a %s (%s), %s' % \
                  (error_code,
                   HTTP_STATUS_CODE[error_code][0],
                   msg)
            print(msg)

        super(BBError, self).__init__(msg)
