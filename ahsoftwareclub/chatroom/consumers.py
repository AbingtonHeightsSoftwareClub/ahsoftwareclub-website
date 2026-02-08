import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import Group

from users.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user_name = await self.get_name()

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        users_list = await self.get_group_users_sync(self.room_name)
        active_users = []
        active_user_ids = []
        print(users_list)
        for user in users_list:
            active_users.append(user.get_username())
            active_user_ids.append(user.id)
        self.active_users = active_users
        self.active_user_ids = active_user_ids

        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print(message)
        # Send message to room group
        await self.channel_layer.group_send(
            
            self.room_group_name, {"type": "chat.message", "message":
                {"message_text": message,
                 "user_name": self.scope['user'].username,
                 "active_users": self.active_users,
                 "active_user_ids": self.active_user_ids}}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    async def chat_connect(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def get_name(self):
        user = self.scope["user"]
        return user.get_username()

    @sync_to_async
    def get_group_users_sync(self, group_name):
        print(Group.objects.all().values_list("name", flat=True))
        group = Group.objects.get(name=group_name)
        users_list = list(group.user_set.all())
        return users_list
