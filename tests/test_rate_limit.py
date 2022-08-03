from datetime import datetime, timedelta
from typing import Optional
from unittest import mock

from bigbuy.rate_limit import RATE_LIMIT_RESPONSE_TEXT, RateLimit


def mock_response(ok=True, headers=None, text="", status_code=None):
    if status_code is None:
        status_code = 200 if ok else 429
    return mock.Mock(ok=ok, headers=headers or {}, text=text, status_code=status_code)


def make_rate_limit_response(rate_limit_datetime):
    headers = {}
    if rate_limit_datetime is not None:
        headers["X-Ratelimit-Reset"] = str(int(rate_limit_datetime.timestamp()))
    return mock_response(ok=False, headers=headers, text=RATE_LIMIT_RESPONSE_TEXT)


def test_from_response_none():
    assert RateLimit.from_response(mock_response(ok=True, text="")) is None
    assert RateLimit.from_response(mock_response(ok=True, text=RATE_LIMIT_RESPONSE_TEXT)) is None
    assert RateLimit.from_response(mock_response(ok=False, text=RATE_LIMIT_RESPONSE_TEXT)) is None


def test_from_response():
    rl = RateLimit.from_response(make_rate_limit_response(datetime.now()))
    assert isinstance(rl, RateLimit)


def test_reset_time():
    dt = datetime.now().replace(microsecond=0)
    r = make_rate_limit_response(dt)
    rl = RateLimit.from_response(r)
    assert isinstance(rl, RateLimit)
    assert rl.reset_time == dt


def test_wait_until_expiration_past_date(utcnow):
    def dont_wait(_):
        assert False

    r = make_rate_limit_response(utcnow - timedelta(days=2))
    rl = RateLimit.from_response(r)
    assert isinstance(rl, RateLimit)
    assert rl.reset_timedelta(utcnow=utcnow) < timedelta(0)
    rl.wait_until_expiration(wait_function=dont_wait)


def test_wait_until_expiration(utcnow):
    _wait: Optional[float] = None

    def wait(seconds: float):
        nonlocal _wait
        _wait = seconds

    r = make_rate_limit_response(utcnow + timedelta(seconds=2))
    rl = RateLimit.from_response(r)
    assert isinstance(rl, RateLimit)
    assert rl.reset_timedelta() > timedelta(0)
    rl.wait_until_expiration(wait_function=wait)

    assert _wait is not None
    assert 1 < _wait < 3  # add some margin
