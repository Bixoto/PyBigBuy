from datetime import datetime

import pytest


@pytest.fixture
def utcnow():
    return datetime.utcnow()


@pytest.fixture
def app_key():
    return "top_secret_app_key"
