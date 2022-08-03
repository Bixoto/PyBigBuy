from datetime import datetime

import pytest
import responses
from responses.registries import OrderedRegistry

from bigbuy import BigBuy, BBRateLimitError
from bigbuy.rate_limit import RATE_LIMIT_RESPONSE_TEXT


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


@responses.activate
def test_get_json_api(app_key):
    bb = BigBuy(app_key)
    payload = {"test": "ok"}

    responses.add(
        responses.GET,
        bb.base_url + "/toto.json",
        json=payload,
    )

    assert bb.get_json_api("toto") == payload


@responses.activate()
def test_get_json_api_rate_limit_no_retry(app_key):
    bb = BigBuy(app_key)

    responses.add(
        responses.GET,
        bb.base_url + "/toto.json",
        body=RATE_LIMIT_RESPONSE_TEXT,
        status=429,
        headers={
            "X-Ratelimit-Reset": str(int(datetime.utcnow().timestamp()))
        }
    )

    with pytest.raises(BBRateLimitError):
        bb.get_json_api("toto")


@responses.activate(registry=OrderedRegistry)
def test_get_json_api_auto_retry_once(app_key):
    bb = BigBuy(app_key, retry_on_rate_limit=True)
    payload = {"test": "ok"}

    responses.add(
        responses.GET,
        bb.base_url + "/toto.json",
        body=RATE_LIMIT_RESPONSE_TEXT,
        status=429,
        headers={
            "X-Ratelimit-Reset": str(int(datetime.utcnow().timestamp()))
        }
    )

    responses.add(
        responses.GET,
        bb.base_url + "/toto.json",
        json=payload,
    )

    assert bb.get_json_api("toto") == payload
