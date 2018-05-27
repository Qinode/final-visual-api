import falcon
import json
import logging

logger = logging.getLogger(__name__)


class DataResources:
    def __init__(self, store):
        self.__store = store


    def on_post(self, req, resp):
        params = json.load(req.bounded_stream)
        logger.info('request: {}'.format(params))

        res = self.__store.get_reading(sensor_id=params['sensor_id'], field=params['field'], timestamp=params['timestamp'])
        res_json = {"data": res}

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(res_json)
