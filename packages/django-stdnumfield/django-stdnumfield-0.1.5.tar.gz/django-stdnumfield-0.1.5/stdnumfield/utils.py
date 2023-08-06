# coding=utf-8
import importlib

from django.utils.itercompat import is_iterable
from six import string_types

from stdnumfield import STDNUM_FORMATS


def import_stdnum(num_format):
    """
    Returns Python module from stdnum package.

    Usage:
        >>> import_stdnum('damm')  #doctest: +ELLIPSIS
        <module 'stdnum.damm' from ...
        >>> import_stdnum('hr.oib')  #doctest: +ELLIPSIS
        <module 'stdnum.hr.oib' from ...

    """
    if num_format not in STDNUM_FORMATS:
        raise ValueError('Unknown stdnum format: "{}"'.format(num_format))
    return importlib.import_module('stdnum.{}'.format(num_format))


def listify(value):
    """
    Convert non-iterable non-string values to list of 1 element.

    Usage:
        >>> listify(101)
        [101]
        >>> listify('qwerty')
        ['qwerty']
        >>> listify([1, 2, 3])
        [1, 2, 3]

    :param value: any
    :return: list
    """
    if not is_iterable(value) or isinstance(value, string_types):
        value = [value]
    return value
