from bigbuy import BigBuy


def test_init_defaults(app_key):
    bb = BigBuy(app_key)
    assert bb.none_on_404 is False
    assert bb.none_on_empty is True
    assert bb.retry_on_rate_limit is False
    assert bb.base_url == "https://api.sandbox.bigbuy.eu/rest"


def test_init_production(app_key):
    bb = BigBuy(app_key, mode="production")
    assert bb.base_url == "https://api.bigbuy.eu/rest"


def test_repr(app_key):
    bb = BigBuy(app_key)
    assert repr(bb) == f"<Bigbuy key={app_key[:10]}…>"
