from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.request import Request

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def cache_action(key_prefix, timeout=CACHE_TTL):
    def decorator(action):
        def wrapper(self, request: Request, *args, **kwargs):
            authorization_header = request.headers["Authorization"]
            cache_key = f"{key_prefix}-${authorization_header}"

            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return Response(cached_data)

            response = action(self, request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=timeout)

            return response

        return wrapper

    return decorator
