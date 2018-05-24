from falcon import testing
import pytest

from test import test_client

# docker run <image-name> py.test

@pytest.fixture()
def client():
    # Assume the hypothetical `myapp` package has a function called
    # `create()` to initialize and return a `falcon.API` instance.
    return testing.TestClient(test_client.create())


def test_get_message(client):
    doc = {u'message': u'Hello world!'}

    result = client.simulate_get('/data')
    assert result.json == doc
