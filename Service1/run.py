import os
import uvicorn
import django
import asyncio
from grpc import aio
from django.core.asgi import get_asgi_application


# Function to run HTTP server using Uvicorn (Django ASGI)
async def run_http_server():
    asgi_app = get_asgi_application()
    config = uvicorn.Config(asgi_app, host="0.0.0.0", port=8000, workers=3)
    server = uvicorn.Server(config)
    await server.serve()


# Function to run gRPC server
async def run_grpc_server():
    from apps.grpc.server import serve as grpc_serve  # import grpc server function
    server = aio.server()
    grpc_serve(server)  # Register your gRPC services here
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    await server.start()  # Non-blocking start for gRPC
    print(f"gRPC server started on {listen_addr}")
    await server.wait_for_termination()


async def main():
    await asyncio.gather(
        run_http_server(),
        run_grpc_server()
    )


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
    django.setup()
    asyncio.run(main())
