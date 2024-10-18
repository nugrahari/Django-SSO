import requests
from apps.grpc.pbs.user_pb2 import Empty, UserList
from apps.grpc.server import serve
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run the gRPC server'

    def test_grpc_http(self):
        request = Empty()

        # Ganti dengan URL yang benar
        url = 'http://localhost:802/grpc/UserService.GetUsers'
        headers = {
            'Content-Type': 'application/grpc',  # Content-Type untuk gRPC-Web
        }

        response = requests.post(url, headers=headers,
                                 data=request.SerializeToString())
        if response.status_code == 200:
            your_response = UserList()  # Membuat objek untuk menampung respons
            your_response.ParseFromString(
                response.content)  # Parse data dari respons

            print("status", response.status_code)
            print("Response message:", your_response)

        else:
            print("Error:", response.status_code, response.text)

    def handle(self, *args, **kwargs):
        self.test_grpc_http()
