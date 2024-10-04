from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.processing_data import *
from django.shortcuts import render
@csrf_exempt  
def send_notification(request):
    if request.method == 'POST':
        notification_type,message,image,voice,channel_layer=get_data(request)
        
        if notification_type == 'text':
            send_message(message,'text',channel_layer)
            return JsonResponse({'status': 'success', 'type': 'text'})

        elif notification_type == 'image' and image:
            try:
                img_str = process_send_image(image)
                send_message(img_str,'image',channel_layer)
                return JsonResponse({'status': 'success', 'type': 'image'})
            except Exception as e:
                print(f"Error processing image: {e}")
                return JsonResponse({'status': 'error', 'error': 'Image processing failed'}, status=400)

        else: 
            try:
                voice_str = process_send_voice(voice)
                send_message(voice_str,'voice',channel_layer)
                return JsonResponse({'status': 'success', 'type': 'voice'})
            except Exception as e:
                print(f"Error processing voice: {e}")
                return JsonResponse({'status': 'error', 'error': 'Voice processing failed'}, status=400)

    return JsonResponse({'status': 'error', 'error': 'Invalid request'}, status=400)


def send_message(message,type,channel_layer):
    async_to_sync(channel_layer.group_send)(
                    'notifications',
                    {
                        'message': message,
                        'notification_type':type
                    }
                )
        

def get_data(request):
     notification_type = request.POST.get('type')
     message = request.POST.get('message')
     image = request.FILES.get('image')
     voice = request.FILES.get('voice')  
     channel_layer = get_channel_layer()
     return notification_type,message,image,voice,channel_layer


from django.shortcuts import render

def index(request):
    return render(request,"index.html")