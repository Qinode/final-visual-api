import influxdb
import logging

logger = logging.getLogger(__name__)


class DataStore(object):
    def __init__(self, client):
        self.__client = client

    def get_reading(self, sensor_id, field, start_from, measurement='winery_data'):
        query = 'select {} from {} where sensor_id=\'{}\' and time>=\'{}\''.format(field, measurement, sensor_id, start_from)
        logger.debug(query)

        try:
            return list(self.__client.query(query).get_points())
        except influxdb.exceptions.InfluxDBClientError:
            raise

    def get_latest(self, field, group_tag='sensor_id', measurement='winery_data', sensor_id = None):
        if sensor_id is None:
            query = 'select {field} from {measurement} group by {group_tag} order by time desc limit 1'.format(
                field=field, measurement=measurement, group_tag=group_tag)

            try:
                res = list(self.__client.query(query).items())
                return [{'sensor_id': e[0][1]['sensor_id'], field: list(e[1])[0][field]} for e in res]
            except influxdb.exceptions.InfluxDBClientError:
                raise
