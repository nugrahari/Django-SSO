import grpc
from concurrent import futures
from django.core.management.base import BaseCommand
from apps.grpc.server import serve as grpc_serve  # import grpc server function


class Command(BaseCommand):
    help = 'Run the gRPC server'

    def handle(self, *args, **kwargs):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        grpc_serve(server)  # Register your gRPC services here
        server.add_insecure_port('[::]:50051')
        server.start()
        print("gRPC server is running on port 50051...")
        server.wait_for_termination()
