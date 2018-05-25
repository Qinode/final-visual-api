import falcon
import json
from src.data_util.get import *

logging.config.fileConfig('/api/logging.ini')
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


class DataResources:
    def on_post(self, req, resp):
        params = json.load(req.bounded_stream)
        logger.info('request: {}'.format(params))

        res = get_reading(sensor_id=params['sensor_id'], field=params['field'], timestamp=params['timestamp'])
        res_json = {"data": res}

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(res_json)
