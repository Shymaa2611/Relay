import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        try:
            if text_data:
                # Process the incoming text data
                data = json.loads(text_data)
                logger.info(f"Received text data: {data}")
                await self.send(text_data=json.dumps({
                    "message": f"Echo: {text_data}"
                }))
            elif bytes_data:
                # Decode and process the incoming binary data if applicable
                logger.info(f"Received bytes data: {bytes_data}")
                await self.send(text_data=json.dumps({
                    "message": f"Received binary data"
                }))
            else:
                logger.warning("No data received")
                await self.send(text_data=json.dumps({
                    "error": "No message received"
                }))
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON")
            await self.send(text_data=json.dumps({
                "error": "Invalid JSON format"
            }))
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            await self.send(text_data=json.dumps({
                "error": "An internal error occurred"
            }))
