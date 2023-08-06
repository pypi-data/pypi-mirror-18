# coding=utf-8
try:
    from django.urls.base import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import SampleForm


class SampleFormView(FormView):
    form_class = SampleForm
    template_name = 'form.html'
    success_url = reverse_lazy('success')


class SuccessView(TemplateView):
    template_name = 'success.html'
