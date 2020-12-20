import uuid
import base64
import datetime
from typing import Optional


class BookEntity:
    def __init__(self, book_id: Optional[str], title: str, author: str, published_date: Optional[datetime.date],
                 isbn: Optional[str], page_count: Optional[int], cover_url: Optional[str], language: str):
        if book_id is None:
            self.id = base64.b64encode(uuid.uuid4().bytes).decode()
        else:
            self.id = book_id
        self.title = title
        self.author = author
        self.published_date = published_date
        self.isbn = isbn
        self.page_count = page_count
        self.cover_url = cover_url
        self.language = language

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'published_date': self.published_date.strftime("%Y-%m-%d") if self.published_date else None,
            'isbn': self.isbn,
            'page_count': self.page_count,
            'cover_url': self.cover_url,
            'language': self.language
        }
