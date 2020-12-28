import unittest
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
