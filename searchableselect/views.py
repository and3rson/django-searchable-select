try:
    # Django <=1.9
    from django.db.models.loading import get_model

    # Django 1.6.*
    import django
    if django.VERSION[0] == 1 and django.VERSION == 6:
        def get_model_wrapper(model):
            get_model(*model.split('.'))

        get_model = get_model_wrapper

except ImportError:
    # Django 1.10+
    from django.apps import apps
    get_model = apps.get_model

from django.utils.encoding import smart_str
from django.http import HttpResponse

try:
    from django.http import JsonResponse
except ImportError as e:
    # Django < 1.7
    from django.utils import simplejson
    class JsonResponse(HttpResponse):
        """
            JSON response
        """
        def __init__(self, content, mimetype='application/json', status=None, content_type=None):
            super(JsonResponse, self).__init__(
                content=simplejson.dumps(content),
                mimetype=mimetype,
                status=status,
                content_type=content_type,
    )

from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def filter_models(request):
    model_name = request.GET.get('model')
    search_field = request.GET.get('search_field')
    value = request.GET.get('q')
    limit = int(request.GET.get('limit', 10))
    try:
        model = get_model(model_name)
    except LookupError as e:  # pragma: no cover
        return JsonResponse(dict(status=400, error=e.message))
    except (ValueError, AttributeError) as e:  # pragma: no cover
        return JsonResponse(dict(status=400, error='Malformed model parameter.'))

    values = model.objects.filter(**{'{}__icontains'.format(search_field): value})[:limit]
    values = [
        dict(pk=v.pk, name=smart_str(v))
        for v
        in values
    ]

    return JsonResponse(dict(result=values))
