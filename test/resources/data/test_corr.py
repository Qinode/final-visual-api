from falcon import testing
import falcon
import pytest
from mock import MagicMock
from api import create_app

class TestCorr(object):

    @pytest.fixture()
    def mock_data_store(self):
        return MagicMock()

    @pytest.fixture()
    def client(self, mock_data_store):
        return testing.TestClient(create_app(mock_data_store))

    def test_corr(self, client):
        params = {'series1': 'a', 'series2': 'b'}
        result = client.simulate_get('/data/corr', params=params)

        corr = result.json['corr']
        for point in corr:
            assert len(point) == 2

    def test_corr_400(self, client):
        params = {'series1': 'a'}
        result = client.simulate_get('/data/corr', params=params)

        assert result.status == falcon.HTTP_400
        assert result.json['error message'] == 'bad series parameters'
