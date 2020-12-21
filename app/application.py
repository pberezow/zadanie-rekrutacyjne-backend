import falcon

from app.db_manager import DBManager
from app.repository.book_repository import BookRepository
from app.route import BookImportResource, BookDetailsResource, BookListResource
from app.service import BookService
from app.middleware import CrossOriginMiddleware


class Application(falcon.API):
    def __init__(self, config, is_test_instance=False, test_db_id=None):
        self.config = config

        self._setup_db(is_test_instance, test_db_id)
        self._setup_services()
        self._setup_middleware()

        super().__init__(middleware=self._middleware)

        self._setup_routes()

    def _setup_db(self, is_test_instance, test_db_id):
        self._db_manager = DBManager(db_config=self.config['db'], test_db_config=self.config['test_db'],
                                     is_test_instance=is_test_instance, test_db_id=test_db_id)
        self.book_repository = BookRepository(self._db_manager)

    def _setup_services(self):
        self.book_service = BookService(self.book_repository)

    def _setup_routes(self):
        self.add_route('/api/books', BookListResource(self.book_service))
        self.add_route('/api/books/import', BookImportResource(self.book_service))
        self.add_route('/api/books/{book_id}', BookDetailsResource(self.book_service))

    def _setup_middleware(self):
        self._middleware = [
            CrossOriginMiddleware(),
        ]
