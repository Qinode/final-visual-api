from falcon import testing
import pytest
from test.api import test_client

# docker run <image-name> py.test


@pytest.fixture()
def client():
    # Assume the hypothetical `myapp` package has a function called
    # `create()` to initialize and return a `falcon.API` instance.
    return testing.TestClient(test_client.create())


def test_on_post_success_empty(client):
    params = {"sensor_id": 1, "field": "field1", "timestamp": '2018-01-01T00:00:00Z'}
    result = client.simulate_post('/data', json=params)
    assert result.json['data'] == []
