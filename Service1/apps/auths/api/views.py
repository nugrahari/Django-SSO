# views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import redis

# Redis instance
redis_instance = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    API Logout that blacklists the token in Redis
    """
    try:
        # Get the token from the request and blacklist it
        token = request.auth
        if token:
            # Store the token in Redis blacklist
            redis_instance.set(f"blacklist_{token}", "true", ex=settings.BLACKLIST_TOKEN_TTL)
            return Response({"message": "Logout successful. Token has been blacklisted."}, status=200)
        return Response({"error": "No token found"}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
