import falcon
from src.resources.data_resources import DataResources

app = falcon.API()
app.add_route('/data', DataResources())
