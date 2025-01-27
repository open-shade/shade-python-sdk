import pytest

from shade import Shade

# ToDo - do something better w this once we add it to GH actions
API_KEY = 'sk_965a8a31cbf49c8ecc842082d40d5fa8cc529aa78a217788536cbeff5cf56ab3'
REMOTE_URL = 'http://127.0.0.1:9082'


@pytest.fixture
def shade():
    return Shade(remote_url=REMOTE_URL, api_key=API_KEY)
