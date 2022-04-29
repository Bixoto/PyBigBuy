# -*- coding: utf-8 -*-

"""
bigbuy.exceptions
~~~~~~~~~~~~~~~~~~

This module contains Bigbuy-specific Exception classes.
"""
from datetime import datetime, timedelta
from typing import Optional, Collection, Union, Dict, Any, List

import json


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


class BBRateLimitError(BBResponseError):
    def __init__(self, text: str, response):
        super().__init__(text, response)
        self.reset_time: Optional[datetime] = None
        reset_timestamp: str = response.headers.get("X-Ratelimit-Reset", "")
        if reset_timestamp and reset_timestamp.isdigit():
            self.reset_time = datetime.fromtimestamp(int(reset_timestamp))

    def reset_timedelta(self, utcnow: Optional[datetime] = None):
        """
        Return a timedelta object representing the delta between the current time and the reset time.
        Return None if it would be negative (i.e. the rest time is in the past).

        :param utcnow: if passed, this is used instead of datetime.utcnow()
        """
        if not self.reset_time:
            return

        if utcnow is None:
            utcnow = datetime.utcnow()

        delta = self.reset_time - utcnow
        if delta <= timedelta(0):
            return

        return delta


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


class BBServerError(BBResponseError):
    pass


class BBValidationError(BBResponseError):
    def __init__(self, error_fields, response, **kwargs):
        text = "Validation failed: %s" % str(error_fields)
        super().__init__(text, response, **kwargs)
        self.error_fields = error_fields


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
        return json.loads(text)
    except ValueError:
        return None


def _trim_empty_collections(obj: Any):
    """
    Given a dict or list whose children are only dicts or lists with either truthy values or empty collections, remove
    the latter. This is an internal utility.
    """
    if isinstance(obj, list):
        trimmed_elements = (_trim_empty_collections(el) for el in obj)
        return [el for el in trimmed_elements if el]

    if isinstance(obj, dict):
        d = {}
        for k, v in obj.items():
            trimmed_value = _trim_empty_collections(v)
            if not trimmed_value:
                continue

            d[k] = trimmed_value

        return d

    return obj


def flat_children_errors(children: Union[List, Dict[str, Any]], prefix=""):
    """
    Simplify children errors:

    Before:
      {'internalReference': [], 'cashOnDelivery': [], 'language': [],
       'shippingAddress': {'children': {'firstName': [], 'lastName': {'errors': ['This value is too long.']}}}

    After:
      {'shippingAddress.lastName': ['This value is too long.']}
    """
    children = _trim_empty_collections(children)

    if isinstance(children, list):
        return children

    trimmed = {}

    for field, value in children.items():
        if prefix:
            field = f"{prefix}.{field}"

        if isinstance(value, dict) and len(value) == 1:
            if "errors" in value:
                trimmed[field] = value["errors"]
            elif "children" in value:
                flattened = flat_children_errors(value["children"], prefix=field)
                if isinstance(flattened, dict):
                    trimmed.update(flattened)
                else:
                    trimmed[field] = value
            else:
                trimmed[field] = value
        else:
            trimmed[field] = value

    return trimmed


def raise_for_response(response):
    """
    Equivalent of request.Response#raise_for_status() that raises an exception based on the response's status.
    """
    if response.ok:
        return

    text = response.text
    content = json_or_none(text)

    if content is None:
        if text == "You exceeded the rate limit":
            cls = BBRateLimitError
        elif text.startswith("<html><body><h1>504 Gateway Time-out</h1>") or \
                text in {"Bad Gateway", "Internal Server Error"}:
            cls = BBServerError
        else:
            cls = BBResponseError

        raise cls(text, response)

    content = response.json()

    bb_code = "unknown"
    message = str(content)

    # {"errors":[{"code":34,"message":"Sorry, that page does not exist"}]}
    if "errors" in content and content["errors"]:
        errors = content["errors"]

        if errors:
            if isinstance(errors, dict) and "code" in content and "message" in content:
                # {"code":400,"message":"Validation Failed",
                #  "errors":{"children":{"delivery":{"children":{"postcode":{"errors":["Invalid postcode format..."]}}},
                #                        "products":{...}}}}
                if "children" in errors:
                    errors_message = flat_children_errors(errors["children"])

                    if content["message"].strip() == "Validation Failed" or "ERROR:" in content["message"]:
                        raise BBValidationError(
                            # {'delivery.postcode': [
                            #     "Invalid postcode format. Valid format for the selected country is 'NNNNN'.",
                            #     'This value is not valid.']}
                            error_fields=errors_message,
                            response=response,
                            bb_code=bb_code,
                        )
                else:
                    errors_message = str(errors)

                bb_code = str(content["code"])
                message = "%s: %s" % (content["message"], errors_message)
            else:
                error = errors[0]
                if "code" in error:
                    bb_code = error["code"]
                message = error.get("message", message)

    # {"code": "ER003", "message": "..."}
    elif "code" in content and "message" in content:
        bb_code = content["code"]
        message = content["message"]

    try:
        if int(bb_code) // 100 == 5:
            raise BBServerError(message, response, bb_code=bb_code)
    except ValueError:
        pass

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
