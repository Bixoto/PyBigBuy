import json
import math
from datetime import datetime, timedelta
from unittest import mock

import pytest
from requests import Response

from bigbuy import exceptions as ex


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
    response._content = """HTTP/1.0 500 Internal Server Error
Cache-Control: no-cache, private
Content-Type:  application/json
Date:          Tue, 24 May 2022 15:01:07 GMT

{"error":"Information is not available right now. Try it again later"}
""".encode("utf-8")

    with pytest.raises(ex.BBServerError, match="not available right now"):
        ex.raise_for_response(response)


def make_exception(rate_limit_datetime):
    headers = {}
    if rate_limit_datetime is not None:
        headers["X-Ratelimit-Reset"] = str(int(rate_limit_datetime.timestamp()))
    response = mock.Mock(headers=headers)
    return ex.BBRateLimitError("some text", response)


def test_reset_time():
    for dt in (
            None,
            datetime(2000, 1, 2, 3, 4, 5),
            datetime(2100, 1, 2, 3, 4, 5),
    ):
        e = make_exception(dt)
        assert dt == e.reset_time


def test_bbratelimiterror_reset_timedelta():
    one_day = timedelta(days=1)
    day_2 = datetime.utcnow()
    day_1 = day_2 - one_day

    # future
    e = make_exception(day_2)
    diff = e.reset_timedelta(utcnow=day_1)
    assert isinstance(diff, timedelta)
    # avoid a rounding issue
    assert one_day.total_seconds() == math.ceil(diff.total_seconds())

    # present
    e = make_exception(day_1)
    assert e.reset_timedelta(utcnow=day_1) is None

    # past
    e = make_exception(day_1)
    assert e.reset_timedelta(utcnow=day_2) is None
