# coding=utf-8
from django import forms

from . import settings
from .utils import listify
from .validators import StdnumFormatValidator


class StdnumField(forms.CharField):
    formats = None
    alphabets = None

    def __init__(self, max_length=None, min_length=None, strip=True,
                 formats=None, alphabets=None, *args, **kwargs):
        super(StdnumField, self).__init__(max_length, min_length, strip,
                                          *args, **kwargs)
        if formats is None:
            raise ValueError('StdnumField defined without formats')
        formats = listify(formats)
        if alphabets is not None:
            alphabets = listify(alphabets)
        if alphabets is not None and len(formats) != len(alphabets):
            raise ValueError(
                'StdnumField got alphabets and formats of different length')
        for format in formats:
            if format not in settings.DEFAULT_FORMATS:
                raise ValueError(
                    'Unknown format for StdnumField: "{}". Is it missing from '
                    'settings.STDNUMFIELD["DEFAULT_FORMATS"]?'.format(
                        format,
                    ))
        self.formats = formats
        self.alphabets = alphabets

    def validate(self, value):
        super(StdnumField, self).validate(value)
        validator = StdnumFormatValidator(self.formats, self.alphabets)
        validator(value)
