# -*- coding: utf-8 -*-

"""
bigbuy.exceptions
~~~~~~~~~~~~~~~~~~

This module contains Bigbuy-specific Exception classes.
"""
from typing import Optional, Collection, Union

import ujson


class BBError(Exception):
    """Generic error class."""


class BBResponseError(BBError):
    def __init__(self, text: str,
                 response,
                 bb_code: Optional[Union[str, int]] = None,
                 bb_data: Optional[dict] = None):
        self.response = response
        self.text = text
        self.bb_code = bb_code
        self.bb_data = bb_data

        super(BBError, self).__init__(text)


class BBProductError(BBResponseError):
    def __init__(self, text, response, bb_code, bb_data):
        self.skus: Collection[str] = bb_data["skus"]
        super().__init__(text, response, bb_code, bb_data)


class BBProductNotFoundError(BBProductError):
    pass


class BBIncorrectRefError(BBProductError):
    pass


class BBStockError(BBProductError):
    pass


class BBZipcodeFormatError(BBResponseError):
    """
    bb_data: ``{"zipExample": "..."}``
    """


class BBMoneyBoxTooLowError(BBResponseError):
    """
    bb_data: ``{"moneyBoxAmount":0.00,"totalOrder":0.00}``
    """


class BBOrderTooLowError(BBResponseError):
    """
    bb_data: ``{"minimunPurchase":0.00,"totalOrder":0.00}`` (yes, that's a typo)
    """


class BBOrderAlreadyExistsError(BBResponseError):
    """
    bb_data: ``{"orderId": 123}``
    """


class BBTemporaryOrderError(BBResponseError):
    pass


class BBNoCarrierError(BBResponseError):
    pass


class BBInvalidPaymentError(BBResponseError):
    pass


class BBBankWireTooLowError(BBResponseError):
    """
    bb_data: ``{"minBankwire": 0.00}``
    """


class BBExportError(BBResponseError):
    pass


class BBPackError(BBResponseError):
    pass


class BBSSLEndpointError(BBError):
    """
    Exception raised if one uses a non-HTTPS URL for a BigBuy endpoint.
    """

    def __init__(self, endpoint):
        self.endpoint = endpoint
        super().__init__('api.bigbuy.com is restricted to SSL/TLS traffic.')


error_classes = {
    # https://api.bigbuy.eu/doc#post--rest-order-check.{_format}
    "ER001": BBProductNotFoundError,
    "ER002": BBIncorrectRefError,
    "ER003": BBStockError,
    "ER004": BBZipcodeFormatError,
    "ER005": BBMoneyBoxTooLowError,
    "ER007": BBOrderTooLowError,
    "ER008": BBOrderAlreadyExistsError,
    "ER009": BBTemporaryOrderError,
    "ER010": BBNoCarrierError,
    "ER011": BBInvalidPaymentError,
    "ER012": BBBankWireTooLowError,
    "ER013": BBExportError,
    "ER014": BBPackError,
}


def json_or_none(text) -> Optional[dict]:
    # don't even try to decode it if it doesn't look like a dict
    if text[0] != '{':
        return None

    try:
        return ujson.loads(text)
    except ValueError:
        return None


def raise_for_response(response):
    """
    Equivalent of request.Response#raise_for_status() that raises an exception based on the response's status.
    """
    if response.ok:
        return

    text = response.text
    content = json_or_none(text)

    if content is None:
        # e.g.: "You exceeded the rate limit"
        raise BBResponseError(text, response)

    content = response.json()

    # {"errors":[{"code":34,"message":"Sorry, that page does not exist"}]}
    if "errors" in content and content["errors"]:
        error = content["errors"][0]
    # {"code": "ER003", "message": "..."}
    elif "code" in content and "message" in content:
        error = content
    else:
        # safe default
        error = {"code": "?", "message": str(content)}

    bb_code = error["code"]
    message = error["message"]

    # Yes, nested JSON
    message_content = json_or_none(message)
    if message_content is None:
        raise BBResponseError(message, response, bb_code=bb_code)

    text = message_content["info"]
    bb_data = message_content.get("data", {})

    if bb_code in error_classes:
        error_class = error_classes[bb_code]
        raise error_class(text, response, bb_code, bb_data)

    raise BBResponseError(text, response, bb_code=bb_code, bb_data=bb_data)
