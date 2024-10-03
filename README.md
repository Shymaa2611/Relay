# RELAY 

This project implements a Django WebSocket-based notification system using Django Channels. The application allows sending and receiving real-time notifications, including text, image, and voice data, through WebSocket connections.

## Features

- Real-time WebSocket notifications
- Supports text, image (base64 encoded), and voice (base64 encoded) messages
- WebSocket consumer logic using `channels` for handling real-time events
- Async handling of WebSocket connections
- JWT authentication for securing WebSocket connections

## Requirements

- Python 3.8+
- Django 3.2+
- Django Channels 3.0+
- Redis (for channel layer)
- Pillow (for image processing)
- Pydub (for voice/audio processing)
- Django REST Framework SimpleJWT

## Installation

1. Clone the repository:

```bash
   git clone https://github.com/Shymaa2611/Relay.git
   cd Relay 
```
2. Install dependencies:
``` bash 
  pip install -r requirements.txt
```

## JWT Authentication

Obtaining a Token

To authenticate, you need to obtain a JWT token. You can do this by sending a POST request to the /api/token/ endpoint with your username and password.

### Example Request:

``` bash 
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```
### Example Response:

``` bash
{
    "refresh": "your_refresh_token",
    "access": "your_access_token"
}
```


## Running WebSocket Notifications
1. Run the Django development server:

``` bash
python manage.py runserver

```

## WebSocket URL

The WebSocket URL for notifications is:
``` bash 
ws://localhost:8000/ws/notifications/

```
You can send and receive the following message types:

    text: Simple text messages.
    image: Base64-encoded images.
    voice: Base64-encoded audio files.

## Example Message Payloads

### Text Message
``` bash
{
  "type": "text",
  "message": "Hello"
}

```

### Text Image
``` bash
{
  "type": "image",
  "image": "base64_encoded_image_data"
}

```
### Text Voice
``` bash
{
  "type": "voice",
  "voice": "base64_encoded_voice_data"
}


```

