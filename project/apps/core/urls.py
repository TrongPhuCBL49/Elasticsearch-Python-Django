# from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

app_name = 'core'

urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name="index.html")),
    path('', TemplateView.as_view(template_name="index.html")),
]
