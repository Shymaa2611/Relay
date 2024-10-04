import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from django.urls import path

# Configure logging
logger = logging.getLogger(__name__)

class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        logger.info(f"Client connected: {self}")

    async def disconnect(self, close_code):
        logger.info(f"Client disconnected: {self}")

    async def receive(self, text_data=None):
        if text_data:
            data = json.loads(text_data)
            message = data.get('message', 'No message received')
            logger.info(f"Message received: {message}")
            await self.send(text_data=json.dumps({
                "message": f"Echo: {message}"
            }))
        else:
            await self.send(text_data=json.dumps({
                "message": "No message received"
            }))


