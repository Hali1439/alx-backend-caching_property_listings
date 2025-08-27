from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property

# Cache this view for 15 minutes
@cache_page(60 * 15)
def property_list(request):
    properties = Property.objects.all().values(
        "id", "title", "description", "price", "location"
    )
    return JsonResponse({"data": list(properties)}, safe=False)
