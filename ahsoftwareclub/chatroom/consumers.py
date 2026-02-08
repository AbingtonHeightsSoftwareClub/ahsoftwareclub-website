import json

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

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user_name = await self.get_name()

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # send a message saying someone connected (and tell the person who connected who's here)
        active_users, active_user_ids= [], []
        users = await self.get_group_users_sync(self.room_name)
        for user in users:
            active_users.append(user.username)
            active_user_ids.append(user.id)
        await self.channel_layer.group_send(self.room_group_name, {
            "type": "chat.connect",
            "username": self.scope["user"].username,
            "active_users": active_users,
            "active_user_ids": active_user_ids
        })

    async def disconnect(self, close_code):
        # tell everyone they left so it removes them from the activeUsers list
        await self.channel_layer.group_send(self.room_group_name, {
            "type": "chat.disconnect",
            "userID": self.scope["user"].id
        })

        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json["message"]
        # Send message to room group
        await self.channel_layer.group_send(
            
            self.room_group_name, {"type": "chat.message", "message": message, "username": self.user_name}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"type": "chat_message", "message": message, "username":username}))

    async def chat_connect(self, event):
        username = event["username"]
        active_users = event["active_users"]
        active_user_ids = event["active_user_ids"]

        await self.send(text_data=json.dumps({"type": "chat_connect", "username": username, "activeUsers": active_users, "activeUserIDs": active_user_ids}))

    async def chat_disconnect(self, event):
        userID = event["userID"]
        await self.send(text_data=json.dumps({"type": "chat_disconnect", "userID": userID}))

    @database_sync_to_async
    def get_name(self):
        user = self.scope["user"]
        return user.get_username()

    @sync_to_async
    def get_group_users_sync(self, group_name):
        group = Group.objects.get(name=group_name)
        users_list = list(group.user_set.all())
        return users_list
