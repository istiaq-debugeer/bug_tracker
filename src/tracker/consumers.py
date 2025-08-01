import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ProjectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.projects_id = self.scope["url_route"]["kwargs"]["projects_id"]
        self.room_group_name = f"projects_{self.projects_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        # Not needed for your use case
        pass

    # Receive message from group
    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["message"]))
