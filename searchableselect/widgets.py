from django import forms
from django.db.models.loading import get_model
from django.template.loader import render_to_string


class SearchableSelect(forms.CheckboxSelectMultiple):
    class Media:
        css = {
            'all': (
                'searchableselect/main.css',
            )
        }
        js = (
            'searchableselect/bloodhound.min.js',
            'searchableselect/typeahead.jquery.min.js',
            'searchableselect/main.js',
        )

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        self.search_field = kwargs.pop('search_field')

        super(SearchableSelect, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []

        values = get_model(self.model).objects.filter(pk__in=value)

        final_attrs = self.build_attrs(attrs, name=name)

        return render_to_string('searchableselect/select.html', dict(
            field_id=final_attrs['id'],
            field_name=final_attrs['name'],
            values=values,
            model=self.model,
            search_field=self.search_field
        ))
