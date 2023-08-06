# coding=utf-8
from django.forms.forms import Form

from stdnumfield.forms import StdnumField


class SampleForm(Form):
    oib = StdnumField(formats=['hr.oib'])
