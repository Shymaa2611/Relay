import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'Project.settings'  
django.setup()
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from api.processing_data import process_image, process_voice
from django.contrib.auth import get_user_model
logger = logging.getLogger(__name__)
User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    authenticated_clients = {}

    async def connect(self):
        user = self.scope.get('user', None)
        if user and user.is_authenticated:
            await self.accept()
            NotificationConsumer.authenticated_clients[self] = user
            logger.info(f"Authenticated client connected: {user.username}. Total clients: {len(NotificationConsumer.authenticated_clients)}")
        else:
            logger.warning(f"Unauthenticated connection attempt.")
            await self.close()

    async def disconnect(self, close_code):
        if self in NotificationConsumer.authenticated_clients:
            user = NotificationConsumer.authenticated_clients.pop(self)
            logger.info(f"Client disconnected: {user.username}. Total clients: {len(NotificationConsumer.authenticated_clients)}")

    async def receive(self, text_data=None):
        try:
            if text_data:
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
                        logger.info(f"Received image data of length: {len(image_data)}")
                        image_base64 = process_image(image_data)
                        response = {
                            "message": image_base64,
                            "type": "image"
                        }

                    except ValueError as e:
                        logger.error(f"Image processing error: {e}")
                        response = {
                            "error": str(e),
                            "type": "error"
                        }
                    except Exception as e:
                        logger.error(f"Unexpected error processing image: {e}")
                        response = {
                            "error": "Failed to process image",
                            "type": "error"
                        }

                elif message_type == "voice":
                    voice_data = data.get("voice", "")
                    try:
                        logger.info(f"Received voice data of length: {len(voice_data)}")
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
                else:
                    response = {
                        "message": "Invalid message type"
                    }

                await self.broadcast_message(response)

        except json.JSONDecodeError as e:
            logger.error(f"Received non-JSON text message: {e}")
            await self.send_error("Invalid JSON format")

        except Exception as e:
            logger.error(f"Error handling message: {e}")

    async def broadcast_message(self, response):
        # Send the message only to authenticated clients
        for client in NotificationConsumer.authenticated_clients:
            if client.scope["user"].is_authenticated:
                await client.send(text_data=json.dumps(response))

    async def send_error(self, error_message):
        error_response = {
            "error": error_message,
            "type": "error"
        }
        await self.send(text_data=json.dumps(error_response))
