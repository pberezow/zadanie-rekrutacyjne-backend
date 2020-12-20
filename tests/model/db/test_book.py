import pytest
import datetime
from app.model.db import BookEntity


@pytest.fixture
def data_with_id():
    return {
        'book_id': 'some_id',
        'title': 'Title',
        'author': 'Author',
        'published_date': datetime.date(2020, 1, 2),
        'isbn': '1234567890',
        'page_count': 100,
        'cover_url': 'http://www.someurl.pl/book/cover?size=small',
        'language': 'pl'
    }


@pytest.fixture
def data_without_id():
    return {
        'book_id': None,
        'title': 'Title',
        'author': 'Author',
        'published_date': datetime.date(2020, 1, 2),
        'isbn': '1234567890',
        'page_count': 100,
        'cover_url': 'http://www.someurl.pl/book/cover?size=small',
        'language': 'pl'
    }


class TestBookEntity:

    def test_generate_id_when_initialized_with_none(self, data_without_id):
        entity = BookEntity(**data_without_id)

        assert entity.id is not None

    def test_not_generate_id_when_provided(self, data_with_id):
        entity = BookEntity(**data_with_id)

        assert entity.id == data_with_id['book_id']

    def test_as_dict_converts_published_date(self, data_with_id):
        dct = BookEntity(**data_with_id).as_dict()

        assert type(dct['published_date']) is str
        assert dct['published_date'] == '2020-01-02'
