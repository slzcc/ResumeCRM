# -*- coding: utf-8 -*-
from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import async_to_sync
from channels.auth import login, logout
from repository import models
from channels.db import database_sync_to_async

# 自定义websocket处理类
class Common(AsyncWebsocketConsumer):

    async def connect(self):
        # 创建连接时调用
        await self.accept()

        self.content = ""

        for item in self.scope["query_string"].decode('utf-8').split("&"):
            key, value = item.split("=")
            if key == "auth":
                self.uuid = value
            elif key == "target":
                self.target = value
            elif key == "content":
                self.content = value

        self.user = await database_sync_to_async(self.get_user)()

        # 将新的连接加入到群组
        if self.user:
            await self.channel_layer.group_add(self.user.uuid, self.channel_name)
        else:
            return

        # print(dir(self.channel_layer))
    async def receive(self, text_data=None, bytes_data=None):
        # 收到信息时调用

        # login the user to this session.
        try:
            await login(self.scope, self.user)
        except:
            return

        # save the session (if the session backend does not access the db you can use `sync_to_async`)
        await database_sync_to_async(self.scope["session"].save)()

        if self.content:
            text_data = self.content

        # 信息群发
        await self.channel_layer.group_send(
            self.target,
            {
                "type": "chat.message",
                "text": text_data,
            },
        )

    async def disconnect(self, close_code):
        # 连接关闭时调用
        # 将关闭的连接从群组中移除
        await self.channel_layer.group_discard(self.user.uuid, self.channel_name)
        
        # await logout(self.scope)
        
        await self.close()

    async def chat_message(self, event):
        # Handles the "chat.message" event when it's sent to us.
        await self.send(text_data=event["text"])

    def get_user(self):
        return models.UserProfile.objects.filter(uuid=self.uuid).last()
