from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from apps.auths.libs import IsAuthenticatedAndNotBlacklisted


@api_view(['GET'])
@permission_classes([IsAuthenticatedAndNotBlacklisted])
def root_view(request):
    return Response({"message": "Welcome to User root api, You are authenticated"}, status=200)
