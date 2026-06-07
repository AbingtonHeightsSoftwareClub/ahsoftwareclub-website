"""
ASGI config for ahsoftwareclub project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsoftwareclub.settings')
django_asgi_app = get_asgi_application()

from chatroom.routing import chatroom_websocket_urlpatterns
from monopoly.routing import monopoly_websocket_urlpatterns

combined_routes = chatroom_websocket_urlpatterns + monopoly_websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            combined_routes
        )
    ),
})