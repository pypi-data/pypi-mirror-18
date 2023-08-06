# coding=utf-8
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.itercompat import is_iterable
from six import string_types

from stdnumfield.validators import StdnumFormatValidator
from . import settings
from .forms import StdnumField
from .utils import listify


__all__ = [
    'StdNumField',
]


class StdNumField(models.CharField):
    """Model field that can store an stdnum value"""

    def __init__(self, formats, *args, **kwargs):
        if formats is None:
            raise ImproperlyConfigured('StdNumField defined without formats')
        if not is_iterable(formats) or isinstance(formats, string_types):
            formats = [formats]
        for format in formats:
            if format not in settings.DEFAULT_FORMATS:
                raise ValueError(
                    'Unknown format for StdNumField: "{}". Is it missing from '
                    'settings.STDNUMFIELD["DEFAULT_FORMATS"]?'.format(
                        format,
                    ))
        if 'alphabets' in kwargs:
            alphabets = kwargs.pop('alphabets')
            alphabets = listify(alphabets)
        else:
            alphabets = None
        self.formats = formats
        self.alphabets = alphabets
        # TODO make dynamic when/if stdnum provides this data:
        kwargs["max_length"] = 254
        super(StdNumField, self).__init__(*args, **kwargs)
        self.validators.append(
            StdnumFormatValidator(self.formats, self.alphabets))

    def deconstruct(self):
        name, path, args, kwargs = super(StdNumField, self).deconstruct()
        kwargs['formats'] = self.formats
        kwargs['alphabets'] = self.alphabets
        del kwargs["max_length"]
        return name, path, args, kwargs

    def get_internal_type(self):
        return 'CharField'

    def formfield(self, **kwargs):
        defaults = {
            'form_class': StdnumField,
            'formats': self.formats,
            'alphabets': self.alphabets,
        }
        defaults.update(kwargs)
        return super(StdNumField, self).formfield(**defaults)
