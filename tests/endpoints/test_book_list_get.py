import pytest
import falcon
import datetime

from app.model.db import BookEntity
from .base_api_test import BaseApiTest


def data():
    return {
        'title': 'Book Title',
        'author': 'Book Author',
        'published_date': datetime.date.fromisocalendar(2020, 1, 2),
        'isbn': '1234567890',
        'page_count': 100,
        'cover_url': 'http://www.someurl.pl/book/cover?size=small',
        'language': 'pl'
    }


class TestBookListGet(BaseApiTest):
    URL = '/api/books'

    def setup_class(cls):
        super().setup_class(cls)
        cls.book = BookEntity(book_id=None, **data())
        cls.book_repository.insert_book(cls.book)

    def test_with_book(self):
        res = self.client.simulate_get(self.URL)
        assert res.status == falcon.HTTP_200
        assert res.json == [self.book.as_dict()]

    def test_filter_by_author(self):
        res = self.client.simulate_get(f'{self.URL}?author={self.book.author}')
        assert res.status == falcon.HTTP_200
        assert res.json == [self.book.as_dict()]

        res = self.client.simulate_get(f'{self.URL}?author={self.book.author}asd')
        assert res.status == falcon.HTTP_200
        assert res.json == []

    def test_filter_by_title(self):
        res = self.client.simulate_get(f'{self.URL}?title={self.book.title}')
        assert res.status == falcon.HTTP_200
        assert res.json == [self.book.as_dict()]

        res = self.client.simulate_get(f'{self.URL}?author={self.book.title}asd')
        assert res.status == falcon.HTTP_200
        assert res.json == []

    def test_filter_by_date(self):
        date = (self.book.published_date + datetime.timedelta(days=10)).strftime('%Y-%m-%d')
        res = self.client.simulate_get(f'{self.URL}?published_date__to={date}')
        assert res.status == falcon.HTTP_200
        assert res.json == [self.book.as_dict()]

        date = (self.book.published_date - datetime.timedelta(days=10)).strftime('%Y-%m-%d')
        res = self.client.simulate_get(f'{self.URL}?published_date__from={date}')
        assert res.status == falcon.HTTP_200
        assert res.json == [self.book.as_dict()]

        date = (self.book.published_date - datetime.timedelta(days=10)).strftime('%Y-%m-%d')
        print(date)
        res = self.client.simulate_get(f'{self.URL}?published_date__to={date}')
        assert res.status == falcon.HTTP_200
        assert res.json == []

    def test_filter_by_language(self):
        res = self.client.simulate_get(f'{self.URL}?language={self.book.language}')
        assert res.status == falcon.HTTP_200
        assert res.json == [self.book.as_dict()]

        res = self.client.simulate_get(f'{self.URL}?language=qw')
        assert res.status == falcon.HTTP_200
        assert res.json == []