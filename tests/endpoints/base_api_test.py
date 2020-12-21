from falcon import testing

from app.service import BookService
from app.repository import BookRepository
from .api_test_util import app_instance


class BaseApiTest:
    client: testing.TestClient = None
    book_service: BookService = None
    book_repository: BookRepository = None

    @staticmethod
    def setup_class(cls):
        # Clear database
        cls.client: testing.TestClient = app_instance()
        cls.book_service: BookService = cls.client.app.book_service
        cls.book_repository: BookRepository = cls.client.app.book_repository

    @classmethod
    def get_db_manager(cls):
        return cls.client.app._db_manager

    @staticmethod
    def teardown_class(cls):
        cls.get_db_manager().drop_test_db()
