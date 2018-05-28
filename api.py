import falcon
from src.resources.DataResource import DataResources
from src.resources.MetadataFieldResource import MetadataFieldResource
from src.resources.MetadataSensorResource import MetadataSensorResource
import logging.config

logging.config.fileConfig('/api/logging.ini')

# Used for testing only, the data_store will be a mock object.
def create_app(data_store):
    app = falcon.API()
    ds = DataResources(data_store)
    mf = MetadataFieldResource(data_store)
    ms = MetadataSensorResource(data_store)
    app.add_route('/data', ds)
    app.add_route('/metadata/fields', mf)
    app.add_route('/metadata/sensors', ms)

    return app


def get_client():
    from influxdb import InfluxDBClient
    client = InfluxDBClient(host='146.169.47.32', username='zq17', password='661231Icl', database='winery_data')

    return client


def get_app():
    from src.store.DataStore import DataStore
    from src.store.MetadataStore import MetadataStore

    client = get_client()

    data_store = DataStore(client)
    metadata_store = MetadataStore(client)

    app = falcon.API()
    app.add_route('/data', DataResources(data_store))
    app.add_route('/metadata/fields', MetadataFieldResource(metadata_store))

    return app


app = get_app()



