import influxdb
import logging

logger = logging.getLogger(__name__)


class MetadataStore(object):
    def __init__(self, client):
        self.__client = client

    def get_fields(self, sensor_id):
        query = 'select * from {sensor_id}'.format(sensor_id=sensor_id)
        logger.debug(query)

        try:
            return list(self.__client.query(query).get_points())
        except influxdb.exceptions.InfluxDBClientError:
            raise

