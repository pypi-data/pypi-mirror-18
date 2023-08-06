# coding=utf-8
from django.core.exceptions import ValidationError
from django.template.defaultfilters import truncatechars
from stdnum.exceptions import ValidationError as Stdnum_ValidationError
from django.utils.deconstruct import deconstructible

from stdnumfield import settings
from stdnumfield.utils import import_stdnum, listify


@deconstructible
class StdnumFormatValidator(object):
    formats = []
    alphabets = None
    empty = (None, '')

    def __init__(self, formats, alphabets=None):
        if formats is not None:
            self.formats = listify(formats)
        if alphabets is not None:
            self.alphabets = listify(alphabets)

    def _get_formats(self):
        if not self.formats:
            self.formats = settings.DEFAULT_FORMATS
        return self.formats

    def _get_alphabets(self):
        if self.alphabets is None:
            self.alphabets = [None] * len(self._get_formats())
        return self.alphabets

    def __call__(self, value):
        if value in self.empty:
            return
        formats = self._get_formats()
        alphabets = self._get_alphabets()
        if not formats:
            raise ValueError(
                'StdnumFormatValidator called without specified formats')
        for format, alphabet in zip(formats, alphabets):
            try:
                stdnum_format = import_stdnum(format)
            except ValueError:
                raise
            else:
                try:
                    if alphabet is None:
                        stdnum_format.validate(value)
                    else:
                        stdnum_format.validate(value, alphabet=alphabet)
                except Stdnum_ValidationError:
                    pass
                else:
                    return
        raise ValidationError(
            'Value does not match with any of the formats: "{}"'
            .format(truncatechars(', '.join(self.formats), 30)))
