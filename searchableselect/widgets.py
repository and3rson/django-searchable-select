from django import forms

try:
    # Django <=1.9
    from django.db.models.loading import get_model
except ImportError:
    # Django 1.10+
    from django.apps import apps
    get_model = apps.get_model

from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDict
try:
    from django.utils.datastructures import MergeDict
    DICT_TYPES = (MultiValueDict, MergeDict)
except:
    DICT_TYPES = (MultiValueDict,)


class SearchableSelect(forms.CheckboxSelectMultiple):
    class Media:
        css = {
            'all': (
                'searchableselect/main.css',
            )
        }
        js = (
            'searchableselect/jquery-2.2.4.min.js',
            'searchableselect/bloodhound.min.js',
            'searchableselect/typeahead.jquery.min.js',
            'searchableselect/main.js',
        )

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        self.search_field = kwargs.pop('search_field')
        self.many = kwargs.pop('many', True)
        self.limit = int(kwargs.pop('limit', 10))

        super(SearchableSelect, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []

        if not isinstance(value, (list, tuple)):
            # This is a ForeignKey field. We must allow only one item.
            value = [value]

        values = get_model(self.model).objects.filter(pk__in=value)
        try:
            final_attrs = self.build_attrs(attrs, name=name)
        except TypeError as e:
            # Fallback for django 1.10+
            final_attrs = self.build_attrs(attrs, extra_attrs={'name': name})

        return render_to_string('searchableselect/select.html', dict(
            field_id=final_attrs['id'],
            field_name=final_attrs['name'],
            values=values,
            model=self.model,
            search_field=self.search_field,
            limit=self.limit,
            many=self.many
        ))

    def value_from_datadict(self, data, files, name):
        if self.many and isinstance(data, DICT_TYPES):
            return data.getlist(name)
        return data.get(name, None)
