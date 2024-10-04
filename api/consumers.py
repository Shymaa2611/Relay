import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the connection
        await self.accept()

    async def disconnect(self, close_code):
        # Handle disconnect logic
        pass

    async def receive(self, text_data=None, bytes_data=None):
        try:
            # Handling text data
            if text_data:
                logger.info(f"Received text data: {text_data}")
                data = json.loads(text_data)
                await self.send(text_data=json.dumps({
                    "message": f"Echo: {data.get('message', '')}"
                }))
            
            # Handling binary data
            elif bytes_data:
                logger.info(f"Received binary data")
                # If your data is binary, process it accordingly.
                await self.send(text_data=json.dumps({
                    "message": "Binary data received"
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
