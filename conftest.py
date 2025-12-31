from datetime import datetime

import pytest


@pytest.fixture
def utcnow() -> datetime:
    return datetime.utcnow()


@pytest.fixture
def app_key() -> str:
    return "top_secret_app_key"
