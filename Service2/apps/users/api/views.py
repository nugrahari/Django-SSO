from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.auths.libs import IsAuthenticatedAndNotBlacklisted
from apps.grpc.client import get_users


@api_view(['GET'])
@permission_classes([IsAuthenticatedAndNotBlacklisted])
def root_view(request):
    return Response({"message": "Welcome to User root api, You are authenticated"}, status=200)


@api_view(['GET'])
# @permission_classes([IsAuthenticatedAndNotBlacklisted])
def user_list(request):
    users = get_users()
    user_data = [
        {"id": user.id, "username": user.username, "email": user.email}
        for user in users
    ]
    return JsonResponse({"users": user_data})
