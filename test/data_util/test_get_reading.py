import pytest
from src.data_util import client
from src.data_util.get import get_reading


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


def test_not_found_by_time():
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

def test_not_found_by_id():
    data = [{
        "measurement": 'test_measurement',
        "time": '2018-01-01T00:00:00Z',
        "fields": {'test_field': 1},
        "tags": {"sensor_id": 1}
    }]

    client.write_points(data)
    res = get_reading(sensor_id=2, field='test_field', timestamp='2018-01-02T00:00:00Z',
                   measurement='test_measurement')
    client.drop_measurement('test_measurement')
    assert len(res) == 0


def test_not_found_by_field():
    data = [{
        "measurement": 'test_measurement',
        "time": '2018-01-01T00:00:00Z',
        "fields": {'test_field': 1},
        "tags": {"sensor_id": 1}
    }]

    client.write_points(data)
    res = get_reading(sensor_id=1, field='invalid_field', timestamp='2018-01-01T00:00:00Z',
                measurement='test_measurement')
    assert len(res) == 0
    client.drop_measurement('test_measurement')


def test_invalid_time():
    data = [{
        "measurement": 'test_measurement',
        "time": '2018-01-01T00:00:00Z',
        "fields": {'test_field': 1},
        "tags": {"sensor_id": 1}
    }]

    client.write_points(data)
    with pytest.raises(Exception) as excinfo:
        res = get_reading(sensor_id=1, field='test_field', timestamp='2018-01-01T00:00:00',
                   measurement='test_measurement')
    assert str(excinfo.value) == 'invalid timestamp string'
    client.drop_measurement('test_measurement')


def test_value():
    data = [{
        "measurement": 'test_measurement',
        "time": '2018-01-01T00:00:00Z',
        "fields": {'test_field': 1},
        "tags": {"sensor_id": 1}
    }]

    client.write_points(data)
    res = get_reading(sensor_id=1, field='test_field', timestamp='2018-01-01T00:00:00Z',
                measurement='test_measurement')
    assert len(res) == 1
    # assert res[0]['sensor_id'] == 1
    assert res[0]['test_field'] == 1
    assert res[0]['time'] == '2018-01-01T00:00:00Z'
    client.drop_measurement('test_measurement')


def test_multiple_value():
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

    client.write_points(data)
    res = get_reading(sensor_id=1, field='test_field', timestamp='2018-01-01T00:00:00Z', measurement='test_measurement')
    assert len(res) == 2
    # assert res[0]['sensor_id'] == 1
    assert res[0]['test_field'] == 1
    assert res[0]['time'] == '2018-01-01T00:00:00Z'
    # assert res[1]['sensor_id'] == 1
    assert res[1]['test_field'] == 2
    assert res[1]['time'] == '2018-01-02T00:00:00Z'
    client.drop_measurement('test_measurement')
