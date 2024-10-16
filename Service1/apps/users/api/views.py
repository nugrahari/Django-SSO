from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.auths.libs import IsAuthenticatedAndNotBlacklisted

@api_view(['GET'])
@permission_classes([IsAuthenticatedAndNotBlacklisted])  # Hanya bisa diakses jika token JWT valid
def root_view(request):
    return Response({"message": "Welcome to User root api, You are authenticated"}, status=200)