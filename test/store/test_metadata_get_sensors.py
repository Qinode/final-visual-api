import pytest
from api import get_client

test_measurement = 'tn'


@pytest.fixture(scope='function')
def data_client():
    return get_client()


@pytest.fixture(scope='function')
def data_store(data_client):
    from src.store.metadata_store import MetadataStore
    metadata_store = MetadataStore(data_client)
    return metadata_store


def test_found(data_client, data_store):
    sensor_id = 'tid'
    data = [{
        "measurement": test_measurement,
        "fields": {'lat': 1, 'lng': 1},
        "tags": {'id': sensor_id}
    }]

    data_client.write_points(data)
    res = data_store.get_sensors(test_measurement)
    data_client.drop_measurement(test_measurement)
    assert len(res) == 1
    assert res[0]['id'] == sensor_id
    assert res[0]['lat'] == 1
    assert res[0]['lng'] == 1


def test_found_two(data_client, data_store):
    test_node = 'tn'
    data = [{
            "measurement": test_measurement,
            "fields": {'lat': 1, 'lng': 1},
            "tags": {'id': 'tid1'}
        },
        {
            "measurement": test_node,
            "fields": {'lat': 2, 'lng': 2},
            "tags": {'id': 'tid2'}
        }
    ]

    data_client.write_points(data)
    res = data_store.get_sensors(test_measurement)
    data_client.drop_measurement(test_measurement)
    assert len(res) == 2


def test_not_found(data_client, data_store):
    res = data_store.get_sensors(test_measurement)
    data_client.drop_measurement(test_measurement)
    assert len(res) == 0
