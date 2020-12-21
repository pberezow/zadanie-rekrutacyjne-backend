import falcon
from .base_api_test import BaseApiTest


class TestBookListGet(BaseApiTest):
    URL = '/api/books'

    def test_get_with_empty_db(self):
        res = self.client.simulate_get(self.URL)
        assert res.status == falcon.HTTP_200
        assert res.json() == []
