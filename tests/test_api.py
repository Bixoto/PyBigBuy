from bigbuy import BigBuy

KEY = 'YmU4NzU4ZTEwMWQzOTlmNzAwMWMxZmY0N2E3MGVhYzFhZTBlMzFkOTdlOGJjOTY0OTQ1MGZlYzg3NDkxZDc0ZA'


def test_check_order():
    bb = BigBuy(app_key=KEY, mode="sandbox")
    assert bb.check_order({}) is not None
