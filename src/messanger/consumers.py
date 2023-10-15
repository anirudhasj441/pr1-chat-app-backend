from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = "test_consumer"
#         self.room_group_name = "test_consumer_group"
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_name,
#             self.room_group_name
#         )
#         self.accept()
#         self.send(text_data=json.dumps({'status': 'connected'}))

#     def receive(self, text_data=None, bytes_data=None):
#         pass

#     def disconnect(self, code):
#         pass


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer_group"

        await self.channel_layer.group_add(
            self.room_name, 
            self.room_group_name
        )

        await self.accept()
        await self.send(text_data=json.dumps({'status': 'connected'}))

    async def receive(self, text_data):
        print(text_data)
        await self.send(text_data=text_data)


    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.room_group_name
        )
        await self.send(text_data=json.dumps({'message': 'Bye!'}))