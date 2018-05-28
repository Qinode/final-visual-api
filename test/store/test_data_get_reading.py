import pytest
from api import get_client

@pytest.fixture()
def data_client():
    return get_client()


@pytest.fixture()
def data_store():
    from src.store.data_store import DataStore
    return DataStore(data_client())


def test_found(data_client, data_store):
    data = [{
        "measurement": 'test_measurement',
        "time": '2018-01-01T00:00:00Z',
        "fields": {'test_field': 1},
        "tags": {"sensor_id": "id"}
    }]

    data_client.write_points(data)
    res = data_store.get_reading(sensor_id="id", field='test_field', start_from='2018-01-01T00:00:00Z',
                                 measurement='test_measurement')
    data_client.drop_measurement('test_measurement')
    assert len(res) == 1


def test_not_found_by_time(data_client, data_store):
    data = [{
        "measurement": 'test_measurement',
        "time": '2018-01-01T00:00:00Z',
        "fields": {'test_field': 1},
        "tags": {"sensor_id": 1}
    }]

    data_client.write_points(data)
    res = data_store.get_reading(sensor_id=1, field='test_field', start_from='2018-01-02T00:00:00Z',
                                 measurement='test_measurement')
    data_client.drop_measurement('test_measurement')
    assert len(res) == 0


def test_not_found_by_id(data_client, data_store):
    data = [{
        "measurement": 'test_measurement',
        "time": '2018-01-01T00:00:00Z',
        "fields": {'test_field': 1},
        "tags": {"sensor_id": 1}
    }]

    data_client.write_points(data)
    res = data_store.get_reading(sensor_id=2, field='test_field', start_from='2018-01-02T00:00:00Z',
                                 measurement='test_measurement')
    data_client.drop_measurement('test_measurement')
    assert len(res) == 0


def test_not_found_by_field(data_client, data_store):
    data = [{
        "measurement": 'test_measurement',
        "time": '2018-01-01T00:00:00Z',
        "fields": {'test_field': 1},
        "tags": {"sensor_id": 1}
    }]

    data_client.write_points(data)
    res = data_store.get_reading(sensor_id=1, field='invalid_field', start_from='2018-01-01T00:00:00Z',
                                 measurement='test_measurement')
    assert len(res) == 0
    data_client.drop_measurement('test_measurement')


def test_invalid_time(data_client, data_store):
    data = [{
        "measurement": 'test_measurement',
        "time": '2018-01-01T00:00:00Z',
        "fields": {'test_field': 1},
        "tags": {"sensor_id": 1}
    }]

    data_client.write_points(data)
    with pytest.raises(Exception) as excinfo:
        res = data_store.get_reading(sensor_id=1, field='test_field', start_from='2018-01-01T00:00:00',
                                     measurement='test_measurement')
    assert str(excinfo.value) == 'invalid timestamp string'
    data_client.drop_measurement('test_measurement')


def test_value(data_client, data_store):
    data = [{
        "measurement": 'test_measurement',
        "time": '2018-01-01T00:00:00Z',
        "fields": {'test_field': 1},
        "tags": {"sensor_id": 1}
    }]

    data_client.write_points(data)
    res = data_store.get_reading(sensor_id=1, field='test_field', start_from='2018-01-01T00:00:00Z',
                                 measurement='test_measurement')
    assert len(res) == 1
    # assert res[0]['sensor_id'] == 1
    assert res[0]['test_field'] == 1
    assert res[0]['time'] == '2018-01-01T00:00:00Z'
    data_client.drop_measurement('test_measurement')


def test_multiple_value(data_client, data_store):
    data = [{
        "measurement": 'test_measurement',
        "time": '2018-01-01T00:00:00Z',
        "fields": {'test_field': 1},
        "tags": {"sensor_id": 1}
        }, {
        "measurement": 'test_measurement',
        "time": '2018-01-02T00:00:00Z',
        "fields": {'test_field': 2},
        "tags": {"sensor_id": 1}
        }
    ]

    data_client.write_points(data)
    res = data_store.get_reading(sensor_id=1, field='test_field', start_from='2018-01-01T00:00:00Z', measurement='test_measurement')
    assert len(res) == 2
    assert res[0]['test_field'] == 1
    assert res[0]['time'] == '2018-01-01T00:00:00Z'
    assert res[1]['test_field'] == 2
    assert res[1]['time'] == '2018-01-02T00:00:00Z'
    data_client.drop_measurement('test_measurement')
