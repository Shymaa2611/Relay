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
        if not text_data:
            return

        try:
            data = json.loads(text_data)
            message_type = data.get("type", "")

            if message_type == "text":
                message = data.get("message", "")
                await self.send_text_message(message)

            elif message_type == "image":
                image_data = data.get("image", "")
                await self.process_image_message(image_data)

            elif message_type == "voice":
                voice_data = data.get("voice", "")
                await self.process_voice_message(voice_data)

            else:
                logger.warning(f"Unknown message type: {message_type}")
                await self.send_error("Unsupported message type")

        except json.JSONDecodeError as e:
            logger.error(f"Received non-JSON text message: {e}")
            await self.send_error("Invalid JSON format")

        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await self.send_error("An error occurred while processing your request")

    async def send_text_message(self, message):
        await self.send(text_data=json.dumps({
            "message": message,
            "type": "text"
        }))

    async def process_image_message(self, image_data):
        try:
            # Ensure that image_data is valid and processed correctly
            result = process_image(image_data)
            
            if isinstance(result, tuple):
                logger.error(f"process_image returned a tuple: {result}")
                # Extract the first value or handle accordingly
                image_base64 = result[0]  # Assuming the first item is the desired string
            else:
                image_base64 = result

            await self.send(text_data=json.dumps({
                "message": image_base64,
                "type": "image"
            }))
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            await self.send_error("Failed to process image")

    async def process_voice_message(self, voice_data):
        try:
            # Ensure that voice_data is valid and processed correctly
            result = process_voice(voice_data)

            if isinstance(result, tuple):
                logger.error(f"process_voice returned a tuple: {result}")
                # Extract the first value or handle accordingly
                voice_str = result[0]  # Assuming the first item is the desired string
            else:
                voice_str = result

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
