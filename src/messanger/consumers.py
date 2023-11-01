from channels.generic.websocket import AsyncWebsocketConsumer
import json
 
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "test_consumer"
        # self.room_group_name = "test_consumer_group"

        await self.channel_layer.group_add(
            self.room_name, 
            self.channel_name
        )

        await self.accept()
        await self.send(text_data=json.dumps({'status': 'connected'}))



    async def receive(self, text_data):
        print(text_data)
        await self.send(text_data=text_data)


    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
        # await self.send(text_data=json.dumps({'message': 'Bye!'}))

    async def sendCounter(self, event):
        print("Called send Counter")
        await self.send(
            text_data=json.dumps(
                {
                    'count': json.dumps(event['values'])
                }
            )
        )
