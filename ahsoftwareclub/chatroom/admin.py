from django.contrib import admin

from chatroom.models import ChatGroup, GroupMessage
from users.models import User
# Register your models here.
admin.site.register(User)
admin.site.register(ChatGroup)
admin.site.register(GroupMessage)