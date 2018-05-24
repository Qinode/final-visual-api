import falcon
import json
from src.data_util.data import *

logging.config.fileConfig('/api/logging.ini')
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


class DataResources:
    def on_post(self, req, resp):
        js = json.load(req.bounded_stream)
        logger.info(js)
        resp.status = falcon.HTTP_200
        resp.body = ('\nhello world\n\n')