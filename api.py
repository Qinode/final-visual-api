import falcon
from src.resources.DataResources import DataResources
import logging.config

logging.config.fileConfig('/api/logging.ini')

def create_app(data_store):
    app = falcon.API()
    app.add_route('/data', DataResources(data_store))

    return app


def get_client():
    from influxdb import InfluxDBClient
    client = InfluxDBClient(host='146.169.47.32', username='zq17', password='661231Icl', database='winery_data')

    return client


def get_app():
    from src.store.DataStore import DataStore
    data_store = DataStore(get_client())

    return create_app(data_store)


app = get_app()



