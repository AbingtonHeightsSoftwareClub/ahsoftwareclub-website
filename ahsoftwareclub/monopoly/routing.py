from django.urls import re_path

from . import consumers

"""
    re_path is a regular expression matching a URL pattern

    Websockets paths can be weird, so we need regular expression to better describe the url

    The following path means if you have a url ahsoftware.club/ws/monopoly/<room_name>
    Send the websocket the room name value was a kwarg (keyword argument--like a dictionary)
    That is what is in the scope value

    """
monopoly_websocket_urlpatterns = [
    re_path(r"ws/monopoly/(?P<room_name>\w+)/$", consumers.MonopolyConsumer.as_asgi()),
]