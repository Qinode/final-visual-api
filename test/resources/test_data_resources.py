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
    mock_data_store.get_reading.return_value = []
    params = {"sensor_id": 1, "field": "field1", "timestamp": '2018-01-01T00:00:00Z'}
    result = client.simulate_post('/data', json=params)

    assert result.json['data'] == []


def test_field_key_error(client):
    wrong_key = 'ield'
    params = {"sensor_id": 1, wrong_key: "field1", "timestamp": '2018-01-01T00:00:00Z'}
    result = client.simulate_post('/data', json=params)

    import falcon
    assert result.status == falcon.HTTP_422
    assert result.json['error message'] == 'KeyError: \'field\''


def test_field_invalid_timestamp(client, mock_data_store):
    from influxdb.exceptions import InfluxDBClientError
    import falcon

    invalid_timestamp = '2018-'
    mock_data_store.get_reading.side_effect = InfluxDBClientError("Invalid Timestamp: {}".format(invalid_timestamp))

    params = {"sensor_id": 1, "field": "field1", "timestamp": invalid_timestamp}
    result = client.simulate_post('/data', json=params)

    assert result.status == falcon.HTTP_422
    assert result.json['error message'] == 'Invalid Timestamp: {}'.format(invalid_timestamp)
