""" from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from api.processing_data import process_send_image, process_send_voice
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
import json
@csrf_exempt  
@api_view(['POST'])
@permission_classes([IsAdminUser])  
def send_notification(request):
    jwt_auth = JWTAuthentication()
    try:
        user, _ = jwt_auth.authenticate(request)
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)}, status=401)

    if request.method == 'POST':
        notification_type, message, image, voice, channel_layer = get_data(request)
        
        if notification_type == 'text':
            send_message(message, 'text', channel_layer)
            return JsonResponse({'status': 'success', 'type': 'text'})

        elif notification_type == 'image' and image:
            try:
                img_str = process_send_image(image)
                send_message(img_str, 'image', channel_layer)
                return JsonResponse({'status': 'success', 'type': 'image'})
            except Exception as e:
                print(f"Error processing image: {e}")
                return JsonResponse({'status': 'error', 'error': 'Image processing failed'}, status=400)

        elif notification_type == 'voice' and voice:
            try:
                voice_str = process_send_voice(voice)
                send_message(voice_str, 'voice', channel_layer)
                return JsonResponse({'status': 'success', 'type': 'voice'})
            except Exception as e:
                print(f"Error processing voice: {e}")
                return JsonResponse({'status': 'error', 'error': 'Voice processing failed'}, status=400)

    return JsonResponse({'status': 'error', 'error': 'Invalid request'}, status=400)


def send_message(message, type, channel_layer):
    async_to_sync(channel_layer.group_send)(
        'notifications',
        {
            'message': message,
            'notification_type': type
        }
    )

def get_data(request):
    data = json.loads(request.body)
    notification_type = data.get('type')
    message = data.get('message')
    image = data.get('image')
    voice = data.get('voice')  
    channel_layer = get_channel_layer()
    return notification_type, message, image, voice, channel_layer
 """