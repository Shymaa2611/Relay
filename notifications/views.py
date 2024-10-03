from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .models import Notification
import json

@csrf_exempt
def create_notification(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            notification_type = data.get('type')
            content = data.get('message')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        file = request.FILES.get('file') 
        if notification_type not in ['text', 'voice', 'image']:
            return JsonResponse({'error': 'Invalid type'}, status=400)
        notification = Notification(type=notification_type, content=content)

        if file:
            file_name = default_storage.save(file.name, file)
            notification.file = file_name
        notification.save()
        return JsonResponse({'message': 'Notification created', 'id': notification.id}, status=201)

    return JsonResponse({'error': 'Invalid method'}, status=405)

def get_notifications(request):
    if request.method == 'GET':
        notifications = Notification.objects.all().values('id', 'type', 'content', 'file', 'created_at')
        return JsonResponse(list(notifications), safe=False)

    return JsonResponse({'error': 'Invalid method'}, status=405)
