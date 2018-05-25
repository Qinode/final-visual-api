import influxdb

from src.data_util import client
import logging.config

logging.config.fileConfig('/api/logging.ini')
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


def get_reading(sensor_id, field, timestamp, measurement='winery_data'):
    query = 'select {} from {} where sensor_id=\'{}\' and time>=\'{}\''.format(field, measurement, sensor_id, timestamp)
    logger.info(query)

    try:
        raw_res = client.query(query)
        return [point for point in raw_res]
    except influxdb.exceptions.InfluxDBClientError:
        raise


