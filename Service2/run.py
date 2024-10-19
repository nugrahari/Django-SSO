import os
import uvicorn
import django
import asyncio
from grpc import aio
from django.core.asgi import get_asgi_application


# Function to run HTTP server using Uvicorn (Django ASGI)
async def run_http_server():
    asgi_app = get_asgi_application()
    config = uvicorn.Config(asgi_app, host="0.0.0.0", port=8001, workers=1)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
    django.setup()
    asyncio.run(run_http_server())
