import grpc
from concurrent import futures
from grpc_reflection.v1alpha import reflection  # Impor modul refleksi
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

    # Tambahkan service UserService ke server
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)

    # Daftar nama service untuk refleksi
    SERVICE_NAMES = (
        user_pb2_grpc.DESCRIPTOR.services_by_name['UserService'].full_name,
        reflection.SERVICE_NAME,
    )

    # Aktifkan refleksi
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    # Jalankan server pada port 50051
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server is running on port 50051...")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
