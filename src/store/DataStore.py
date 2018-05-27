import influxdb
import logging

logger = logging.getLogger(__name__)


class DataStore(object):
    def __init__(self, client):
        self.__client = client

    def get_reading(self, sensor_id, field, timestamp, measurement='winery_data'):
        query = 'select {} from {} where sensor_id=\'{}\' and time>=\'{}\''.format(field, measurement, sensor_id, timestamp)
        logger.debug(query)

        try:
            return list(self.__client.query(query).get_points())
        except influxdb.exceptions.InfluxDBClientError:
            raise


