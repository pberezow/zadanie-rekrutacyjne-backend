from marshmallow import Schema, fields, validates, ValidationError

from .validators import is_numeric


class BookSchema(Schema):
    title = fields.String(required=True)
    author = fields.String(required=False, missing=None)
    published_date = fields.Date(required=False, missing=None)
    isbn = fields.String(required=False, missing=None)
    page_count = fields.Integer(required=False, missing=None)
    cover_url = fields.Url(required=False, missing=None)
    language = fields.String(required=False, missing=None)

    @validates('isbn')
    def validate_isbn(self, value):
        if value is not None and ((len(value) != 10 and len(value) != 13) or not is_numeric(value)):
            raise ValidationError('ISBN must have 10 or 13 digits.')

    @validates('language')
    def validate_language(self, value):
        if value is not None and len(value) != 2:
            raise ValidationError('Wrong language (ISO 639-1 code expected).')
