import falcon
import json
import logging

logger = logging.getLogger(__name__)


class SeriesLatest:
    def __init__(self, store):
        self.__store = store

    def on_post(self, req, resp):
        params = json.load(req.bounded_stream)
        logger.info('request: {}'.format(params))

        try:
            res = self.__store.get_latest(field=params['field'])
            res_json = {"data": res}
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
