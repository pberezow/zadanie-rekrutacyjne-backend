import pytest
from marshmallow.exceptions import ValidationError

from app.schema import BookSchema


@pytest.fixture
def valid_data():
    return {
        'title': 'Book Title',
        'author': 'Book Author',
        'published_date': '2020-01-02',
        'isbn': '1234567890',
        'page_count': 100,
        'cover_url': 'http://www.someurl.pl/book/cover?size=small',
        'language': 'pl'
    }


class TestBookSchema:

    def setup(self):
        self.schema = BookSchema()

    def test_load_with_valid_data_success(self, valid_data):
        self.schema.load(valid_data)

    def test_load_without_title_fail(self, valid_data):
        data = valid_data
        data['title'] = None

        self.should_throw_validation_error(data)

    def test_validate_language_fail(self, valid_data):
        data = valid_data
        data['language'] = 'too-long'

        self.should_throw_validation_error(data)

        data['language'] = 'p'

        self.should_throw_validation_error(data)

    def test_validate_when_language_is_none_success(self, valid_data):
        data = valid_data
        data['language'] = None

        self.should_validate(data)

    @pytest.mark.parametrize("isbn", ['123456789', '12345678911', '123456789111', '12345678901234'])
    def test_validate_isbn_fail(self, valid_data, isbn):
        data = valid_data
        data['isbn'] = isbn

        self.should_throw_validation_error(data)

    def test_validate_isbn_non_numeric_fail(self, valid_data):
        data = valid_data
        data['isbn'] = 'withleng10'

        self.should_throw_validation_error(data)

    def test_validate_published_date_non_date_fail(self, valid_data):
        data = valid_data
        data['published_date'] = 'non date'

        self.should_throw_validation_error(data)

    def test_validate_url_non_url_fail(self, valid_data):
        data = valid_data
        data['url'] = 'non url string'

        self.should_throw_validation_error(data)

    def should_throw_validation_error(self, data):
        try:
            self.schema.load(data)
            assert False
        except ValidationError:
            assert True

    def should_validate(self, data):
        try:
            self.schema.load(data)
            assert True
        except ValidationError:
            assert False
