from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property  # assuming you already have a Property model

# Cache this view for 15 minutes (900 seconds)
@cache_page(60 * 15)
def property_list(request):
    properties = Property.objects.all().values(
        "id", "title", "description", "price", "location"
    )
    return JsonResponse(list(properties), safe=False)
