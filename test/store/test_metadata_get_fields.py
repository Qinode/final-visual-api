import pytest
from api import get_client


@pytest.fixture(scope='module')
def data_client():
    return get_client()


@pytest.fixture(scope='module')
def data_store():
    from src.store.MetadataStore import MetadataStore
    return MetadataStore(data_client())


def test_found(data_client, data_store):
    sensor_id = 'id'
    field = 'name_of_field'
    data = [{
        "measurement": sensor_id,
        "fields": {'test_field': 1},
        "tags": {"field": field}
    }]

    data_client.write_points(data)
    res = data_store.get_fields(sensor_id)
    data_client.drop_measurement(sensor_id)
    assert len(res) == 1


def test_found_two(data_client, data_store):
   sensor_id = 'id'
   field1 = 'name_of_field'
   field2 = 'other name'
   data = [{
       "measurement": sensor_id,
       "fields": {'test_field': 1},
       "tags": {"field": field1}
       },{
       "measurement": sensor_id,
       "fields": {'test_field': 1},
       "tags": {"field": field2}
       }

   ]

   data_client.write_points(data)
   res = data_store.get_fields(sensor_id)
   data_client.drop_measurement(sensor_id)
   assert len(res) == 2


def test_not_found(data_client, data_store):
   sensor_id = 'id'
   field = 'name_of_field'
   data = [{
       "measurement": sensor_id,
       "fields": {'test_field': 1},
       "tags": {"field": field}
   }]

   data_client.write_points(data)
   res = data_store.get_fields('non_exist_id')
   data_client.drop_measurement(sensor_id)
   assert len(res) == 0


def test_invalid_id(data_client, data_store):
   sensor_id = 'id'
   field = 'name_of_field'
   data = [{
       "measurement": sensor_id,
       "fields": {'test_field': 1},
       "tags": {"field": field}
   }]

   data_client.write_points(data)
   with pytest.raises(Exception):
       res = data_store.get_fields('name of id')
   data_client.drop_measurement(sensor_id)
