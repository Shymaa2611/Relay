import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from api.processing_data import process_image, process_voice

logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncWebsocketConsumer):
    connected_clients = set()

    async def connect(self):
        await self.accept()
        NotificationConsumer.connected_clients.add(self)
        logger.info(f"Client connected: {self}")

    async def disconnect(self, close_code):
        NotificationConsumer.connected_clients.remove(self)
        logger.info(f"Client disconnected: {self}")

    async def receive(self, text_data=None):
        return str(text_data)
    async def send_text_message(self, message):
        await self.send(text_data=json.dumps({
            "message": message,
            "type": "text"
        }))

    async def process_image_message(self, image_data):
        try:
            image_base64 = process_image(image_data)
            await self.send(text_data=json.dumps({
                "message": image_base64,
                "type": "image"
            }))
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            await self.send_error("Failed to process image")

    async def process_voice_message(self, voice_data):
        try:
            voice_str = process_voice(voice_data)  
            await self.send(text_data=json.dumps({
                "message": voice_str,
                "type": "voice"
            }))
        except Exception as e:
            logger.error(f"Error processing voice: {e}")
            await self.send_error("Failed to process voice")

    async def send_error(self, error_message):
        await self.send(text_data=json.dumps({
            "error": error_message,
            "type": "error"
        }))

    @classmethod
    async def send_notification(cls, message, message_type):
        for client in cls.connected_clients:
            await client.send(text_data=json.dumps({
                "message": message,
                "type": message_type
            }))
