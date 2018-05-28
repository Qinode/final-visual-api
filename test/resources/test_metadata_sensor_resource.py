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
    params = {'node_table': 'a_table'}
    mock_metadata_store.get_sensors.return_value = []
    result = client.simulate_post('/metadata/sensors', json=params)

    assert result.json['data'] == []


def test_field_key_error(client):
    wrong_key = 'node_t'
    params = {wrong_key: 'nt'}
    result = client.simulate_post('/metadata/sensors', json=params)

    import falcon
    assert result.status == falcon.HTTP_422
    assert result.json['error message'] == 'KeyError: \'node_table\''


def test_on_post_found(client, mock_metadata_store):
    mock_metadata_store.get_sensors.return_value = [{'sensor_id': 'node1', 'time': '2018-05-27T16:37:31.428136866Z', 'lat': 1, 'lng': 1},
                                               {'sensor_id': 'node2', 'time': '2018-05-27T16:37:31.428136866Z', 'lat': 2, 'lng': 2}]
    params = {"node_table": 'nt'}
    result = client.simulate_post('/metadata/sensors', json=params)

    print(result.json['data'])
    assert result.json['data'] == [{'sensor_id': 'node1', 'latlng': [1, 1]}, {'sensor_id': 'node2', 'latlng': [2, 2]}]