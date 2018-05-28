from api import get_client
import pytest

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
    res = data_store.get_latest(field='test_field', measurement='test_measurement')
    data_client.drop_measurement('test_measurement')
    assert len(res) == 1
    assert res[0]["sensor_id"] == "id"
    assert res[0]["test_field"] == 1


def test_not_found(data_client, data_store):
    res = data_store.get_latest(field='test_field', measurement='test_measurement')
    data_client.drop_measurement('test_measurement')
    assert len(res) == 0


def test_found_two(data_client, data_store):
    data = [{
        "measurement": 'test_measurement',
        "time": '2018-01-01T00:00:00Z',
        "fields": {'test_field': 1},
        "tags": {"sensor_id": "id1"}
        }, {
        "measurement": 'test_measurement',
        "time": '2018-01-03T10:00:00Z',
        "fields": {'test_field': 2},
        "tags": {"sensor_id": "id2"}
    }]

    data_client.write_points(data)
    res = data_store.get_latest(field='test_field', measurement='test_measurement')
    data_client.drop_measurement('test_measurement')
    assert len(res) == 2
    assert {'sensor_id': 'id1', 'test_field': 1} in res
    assert {'sensor_id': 'id2', 'test_field': 2} in res


def test_latest(data_client, data_store):
    data = [{
        "measurement": 'test_measurement',
        "time": '2018-01-01T00:00:00Z',
        "fields": {'test_field': 1},
        "tags": {"sensor_id": "id1"}
        }, {
        "measurement": 'test_measurement',
        "time": '2018-01-02T00:00:00Z',
        "fields": {'test_field': 2},
        "tags": {"sensor_id": "id1"}
        }
    ]

    data_client.write_points(data)
    res = data_store.get_latest(field='test_field', measurement='test_measurement')
    data_client.drop_measurement('test_measurement')
    assert len(res) == 1
    assert res[0]['sensor_id'] == 'id1'
    assert res[0]['test_field'] == 2
