from marshmallow import Schema, fields, validates, ValidationError


class BookSchema(Schema):
    title = fields.String(required=True)
    author = fields.String(required=False, allow_none=True, missing=None)
    published_date = fields.Date(required=False, allow_none=True, missing=None)
    isbn = fields.String(required=False, allow_none=True, missing=None)
    page_count = fields.Integer(required=False, allow_none=True, missing=None)
    cover_url = fields.Url(required=False, allow_none=True, missing=None)
    language = fields.String(required=False, allow_none=True, missing=None)

    class Meta:
        strict = True

    @validates('isbn')
    def validate_isbn(self, value):
        if value is not None and not (10 <= len(value) <= 13):
            raise ValidationError('ISBN must have 10-13 characters.')

    @validates('language')
    def validate_language(self, value):
        if len(value) != 2:
            raise ValidationError('Wrong language (ISO 639-1 code expected).')
