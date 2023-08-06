# coding=utf-8
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from django.core.exceptions import ValidationError
from django.test.testcases import TestCase

from stdnumfield.validators import StdnumFormatValidator


class ValidatorsTests(TestCase):

    def test_invalid_format(self):
        validator = StdnumFormatValidator(formats=['damn'])
        self.assertRaisesMessage(
            ValueError,
            'Unknown stdnum format: "damn"',
            validator,
            '123456',
        )

    def test_valid_format_valid_value(self):
        validator = StdnumFormatValidator(formats=['hr.oib'])
        validator('69435151530')

    def test_valid_format_invalid_value(self):
        validator = StdnumFormatValidator(formats=['hr.oib'])
        self.assertRaises(
            ValidationError,
            validator,
            '69435151531',
        )

    def test_default_format_valid_value(self):
        validator = StdnumFormatValidator(formats=['hr.oib'])
        validator('69435151530')

    @patch('stdnumfield.settings.DEFAULT_FORMATS', [])
    def test_empty_format(self):
        validator = StdnumFormatValidator(formats=None)
        self.assertRaisesMessage(
            ValueError,
            'StdnumFormatValidator called without specified formats',
            validator,
            '69435151530',
        )

    def test_custom_alphabet(self):
        validator = StdnumFormatValidator(
            formats='iso7064.mod_37_2',
            alphabets='0123456789X',
        )
        validator('079X')

    def test_custom_multiple_alphabets(self):
        validator = StdnumFormatValidator(
            formats=['iso7064.mod_37_2', 'iso7064.mod_37_36'],
            alphabets=['0123456789X', '0123456789'],
        )
        validator('002006673085')
