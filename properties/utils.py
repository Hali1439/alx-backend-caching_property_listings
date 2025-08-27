from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)


def get_all_properties():
    """
    Return all properties, using low-level Redis cache.
    Cache key: 'all_properties'
    TTL: 1 hour
    """
    properties = cache.get('all_properties')
    if properties is None:
        # Cache miss → query DB
        properties = list(Property.objects.all().values(
            "id", "title", "description", "price", "location"
        ))
        # Store in Redis for 1 hour
        cache.set('all_properties', properties, 3600)
    return properties


def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss stats and calculate hit ratio.
    """
    conn = get_redis_connection("default")
    info = conn.info()

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total = hits + misses

    hit_ratio = (hits / total) if total > 0 else 0.0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 4),  # 4 decimal precision
    }

    # Log for debugging
    logger.info(f"Redis Cache Metrics: {metrics}")

    return metrics
