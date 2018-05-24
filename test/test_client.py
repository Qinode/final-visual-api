import falcon
from src.resources.data_resources import DataResources


def create():
    app = falcon.API()
    app.add_route('/data', DataResources())
    return app
