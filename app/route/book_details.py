from falcon import Request, Response, status_codes
from marshmallow.exceptions import ValidationError

from app.service import BookService
from app.schema import BookSchema


class BookDetailsResource:
    schema = BookSchema()

    def __init__(self, book_service: BookService):
        self._book_service = book_service

    def on_get(self, req: Request, resp: Response, book_id: str):
        book = self._book_service.get_book_by_id(book_id)
        if book:
            resp.media = book.as_dict()
        else:
            resp.status = status_codes.HTTP_NOT_FOUND

    def on_put(self, req: Request, resp: Response, book_id: str):
        try:
            data = self.schema.load(req.media or {})  # if validation error then return bad request
        except ValidationError as err:
            resp.status = status_codes.HTTP_BAD_REQUEST
            resp.media = err.messages
            return

        created = self._book_service.update_book(book_id, data)
        if created:
            resp.status = status_codes.HTTP_CREATED
        else:
            resp.status = status_codes.HTTP_NOT_FOUND
        # resp.media = created.as_dict()
