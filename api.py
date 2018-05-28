import falcon
from src.resources.data.series_start_from import SeriesStartFrom
from src.resources.metadata.filed_info import FieldInfo
from src.resources.metadata.sensor_infor import SensorInfo
import logging.config

logging.config.fileConfig('/api/logging.ini')

# Used for testing only, the data_store will be a mock object.
def create_app(data_store):
    app = falcon.API()
    ds = SeriesStartFrom(data_store)
    mf = FieldInfo(data_store)
    ms = SensorInfo(data_store)
    app.add_route('/data', ds)
    app.add_route('/metadata/fields', mf)
    app.add_route('/metadata/sensors', ms)

    return app


def get_client():
    from influxdb import InfluxDBClient
    client = InfluxDBClient(host='146.169.47.32', username='zq17', password='661231Icl', database='winery_data')

    return client


def get_app():
    from src.store.data_store import DataStore
    from src.store.metadata_store import MetadataStore

    client = get_client()

    data_store = DataStore(client)
    metadata_store = MetadataStore(client)

    app = falcon.API()
    app.add_route('/data', SeriesStartFrom(data_store))
    app.add_route('/metadata/fields', FieldInfo(metadata_store))
    app.add_route('/metadata/sensors', SensorInfo(metadata_store))

    return app


app = get_app()



