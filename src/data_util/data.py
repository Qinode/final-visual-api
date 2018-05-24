from src.data_util import client
import logging.config

logging.config.fileConfig('/api/logging.ini')
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


def get_data(sensor_id, measurement, timestamp, series='winery_data'):
    query = 'select {} from {} where sensor_id=\'{}\' and time>=\'{}\''.format(measurement, series, sensor_id, timestamp)
    logger.info(query)
    return client.query(query)

