import json
import math
from datetime import datetime, timedelta
from typing import Optional
from unittest import mock

import pytest
from api_session import APISession
from requests import Response

from bigbuy import BigBuy, exceptions as ex
from bigbuy.rate_limit import RATE_LIMIT_RESPONSE_TEXT


def test_json_or_none():
    assert ex.json_or_none("") is None
    assert ex.json_or_none("null") is None


def test_trim_empty_collections():
    assert not ex._trim_empty_collections({
        'a': {'b': [{'c': {'d': []}}, {}, []]},
    })


def test_flat_children_errors():
    assert not ex.flat_children_errors({
        'a': {'children': [{'children': {'b': []}}]},
    })

    assert \
        {'shippingAddress.lastName': ['This value is too long.']} \
        == \
        ex.flat_children_errors({
            'internalReference': [],
            'cashOnDelivery': [],
            'language': [],
            'paymentMethod': [],
            'shippingAddress': {
                'children': {
                    'firstName': [],
                    'lastName': {
                        'errors': ['This value is too long.']},
                    'country': [],
                    'postcode': [],
                    'town': [],
                    'comment': [],
                    'vatNumber': [],
                    'companyName': []
                }
            },
            'carriers': {
                'children': [
                    {
                        'children': {'id': [], 'name': []}
                    }
                ]
            }
        })


@pytest.fixture()
def error_payload():
    return {
        "code": 400,
        "message": "ERROR: This value is not valid.\\n",
        "errors": {
            "errors": ["This value is not valid."],
            "children": {
                "internalReference": [], "cashOnDelivery": [],
                "language": [], "paymentMethod": [],
                "shippingAddress": {"children": {"firstName": [], "lastName": [],
                                                 "country": [], "postcode": [], "town": [],
                                                 "address": [], "phone": [], "email": [], "comment": [],
                                                 "vatNumber": [],
                                                 "companyName": []}},
                "carriers": [], "products": [], "dateAdd": [],
            }
        }
    }


def test_raise_for_response_products_error():
    response = Response()
    response.encoding = "utf-8"
    response.status_code = 409
    # Sentry BIXOTO-PZ
    payload = {
        "code": 409,
        "message": '{"info":"Products error.","data":[{"sku":"S5001344","message":"Inactive product."}]}'
    }
    response._content = json.dumps(payload).encode("utf-8")

    with pytest.raises(ex.BBProductError, match="Products error:"):
        ex.raise_for_response(response)


def test_raise_for_response_invalid_value_error(error_payload):
    response = Response()
    response.encoding = "utf-8"
    response._content = json.dumps(error_payload).encode("utf-8")
    response.status_code = 400

    with pytest.raises(ex.BBValidationError):
        ex.raise_for_response(response)


def test_raise_for_response_too_long_value_error(error_payload):
    response = Response()
    response.encoding = "utf-8"
    error_payload["message"] = ("shippingAddress:\\n    address:\\n        ERROR: This value is too long."
                                " It should have 70 characters or less.\\n")
    error_payload["errors"]["children"]["shippingAddress"]["children"]["address"] = \
        {"errors": ["This value is too long. It should have 70 characters or less."]}

    response._content = json.dumps(error_payload).encode("utf-8")
    response.status_code = 400

    with pytest.raises(ex.BBValidationError):
        ex.raise_for_response(response)


def test_raise_for_response_soft_409():
    response = Response()
    response.status_code = 200
    response.encoding = "utf-8"
    payload = {'code': 409, 'message': 'Something went wrong 56783360c34fff84fe56880fbf62179b'}
    response._content = json.dumps(payload).encode("utf-8")

    with pytest.raises(ex.BBResponseError, match="Something went wrong"):
        ex.raise_for_response(response)


def test_raise_for_response_soft_error_headers_in_body():
    """
    This test reproduces this real-world error we got on 2022/05/24:

        $ curl -iH 'Authorization: Bearer OWZ...Nw' \
            https://api.bigbuy.eu/rest/shipping/lowest-shipping-costs-by-country/ES

        HTTP/2 200
        ...
        content-length: 221

        HTTP/1.0 500 Internal Server Error
        Cache-Control: no-cache, private
        Content-Type:  application/json
        Date:          Tue, 24 May 2022 15:01:07 GMT

        {"error":"Information is not available right now. Try it again later"}

    Note how this is a 200 response but whose body contains headers for a 500 error.
    """

    response = Response()
    response.status_code = 200
    response.encoding = "utf-8"
    response._content = (
        'HTTP/1.0 500 Internal Server Error\r\nCache-Control: no-cache, private\r\nContent-Type:  application/json\r\n'
        'Date:          Tue, 24 May 2022 15:41:45 GMT\r\n\r\n{"error":"Information is not available right now. Try it '
        'again later"}'
    ).encode("utf-8")

    with pytest.raises(ex.BBServerError, match="not available right now"):
        ex.raise_for_response(response)


def test_raise_for_response_500_html_body():
    # Unfortunately Sentry truncated the body so we don't know it
    # https://sentry.io/organizations/bixoto/issues/3390287708/
    response = Response()
    response.status_code = 500
    response.encoding = "utf-8"
    response._content = (
        '<!DOCTYPE html>\n<html>\n<head>\n    <meta charset="UTF-8" />\n    <meta name="robots" content="noindex,'
        'nofollow,noarchive" />\n    <title>An Error Occurred: Internal Server Error</title>\n    <style>body { '
        'background-color: #fff; color: #222; font: 16px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, '
        '"Helvetica Neue", Arial, sans-serif; margin: 0; }\n.container { margin: 30px; max-width: 600px; }\nh1 { color:'
        ' #dc3545; font-size: 24px; }\nh2 { font-size: 18px; }</style>\n</head>\n<body>\n<div>...</div>\n</body></html>'
    ).encode("utf-8")

    with pytest.raises(ex.BBServerError, match="^<div>"):
        ex.raise_for_response(response)


def make_rate_limit_response(rate_limit_datetime):
    headers = {}
    if rate_limit_datetime is not None:
        headers["X-Ratelimit-Reset"] = str(int(rate_limit_datetime.timestamp()))
    response = mock.Mock(ok=False, headers=headers, text=RATE_LIMIT_RESPONSE_TEXT)
    return response


def make_rate_limit_exception(rate_limit_datetime):
    response = make_rate_limit_response(rate_limit_datetime)
    return ex.BBRateLimitError(response.text, response)


def test_reset_time():
    e = make_rate_limit_exception(None)
    assert e.rate_limit is None

    for dt in (
            datetime(2000, 1, 2, 3, 4, 5),
            datetime(2100, 1, 2, 3, 4, 5),
    ):
        e = make_rate_limit_exception(dt)
        assert e.rate_limit is not None
        assert dt == e.reset_time


def test_bbratelimiterror_no_header():
    e = ex.BBRateLimitError("some text", mock.Mock(text=RATE_LIMIT_RESPONSE_TEXT, ok=False, headers={}))
    assert e.reset_time is None
    assert e.reset_timedelta() is None


def test_bbratelimiterror_reset_timedelta():
    one_day = timedelta(days=1)
    day_2 = datetime.utcnow()
    day_1 = day_2 - one_day

    # future
    e = make_rate_limit_exception(day_2)
    diff = e.reset_timedelta(utcnow=day_1)
    assert isinstance(diff, timedelta)
    # avoid a rounding issue
    assert one_day.total_seconds() == math.ceil(diff.total_seconds())

    # present
    e = make_rate_limit_exception(day_1)
    assert e.reset_timedelta(utcnow=day_1) is None

    # past
    e = make_rate_limit_exception(day_1)
    assert e.reset_timedelta(utcnow=day_2) is None


def test_wait_until_expiration_past_date():
    def dont_wait(_):
        assert False

    e = make_rate_limit_exception(datetime.utcnow() - timedelta(days=2))
    assert e.reset_timedelta() is None
    assert e.wait_until_expiration(wait_function=dont_wait) is False


def test_wait_until_expiration():
    _wait: Optional[float] = None

    def wait(seconds: float):
        nonlocal _wait
        _wait = seconds

    e = make_rate_limit_exception(datetime.utcnow() + timedelta(seconds=100))

    t = e.reset_timedelta()
    assert t is not None
    # Allow some margin
    assert 90 < t.seconds < 110
    assert e.wait_until_expiration(wait_function=wait) is True
    assert _wait is not None
    assert 90 < _wait < 110
