# coding=utf-8
from django.db import models

from stdnumfield.models import StdNumField


class SomeModel(models.Model):
    name = models.CharField(max_length=100)
    oib = StdNumField('hr.oib')
