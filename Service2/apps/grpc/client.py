import grpc
from django.conf import settings
from apps.grpc.pbs.user_pb2 import Empty
from apps.grpc.pbs.user_pb2_grpc import UserServiceStub


def get_users():
    # Ambil host dan port dari settings
    grpc_host = settings.GRPC_SERVER_HOST
    grpc_port = settings.GRPC_SERVER_PORT

    # Menghubungkan ke server gRPC
    with grpc.insecure_channel(f'{grpc_host}:{grpc_port}') as channel:
        stub = UserServiceStub(channel)
        response = stub.GetUsers(Empty())
        return response.users
