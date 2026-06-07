import json
import urllib.parse
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import Group


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_name = None
        self.room_group_name = None
        self.room_name = None

    import urllib.parse

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # JUST FREAKING ACCEPT IT
        await self.accept()

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        if self.scope.get("user") and self.scope["user"].is_authenticated:
            self.user_name = self.scope["user"].username
            username_to_send = self.user_name
            user_id_to_send = self.scope["user"].id
        else:
            try:
                query_params = dict(urllib.parse.parse_qsl(self.scope["query_string"].decode()))
                self.user_name = query_params.get("user", "MobileGuest")
            except Exception:
                self.user_name = "MobileGuest"
            username_to_send = self.user_name
            user_id_to_send = 0

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.connect",
                "username": username_to_send,
                "active_users": [username_to_send],
                "active_user_ids": [user_id_to_send]
            }
        )
    async def disconnect(self, close_code):
        user_id = self.scope["user"].id if self.scope["user"].is_authenticated else 0

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.disconnect",
                "userID": user_id
            }
        )

        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        if text_data_json["type"] == "message":
            message = text_data_json["message"]
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": message, "username": self.user_name}
            )
        elif text_data_json["type"] == "file":
            data_url = text_data_json["dataURL"]
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.file", "dataURL": data_url, "username": self.user_name}
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"type": "chat_message", "message": message, "username": username}))

    async def chat_connect(self, event):
        username = event["username"]
        active_users = event["active_users"]
        active_user_ids = event["active_user_ids"]

        await self.send(text_data=json.dumps({"type": "chat_connect", "username": username, "activeUsers": active_users,
                                              "activeUserIDs": active_user_ids}))

    async def chat_disconnect(self, event):
        userID = event["userID"]
        await self.send(text_data=json.dumps({"type": "chat_disconnect", "userID": userID}))

    async def chat_file(self, event):
        username = event["username"]
        data_url = event["dataURL"]
        await self.send(text_data=json.dumps({"type": "chat_file", "dataURL": data_url, "username": username}))

    @database_sync_to_async
    def get_name(self):
        user = self.scope["user"]
        if user and user.is_authenticated:
            try:
                return user.get_username()
            except Exception:
                return user.username
        return "MobileGuest"

    @sync_to_async
    def get_group_users_sync(self, group_name):
        try:
            group = Group.objects.get(name=group_name)
            users_list = list(group.user_set.all())
            return users_list
        except Exception as e:
            print(f"Database query failed: {e}")
            return []
