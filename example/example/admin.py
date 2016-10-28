from django.contrib import admin
from django import forms
from searchableselect.widgets import SearchableSelect
from .models import Cat, Food


class CatAdminForm(forms.ModelForm):
    class Meta:
        model = Cat
        exclude = ()
        widgets = {
            'favorite_foods': SearchableSelect(model='example.Food', search_field='name', many=True)
        }


class CatAdmin(admin.ModelAdmin):
    form = CatAdminForm


class FoodAdmin(admin.ModelAdmin):
    pass


admin.site.register(Cat, CatAdmin)
admin.site.register(Food, FoodAdmin)
