import math
from datetime import datetime, timedelta
from unittest import mock

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
