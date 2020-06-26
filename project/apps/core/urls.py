# from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

app_name = 'core'

urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name="index.html")),
    # url(r'^autocomplete/', autocomplete_view, name='autocomplete-view'),
    # url(r'^student', student_detail, name='student-detail'),
    # url(r'^$', HomePageView.as_view(), name='index-view'),
    # path('', TemplateView.as_view(template_name="index.html")),
]
