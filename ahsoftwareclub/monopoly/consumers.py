import json

import random
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import Group
import urllib.parse




class MonopolyConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.user_name = None
        self.position = 1

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user_name = await self.get_name()
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        username_to_send = await self.get_group_users_sync(self.room_name)

        users = []
        for i in username_to_send:
            users.append(i.get_username())

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.connection",
                "username": self.user_name,
                "active_users": users
            }
        )



    async def disconnect(self, close_code):
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
                self.room_group_name, {"type": "chat.message", "message": message}
            )
        elif text_data_json["type"] == "roll":
            old_position = self.position
            roll = random.randint(1, 6) + random.randint(1, 6)
            self.position = (old_position + roll) % 41
            print(self.position)
            if self.position == 0:
                self.position = 1
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "monopoly.roll", "roll": roll, "current_position": self.position,
                                      "username": self.user_name}
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    async def chat_connection(self, event):
        username = event["username"]
        active_users = event["active_users"]
        print(active_users)
        await self.send(text_data=json.dumps(
            {
                "type": "chat_connection",
                "username": username,
                "activeUsers": active_users
                                              }))

    async def monopoly_roll(self, event):
        username = event["username"]
        roll = event["roll"]
        current_position = event["current_position"]

        await self.send(text_data=json.dumps(
            {"type": "monopoly_roll", "username": username, "roll": roll, "current_position": current_position})
        )

    @database_sync_to_async
    def get_name(self):
        user = self.scope["user"]
        name = user.get_username()

        return name

    @sync_to_async
    def get_group_users_sync(self, group_name):
        try:
            group = Group.objects.get(name=group_name)
            users_list = list(group.user_set.all())
            return users_list
        except Exception as e:
            print(f"Database query failed: {e}")
            return []

