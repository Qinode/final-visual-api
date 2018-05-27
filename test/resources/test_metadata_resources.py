from falcon import testing
import pytest
from mock import MagicMock
from api import create_app

# docker run <image-name> py.test


@pytest.fixture()
def mock_metadata_store():
    return MagicMock()


@pytest.fixture()
def client(mock_metadata_store):
    return testing.TestClient(create_app(mock_metadata_store))


def test_on_post_success_empty(client, mock_metadata_store):
    mock_metadata_store.get_fields.return_value = []
    params = {"sensor_id": 'id'}
    result = client.simulate_post('/metadata/fields', json=params)

    assert result.json['data'] == []


def test_field_key_error(client):
    wrong_key = 'sensor_i'
    params = {wrong_key: 'id'}
    result = client.simulate_post('/metadata/fields', json=params)

    import falcon
    assert result.status == falcon.HTTP_422
    assert result.json['error message'] == 'KeyError: \'sensor_id\''

def test_on_post_found(client, mock_metadata_store):
    mock_metadata_store.get_fields.return_value = [{'field': 'field1', 'time': '2018-05-27T16:37:31.428136866Z', 'value': 1},
                                               {'field': 'field2', 'time': '2018-05-27T16:37:34.242221823Z', 'value': 1}
                                               ]
    params = {"sensor_id": 'id'}
    result = client.simulate_post('/metadata/fields', json=params)

    assert result.json['data'] == ['field1', 'field2']
