from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Return all properties, using low-level Redis cache.
    Cache key: 'all_properties'
    TTL: 1 hour
    """
    # Try to fetch from Redis
    properties = cache.get('all_properties')
    if properties is None:
        # Cache miss → query DB
        properties = list(Property.objects.all().values(
            "id", "title", "description", "price", "location"
        ))
        # Store in Redis for 1 hour
        cache.set('all_properties', properties, 3600)
    return properties
