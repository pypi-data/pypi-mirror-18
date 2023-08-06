# coding=utf-8
try:
    from django.conf.urls import url
except ImportError:
    from django.core.urlresolvers import url

from .views import (
    SampleFormView,
    SuccessView,
)


urlpatterns = [
    url(r'^sample_form/$', SampleFormView.as_view(), name='sample_form'),
    url(r'^success/$', SuccessView.as_view(), name='success'),
]
