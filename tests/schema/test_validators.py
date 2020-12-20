import pytest

from app.schema.validators import is_numeric


class TestValidators:

    def test_is_numeric_with_non_numeric_string(self):
        value = 'adasdasdsd'

        result = is_numeric(value)

        assert result is False

    def test_is_numeric_with_numeric_string(self):
        value = '1234567890'

        result = is_numeric(value)

        assert result is True
