import math
import unittest
from datetime import datetime, timedelta
from unittest import mock

from bigbuy import exceptions as ex


class TestExceptions(unittest.TestCase):
    def test_flat_children_errors(self):
        self.assertDictEqual(
            {'shippingAddress.lastName': ['This value is too long.']},
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
                'carriers': []
            }))


class TestBBRateLimitError(unittest.TestCase):
    def make_exception(self, rate_limit_datetime):
        _ = self
        headers = {}
        if rate_limit_datetime is not None:
            headers["X-Ratelimit-Reset"] = str(int(rate_limit_datetime.timestamp()))
        response = mock.Mock(headers=headers)
        return ex.BBRateLimitError("some text", response)

    def test_reset_time(self):
        for dt in (
                None,
                datetime(2000, 1, 2, 3, 4, 5),
                datetime(2100, 1, 2, 3, 4, 5),
        ):
            e = self.make_exception(dt)
            self.assertEqual(dt, e.reset_time, dt)

    def test_BBRateLimitError_reset_timedelta(self):
        one_day = timedelta(days=1)
        day_2 = datetime.utcnow()
        day_1 = day_2 - one_day

        # future
        e = self.make_exception(day_2)
        diff = e.reset_timedelta(utcnow=day_1)
        self.assertIsInstance(diff, timedelta)
        # avoid a rounding issue
        self.assertEqual(one_day.total_seconds(), math.ceil(diff.total_seconds()))

        # present
        e = self.make_exception(day_1)
        self.assertIsNone(e.reset_timedelta(utcnow=day_1))

        # past
        e = self.make_exception(day_1)
        self.assertIsNone(e.reset_timedelta(utcnow=day_2))
