"""
ASGI config for urmart_demo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack
import web.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urmart_demo.settings')

# root routing
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack( # for ws:// or wss:// let AuthMiddlewareStack handle the requests
        URLRouter(
            web.routing.websocket_urlpatterns # eventually route it to consumers.py
        )
    )
    # Just Http for now.
})
