"""
ASGI config for ahsoftwareclub project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ahsoftwareclub.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

# The urls for all websockets need to be imported so we put them all together
from chatroom.routing import chatroom_websocket_urlpatterns
from monopoly.routing import monopoly_websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            # Each set of url patterns is a list of routes. We add together each list to combine the lists, which combine the routes
            AuthMiddlewareStack(URLRouter(chatroom_websocket_urlpatterns + monopoly_websocket_urlpatterns))
        ),
    }
)
