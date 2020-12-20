from falcon import Request, Response, status_codes
from marshmallow.exceptions import ValidationError

from app.service import BookService
from app.schema import BookSchema


class BookListResource:
    schema = BookSchema()

    def __init__(self, book_service: BookService):
        self._book_service = book_service

    def on_get(self, req: Request, resp: Response):
        books = self._book_service.get_all_books(req.query_string)
        resp.media = [book.as_dict() for book in books]

    def on_post(self, req: Request, resp: Response):
        try:
            data = self.schema.load(req.media or {})  # if validation error then return bad request
        except ValidationError as err:
            resp.status = status_codes.HTTP_BAD_REQUEST
            resp.media = err.messages
            return

        created = self._book_service.create_book(data)
        if created:
            resp.status = status_codes.HTTP_CREATED
        else:
            resp.status = status_codes.HTTP_500
