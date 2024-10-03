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

    async def disconnect(self, close_code):
        NotificationConsumer.connected_clients.remove(self)

    async def receive(self, text_data=None):
        try:
            if text_data:
                try:
                    data = json.loads(text_data) 
                    message_type = data.get("type", "")

                    if message_type == "text":
                        message = data.get("message", "")
                        await self.send(text_data=json.dumps({
                            "message": message,
                            "type": "text"
                        }))

                    elif message_type == "image":
                        image_data = data.get("image", "")
                        try:
                            image_base64 = process_image(image_data)
                            await self.send(text_data=json.dumps({
                                "message": image_base64,
                                "type": "image"
                            }))
                        except Exception as e:
                            logger.error(f"Error processing image: {e}")
                            await self.send(text_data=json.dumps({
                                "error": "Failed to process image",
                                "type": "error"
                            }))

                    else :
                        voice_data = data.get("voice", "")
                        try:
                            voice_str = process_voice(voice_data)  
                            await self.send(text_data=json.dumps({
                                "message": voice_str,
                                "type": "voice"
                            }))
                        except Exception as e:
                            logger.error(f"Error processing voice: {e}")
                            await self.send(text_data=json.dumps({
                                "error": "Failed to process voice",
                                "type": "error"
                            }))

                except json.JSONDecodeError as e:
                    logger.error(f"Received non-JSON text message: {e}")
                    await self.send(text_data=json.dumps({
                        "error": "Invalid JSON format",
                        "type": "error"
                    }))

        except Exception as e:
            logger.error(f"Error handling message: {e}")

    @classmethod
    async def send_notification(cls, message, message_type):
        for client in cls.connected_clients:
            await client.send(text_data=json.dumps({
                "message": message,
                "type": message_type
            }))
