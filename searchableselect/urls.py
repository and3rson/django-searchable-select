from django.urls import re_path
from . import views


urlpatterns = [
    re_path('^filter$', views.filter_models, name='searchable-select-filter'),
]
