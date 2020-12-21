from falcon import testing

from .api_test_util import app_instance


class BaseApiTest:
    client: testing.TestClient = None
    book_service = None

    @staticmethod
    def setup_class(cls):
        # Clear database
        cls.client: testing.TestClient = app_instance()
        cls.book_service = cls.client.app.book_service

    @classmethod
    def get_db_manager(cls):
        return cls.client.app._db_manager

    @staticmethod
    def teardown_class(cls):
        cls.get_db_manager().drop_test_db()
