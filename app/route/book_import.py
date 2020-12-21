from falcon import Request, Response, status_codes

from app.service import BookService


class BookImportResource:

    def __init__(self, book_service: BookService):
        self._book_service = book_service

    def on_put(self, req: Request, resp: Response):
        self._book_service.import_books(req.query_string)
        resp.status = status_codes.HTTP_ACCEPTED
