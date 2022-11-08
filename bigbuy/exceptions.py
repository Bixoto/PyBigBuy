# -*- coding: utf-8 -*-

"""
bigbuy.exceptions
~~~~~~~~~~~~~~~~~~

This module contains Bigbuy-specific Exception classes.
"""
import json
import re
import time
from datetime import datetime, timedelta
from typing import Optional, Union, Dict, Any, List, Type, cast, Sequence

from requests import Response

from bigbuy.rate_limit import RateLimit


class BBError(Exception):
    """Generic error class."""


class BBResponseError(BBError):
    def __init__(self, text: str,
                 response: Response,
                 bb_code: Optional[Union[str, int]] = None,
                 bb_data: Optional[Union[dict, list]] = None):
        self.response = response
        self.text = text
        self.bb_code = bb_code
        self.bb_data = bb_data

        super(BBError, self).__init__(text)


class BBRateLimitError(BBResponseError):
    def __init__(self, text: str, response: Response):
        super().__init__(text, response)
        self.rate_limit = RateLimit.from_response(response)

    # backward compatibility
    @property
    def reset_time(self):
        if self.rate_limit is not None:
            return self.rate_limit.reset_time

        return None

    # backward compatibility
    def reset_timedelta(self, utcnow: Optional[datetime] = None):
        if self.rate_limit is not None:
            dt = self.rate_limit.reset_timedelta(utcnow=utcnow)
            if dt <= timedelta(0):
                return None
            return dt

        return None

    # backward compatibility
    def wait_until_expiration(self, *, wait_function=time.sleep, additional_delay=0.01):
        if self.rate_limit is not None:
            self.rate_limit.wait_until_expiration(wait_function=wait_function)
            return True
        return None


class BBProductError(BBResponseError):
    def __init__(self, text: str, response: Response, bb_code, bb_data, *, skus: Optional[List[str]] = None):
        if skus is None:
            skus = bb_data["skus"]

        self.skus = skus
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


class BBShippingError(BBResponseError):
    pass


class BBNoCarrierError(BBShippingError):
    pass


class BBWarehouseSplitError(BBShippingError):
    def __init__(self, *args, warehouses: Sequence[dict] = (), **kwargs):
        super().__init__(*args, **kwargs)
        self.warehouses = warehouses


# Backward compatibility
BBWarehouseError = BBWarehouseSplitError


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
    def __init__(self, error_fields, response: Response, **kwargs):
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


def json_or_none(text: Optional[str]) -> Optional[dict]:
    if not text:
        return None

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


def raise_for_response(response: Response):
    """
    Equivalent of request.Response#raise_for_status() that raises an exception based on the response's status.
    This may modify its argument to fix the status code if the response is a soft error.
    """
    text = response.text
    content = json_or_none(text)

    # BigBuy may return soft errors (with a '200 OK' code)
    if response.ok:
        # BigBuy may return soft errors (with a '200 OK' code)
        if isinstance(content, dict) and set(content) - {"error_detail", } == {"code", "message"}:
            code = content["code"]
            message = content["message"]
            if isinstance(code, int) and 400 <= code < 600 and \
                    isinstance(message, str) and "Something went wrong" in message:
                response.status_code = code
                return raise_for_response(response)

        # It may also return whole HTTP responses embedded in the body of a 200 OK response
        # See test_raise_for_response_soft_error_headers_in_body for a real-world example.
        if text.startswith("HTTP/1."):
            if match := re.match(r"HTTP/1\.[01] (\d{3})", text):
                response.status_code = int(match.group(1))
                parts = text.split("\r\n\r\n", 1)
                if len(parts) == 2:
                    _headers, body = parts
                    response.encoding = "utf-8"
                    response._content = body.encode(response.encoding)
                    return raise_for_response(response)

        return

    is_5xx = response.status_code // 100 == 5

    if content is None:
        if text == "You exceeded the rate limit":
            error_class: Type[BBResponseError] = BBRateLimitError
        elif is_5xx or \
                text.startswith("<html><body><h1>504 Gateway Time-out</h1>") or \
                "Internal Server Error" in text or \
                text == "Bad Gateway":
            error_class = BBServerError
        else:
            error_class = BBResponseError

        # Trim what we can.
        if text.startswith("<html>") or text.startswith("<!DOCTYPE html>"):
            # We may want to go further:
            #   '<div class="container">
            #       <h1>Oops! An Error Occurred</h1>
            #       <h2>The server returned a "500 Internal Server Error".</h2>
            #
            #       <p>
            #           Something is broken. Please let us know what you were doing when this error occurred.
            #           We will fix it as soon as possible. Sorry for any inconvenience caused.
            #       </p>
            #   </div>'
            if m := re.match(r".+<body>(.+)</body>\s*</html>\s*", text, re.DOTALL):
                text = m.group(1).strip()

                # Trim "<h1>504 Gateway Time-out</h1>"
                if m := re.match(r"<h1>5\d\d .+?</h1>(.+)$", text, re.DOTALL):
                    text = m.group(1).strip()

        raise error_class(text, response)

    content = cast(dict, response.json())

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

    if "error_detail" in content and "different warehouses" in message:
        error_detail = content["error_detail"]
        if isinstance(error_detail, dict) and "warehouses" in error_detail:
            raise BBWarehouseSplitError(message, response, bb_code=bb_code, warehouses=error_detail["warehouses"])

    try:
        if int(bb_code) // 100 == 5:
            raise BBServerError(message, response, bb_code=bb_code)
    except ValueError:
        pass

    error_class = BBServerError if is_5xx else BBResponseError

    # Yes, nested JSON
    message_content = json_or_none(message)
    if message_content is None:
        raise error_class(message, response, bb_code=bb_code)

    text = message_content["info"]
    bb_data = message_content.get("data", {})

    if bb_code in error_classes:
        error_class = error_classes[bb_code]
        raise error_class(text, response, bb_code, bb_data)

    if not is_5xx:
        if text == "Products error." and bb_data and isinstance(bb_data, list) \
                and all(isinstance(d, dict) and "sku" in d and "message" in d
                        for d in bb_data):

            skus = [d["sku"] for d in bb_data]

            # If there's only one error message, use it to clarify the unhelpful 'Products error'.
            if len(bb_data) == 1:
                text = f"Products error: {bb_data[0]['message']}"

            raise BBProductError(text, response, bb_code, bb_data, skus=skus)

    raise error_class(text, response, bb_code=bb_code, bb_data=bb_data)


# deprecated
def wait_rate_limit(e: BBRateLimitError, wait_function=time.sleep, additional_delay=0.01):
    if not isinstance(e, BBRateLimitError):
        return False

    return e.wait_until_expiration(wait_function=wait_function, additional_delay=additional_delay)
