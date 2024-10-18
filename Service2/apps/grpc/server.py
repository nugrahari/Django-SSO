import grpc
from concurrent import futures
from .pbs import user_pb2, user_pb2_grpc
from django.contrib.auth.models import User


class UserService(user_pb2_grpc.UserServiceServicer):
    def GetUsers(self, request, context):
        users = User.objects.all()
        user_list = [
            user_pb2.User(id=user.id, username=user.username, email=user.email)
            for user in users
        ]
        return user_pb2.UserList(users=user_list)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server is running on port 50051...")
    server.wait_for_termination()
