from falcon import testing
import pytest
from mock import MagicMock
from api import create_app

# docker run <image-name> py.test


@pytest.fixture()
def mock_data_store():
    return MagicMock()


@pytest.fixture()
def client(mock_data_store):
    return testing.TestClient(create_app(mock_data_store))


def test_on_post_success_empty(client, mock_data_store):
    mock_data_store.get_latest.return_value = []
    params = {"sensor_id": "id", "field": "field1"}
    result = client.simulate_post('/data/latest', json=params)

    assert result.json['data'] == []


def test_field_key_error(client):
    wrong_key = 'ield'
    params = {"sensor_id": 1, wrong_key: "field1"}
    result = client.simulate_post('/data/latest', json=params)

    import falcon
    assert result.status == falcon.HTTP_422
    assert result.json['error message'] == 'KeyError: \'field\''


def test_on_post_success(client, mock_data_store):
    import falcon

    mock_data_store.get_latest.return_value = [{'sensor_id': 'id1', 'field1': 1}]

    params = {"sensor_id": 1, "field": "field1"}
    result = client.simulate_post('/data/latest', json=params)

    assert result.status == falcon.HTTP_200
    assert result.json['data'] == [{'sensor_id': 'id1', 'field1': 1}]
    assert len(result.json['data']) == 1