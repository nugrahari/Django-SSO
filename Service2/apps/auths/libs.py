# permissions.py

import redis
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed

# Connect to Redis
redis_instance = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])

class IsAuthenticatedAndNotBlacklisted(IsAuthenticated):
    """
    Custom permission to check if the JWT token is blacklisted in Redis.
    """
    def has_permission(self, request, view):
        # Check if the request has a valid JWT token
        is_authenticated = super().has_permission(request, view)
        
        if is_authenticated:
            token = request.auth
            if token:
                try:
                    # Check if the token is blacklisted
                    if redis_instance.get(f"blacklist_{token}"):
                        raise AuthenticationFailed('Token has been blacklisted.')
                except redis.ConnectionError:
                    # Redis is down, treat token as valid
                    return True
        
        return is_authenticated
