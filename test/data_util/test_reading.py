import pytest
from src.data_util import client
from src.data_util.data import get_reading


def test_found():
    data = [{
        "measurement": 'test_measurement',
        "time": '2018-01-01T00:00:00Z',
        "fields": {'test_field': 1},
        "tags": {"sensor_id": 1}
    }]

    client.write_points(data)
    res = get_reading(sensor_id=1, field='test_field', timestamp='2018-01-01T00:00:00Z',
                   measurement='test_measurement')
    client.drop_measurement('test_measurement')
    assert len(res) == 1


def test_not_found():
    data = [{
        "measurement": 'test_measurement',
        "time": '2018-01-01T00:00:00Z',
        "fields": {'test_field': 1},
        "tags": {"sensor_id": 1}
    }]

    client.write_points(data)
    res = get_reading(sensor_id=1, field='test_field', timestamp='2018-01-02T00:00:00Z',
                   measurement='test_measurement')
    client.drop_measurement('test_measurement')
    assert len(res) == 0


def test_invalid_time():
    data = [{
        "measurement": 'test_measurement',
        "time": '2018-01-01T00:00:00Z',
        "fields": {'test_field': 1},
        "tags": {"sensor_id": 1}
    }]

    client.write_points(data)
    with pytest.raises(Exception) as excinfo:
        res = get_reading(sensor_id=1, field='test_field', timestamp='2018-01-02T00:00:00',
                   measurement='test_measurement')
    assert str(excinfo.value) == 'invalid timestamp string'
    client.drop_measurement('test_measurement')


def test_invalid_field():
    data = [{
        "measurement": 'test_measurement',
        "time": '2018-01-01T00:00:00Z',
        "fields": {'test_field': 1},
        "tags": {"sensor_id": 1}
    }]

    client.write_points(data)
    res = get_reading(sensor_id=1, field='invalid_field', timestamp='2018-01-02T00:00:00Z',
                measurement='test_measurement')
    assert len(res) == 0
    client.drop_measurement('test_measurement')
