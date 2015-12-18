from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns(
    '',
    url('^filter$', views.filter_models, name='searchable-select-filter'),
)
