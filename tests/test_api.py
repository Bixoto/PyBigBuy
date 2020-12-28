import unittest

from bigbuy import BigBuy, BBResponseError

KEY = 'YmU4NzU4ZTEwMWQzOTlmNzAwMWMxZmY0N2E3MGVhYzFhZTBlMzFkOTdlOGJjOTY0OTQ1MGZlYzg3NDkxZDc0ZA'


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.bb = BigBuy(app_key=KEY, mode="sandbox")

    def test_check_order(self):
        try:
            order = self.bb.check_order({})
            print(order)
        except BBResponseError as e:
            print(e.bb_code)
            print(e.text)

# curl  -H "Authorization: Bearer YmU4NzU4ZTEwMWQzOTlmNzAwMWMxZmY0N2E3MGVhYzFhZTBlMzFkOTdlOGJjOTY0OTQ1MGZlYzg3NDkxZDc0ZA" -H 'Content-type: application/json' -H 'Accept: application/json' https://api.sandbox.bigbuy.eu/rest/shipping/orders.json -d '{"order":{"delivery":{"isoCountry":"ES","postcode":"46005"},"products":[{"reference":"V1300179","quantity":1}]}}'
