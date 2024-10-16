# permissions.py

import redis
from django.conf import settings
from django.contrib.auth.hashers import PBKDF2PasswordHasher
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


class CustomPBKDF2PasswordHasher(PBKDF2PasswordHasher):
    """
    Custom PBKDF2 Password Hasher that uses Django secret key for hashing.
    """
    def encode(self, password, salt, iterations=None):
        secret_key = settings.SECRET_KEY
        # Combine password with secret key for additional security
        combined_password = f"{password}{secret_key}"
        return super().encode(combined_password, salt, iterations)
    
    def verify(self, password, encoded):
        secret_key = settings.SECRET_KEY
        combined_password = f"{password}{secret_key}"
        return super().verify(combined_password, encoded)
