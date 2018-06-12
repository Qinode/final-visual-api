import influxdb
import logging

logger = logging.getLogger(__name__)


class MetadataStore(object):
    def __init__(self, client):
        self._client = client

    def get_sensors(self, node_table):
        query = 'select * from {}'.format(node_table)

        try:
            return list(self._client.query(query).get_points())
        except influxdb.exceptions.InfluxDBClientError:
            raise

    def get_fields(self, sensor_id):
        query = 'select * from {sensor_id}'.format(sensor_id=sensor_id)
        logger.debug(query)

        try:
            return list(self._client.query(query).get_points())
        except influxdb.exceptions.InfluxDBClientError:
            raise

