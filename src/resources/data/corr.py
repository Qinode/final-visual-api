import falcon
import json
import logging

logger = logging.getLogger(__name__)


class Correlation:
    def __init__(self, store):
        self.__store = store

    def on_get(self, req, resp):
        params = req.params
        logger.info('request: {}'.format(params))

        if 'series1' not in params or 'series2' not in params:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({'error message': 'bad series parameters'})
        else:
            resp.status = falcon.HTTP_200
            resp.body = json.dumps({'corr': [[1, 2], [2, 3]]})
