import json

import pytest
from requests import Response

from bigbuy import exceptions as ex


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


def test_raise_for_response_error_detail():
    warehouses = [
        {"id": 1, "references": ["59430878", "V0700822"]},
        {"id": 3, "references": ["S7106391"]}
    ]

    response = Response()
    response.encoding = "utf-8"
    response.status_code = 409
    payload = {
        "code": 409,
        "message": "This cart contains products from different warehouses. You must send separate requests for each set of product references to obtain the shipping costs for each set of products. You can find more info in the field \"error_detail\" in this response",
        "error_detail": {"warehouses": warehouses}
    }
    response._content = json.dumps(payload).encode("utf-8")

    with pytest.raises(ex.BBWarehouseSplitError) as exc_info:
        ex.raise_for_response(response)

    assert isinstance(exc_info.value, ex.BBWarehouseSplitError)
    assert exc_info.value.warehouses == warehouses


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


def test_raise_for_response_504_html_body():
    response = Response()
    response.status_code = 504
    response.encoding = "utf-8"
    response._content = (
        "<html><body><h1>504 Gateway Time-out</h1>\nThe server didn't respond in time.\n</body></html>"
    ).encode("utf-8")

    with pytest.raises(ex.BBTimeoutError, match=r"^The server didn't respond in time\."):
        ex.raise_for_response(response)


def test_raise_for_response_500_html_body_container_div():
    response = Response()
    response.status_code = 500
    response.encoding = "utf-8"
    response._content = """
    <html><body><div class="container"><h1>Oops! An Error Occurred</h1>
    <h2>The server returned a "500 Internal Server Error".</h2>
    <p>
        Something is broken. Please let us know what you were doing when this error occurred.
        We will fix it as soon as possible. Sorry for any inconvenience caused.
    </p>
    </div></body></html>
    """.encode("utf-8")

    with pytest.raises(ex.BBServerError, match=r"^Something is broken\."):
        ex.raise_for_response(response)