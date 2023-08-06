# coding=utf-8
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import Client
from django.utils.html import escape

from stdnumfield.tests.forms import INVALID_OIB, VALID_OIB
from .models import SomeModel


class SampleFormViewTest(TestCase):

    def setUp(self):
        self.c = Client()

    def test_invalid_value(self):
        response = self.c.post(path='/sample_form/', data={'oib': INVALID_OIB})
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            escape('Value does not match with any of the formats: "hr.oib"'))

    def test_valid_value(self):
        response = self.c.post(path='/sample_form/', data={'oib': VALID_OIB})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/success/')


class ModelFieldTests(TestCase):

    def setUp(self):
        self.instance = SomeModel()

    def test_save_valid(self):
        self.instance.oib = VALID_OIB
        self.instance.save()
        instance = SomeModel.objects.first()
        self.assertEqual(instance.oib, VALID_OIB)

    def test_save_invalid(self):
        # this should also succeed because models are not validated on save
        self.instance.oib = INVALID_OIB
        self.instance.save()
        instance = SomeModel.objects.first()
        self.assertEqual(instance.oib, INVALID_OIB)

    def test_clean(self):
        self.instance.oib = INVALID_OIB
        self.assertRaises(
            ValidationError,
            self.instance.full_clean
        )
