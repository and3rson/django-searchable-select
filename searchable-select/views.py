from django.db.models.loading import get_model
from django.http import JsonResponse


def filter_models(request):
    model_name = request.GET.get('model')
    search_field = request.GET.get('search_field')
    value = request.GET.get('q')

    model = get_model(model_name)
    print {'{}__icontains'.format(search_field): value}

    values = model.objects.filter(**{'{}__icontains'.format(search_field): value})[:10]
    values = [
        dict(id=value.id, name=unicode(value))
        for value
        in values
    ]

    return JsonResponse(dict(result=values))
