import requests as rq
import threading
import psycopg2
import datetime
from typing import Optional, List, Dict
from urllib.parse import parse_qs

from app.repository import BookRepository
from app.model.db import BookEntity


class BookService:
    API_URL = 'https://www.googleapis.com/books/v1/volumes?{}&projection=full&startIndex={}&maxResults={}&key={}'
    ACCEPTED_BOOK_IDENTIFIERS = {'ISBN_10', 'ISBN_13'}

    def __init__(self, book_repository: BookRepository):
        self._book_repository = book_repository

    def get_all_books(self, query_string: Optional[str]) -> List[BookEntity]:
        if query_string:
            books = self._get_filtered_books(query_string)
        else:
            books = self._book_repository.get_all_books()
        return books

    def create_book(self, data: dict) -> bool:
        book = BookEntity(**{'book_id': None, **data})
        created_book = self._book_repository.insert_book(book)
        if created_book:
            return True
        else:
            return False

    def update_book(self, book_id: str, data: dict) -> bool:
        book = BookEntity(**{'book_id': book_id, **data})
        updated_book = self._book_repository.update_book(book)
        if updated_book:
            return True
        else:
            return False

    def get_book_by_id(self, book_id: str) -> Optional[BookEntity]:
        return self._book_repository.get_book_by_id(book_id)

    def _get_filtered_books(self, query_string: str) -> List[BookEntity]:
        params_dct = dict((k, v[0]) for k, v in parse_qs(query_string, keep_blank_values=False).items())

        print(params_dct)
        date_from = None
        if params_dct.get('published_date__from', None):
            try:
                date_from = self._map_str_to_date(params_dct['published_date__from'])
            except ValueError as err:
                print(err)
                pass
        date_to = None
        if params_dct.get('published_date__to', None):
            try:
                date_to = self._map_str_to_date(params_dct['published_date__to'])
            except ValueError:
                pass

        return self._book_repository.get_filtered_books(
            author=params_dct.get('author', None),
            title=params_dct.get('title', None),
            language=params_dct.get('language', None),
            date_from=date_from,
            date_to=date_to
        )

    def import_books(self, q: str) -> bool:
        threading.Thread(target=self._import_books_task, args=(q,), daemon=True).start()
        return True

    def _import_books_task(self, q: str):
        key = 'AIzaSyC4u_XpkDisOTDYQbVUBEyaSgcXkgH4Ft0'
        url = self.API_URL.format(q, 0, 1, key)
        start_index = 0
        max_results = 40
        results_count = rq.get(url).json()['totalItems']
        while start_index < results_count:
            url = self.API_URL.format(q, start_index, max_results, key)
            result = rq.get(url).json()
            results_count = result['totalItems']
            books_to_import = [BookEntity(**self._map_api_record_to_entity(r)) for r in result['items']]
            for b in books_to_import:
                try:
                    self._book_repository.insert_book(b)
                except psycopg2.Error as err:
                    pass
            start_index += max_results

    @staticmethod
    def _map_str_to_date(value: str) -> datetime.date:
        data = dict(zip(('year', 'month', 'day'), (*(int(v) for v in value.split('-')), 1, 1)))
        return datetime.date(**data)

    @staticmethod
    def _map_api_record_to_entity(record: Dict) -> Dict:
        entity = {
            'book_id': record['id'],
            'title': record['volumeInfo']['title'],
            'author': record['volumeInfo'].get('authors', [None])[0],
            'published_date': None,
            'page_count': record['volumeInfo'].get('pageCount', None),
            'language': record['volumeInfo'].get('language', None),
            'isbn': None,
            'cover_url': record['volumeInfo'].get('imageLinks', {}).get('smallThumbnail', None)
        }

        date = record['volumeInfo'].get('publishedDate', None)
        if date:
            try:
                entity['published_date'] = BookService._map_str_to_date(date)
            except ValueError:
                pass

        isbn = list(filter(
            lambda item: item['type'] in BookService.ACCEPTED_BOOK_IDENTIFIERS,
            record['volumeInfo'].get('industryIdentifiers', [])))
        if isbn:
            entity['isbn'] = isbn[0]['identifier']

        return entity
