from django.conf import settings

from catalog.models import Category
from django.core.cache import cache


def get_category_product_from_cashe():
    queryset = Category.objects.all()
    if settings.CACHE_ENABLED:
        key = 'categories'
        cache_data = cache.get(key)
        if cache_data is None:
            cache_data = queryset
            cache.set(key, cache_data)
        return cache_data
    return queryset