from django.conf.urls import url
try:
    # Django <=1.9
    from django.conf.urls import patterns
except ImportError:
    # Django 1.10+
    patterns = None
from . import views


urls = [
    url('^filter$', views.filter_models, name='searchable-select-filter'),
]

if patterns:  # pragma: no cover
    urlpatterns = patterns('', urls)
else:
    urlpatterns = urls
