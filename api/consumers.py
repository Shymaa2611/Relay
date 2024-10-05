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
        logger.info(f"Client connected: {self.channel_name}. Total clients: {len(NotificationConsumer.connected_clients)}")

    async def disconnect(self, close_code):
        NotificationConsumer.connected_clients.remove(self)
        logger.info(f"Client disconnected: {self.channel_name}. Total clients: {len(NotificationConsumer.connected_clients)}")

    async def receive(self, text_data=None):
        try:
            if text_data:
                try:
                    data = json.loads(text_data)
                    message_type = data.get("type", "")
                    response = {}

                    if message_type == "text":
                        message = data.get("message", "")
                        response = {
                            "message": message,
                            "type": "text"
                        }

                    elif message_type == "image":
                        image_data = data.get("image", "")
                        try:
                            image_base64 = process_image(image_data)
                            response = {
                                "message": image_base64,
                                "type": "image"
                            }
                        except Exception as e:
                            logger.error(f"Error processing image: {e}")
                            response = {
                                "error": "Failed to process image",
                                "type": "error"
                            }

                    elif message_type == "voice":
                        voice_data = data.get("voice", "")
                        try:
                            voice_str = process_voice(voice_data)
                            response = {
                                "message": voice_str,
                                "type": "voice"
                            }
                        except Exception as e:
                            logger.error(f"Error processing voice: {e}")
                            response = {
                                "error": "Failed to process voice",
                                "type": "error"
                            }

                    await self.broadcast_message(response)

                except json.JSONDecodeError as e:
                    logger.error(f"Received non-JSON text message: {e}")
                    await self.send_error("Invalid JSON format")

        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def broadcast_message(self, response):
        logger.info(f"Broadcasting message: {response}")
        for client in NotificationConsumer.connected_clients:
            await client.send(text_data=json.dumps(response))

    async def send_error(self, error_message):
        error_response = {
            "error": error_message,
            "type": "error"
        }
        await self.broadcast_message(error_response)

