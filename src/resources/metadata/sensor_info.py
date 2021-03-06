import falcon
import json
import logging


class SensorInfo:
    def __init__(self, store):
        self.__store = store
        self.logger = logging.getLogger(__name__)

    def on_post(self, req, resp):
        params = json.load(req.bounded_stream)
        self.logger.info('request: {}'.format(params))
        self.logger.info(req.host)

        try:
            res = self.__store.get_sensors(node_table=params['node_table'])
            self.logger.info(res)
            sensors = [{'sensor_id': e['sensor_id'], 'latlng': [e['lat'], e['lng']]} for e in res]
            res_json = {"data": sensors}
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(res_json)
        except KeyError as error:
            res_json = {"error message": 'KeyError: {}'.format(str(error))}
            resp.status = falcon.HTTP_422
            resp.body = json.dumps(res_json)
        except Exception as error:
            res_json = {"error message": str(error)}
            resp.status = falcon.HTTP_422
            resp.body = json.dumps(res_json)