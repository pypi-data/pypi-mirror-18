# coding=utf-8
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.test.testcases import TestCase

from ..models import StdNumField
from ..testproject.testapp.models import SomeModel
from .forms import VALID_OIB


class ModelFieldTests(TestCase):

    def setUp(self):
        self.instance = SomeModel()

    def test_save(self):
        self.instance.oib = VALID_OIB
        self.instance.save()
        instance = SomeModel.objects.first()
        self.assertEqual(instance.oib, VALID_OIB)

    def test_max_length_passed_to_formfield(self):
        """
        CharField passes its max_length attribute to form fields created using
        the formfield() method.
        """
        field = StdNumField('hr.oib')
        self.assertEqual(254, field.formfield().max_length)

    def test_no_formats(self):
        self.assertRaisesMessage(
            ImproperlyConfigured,
            'StdNumField defined without formats',
            StdNumField,
            None
        )

    def test_wrong_format(self):
        self.assertRaises(
            ValueError,
            StdNumField,
            'damn'
        )

    def test_alphabet_valid(self):
        field = StdNumField('iso7064.mod_37_2', alphabets='0123456789X')
        field.run_validators('0123456789X')

    def test_alphabet_invalid(self):
        field = StdNumField('iso7064.mod_37_2', alphabets='0123456789X')

        self.assertRaises(
            ValidationError,
            field.run_validators,
            '0123456789Y'
        )
