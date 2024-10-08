from django.http import JsonResponse
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from .models import Notification
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
import base64

@api_view(['POST'])
@authentication_classes([JWTAuthentication])  
@permission_classes([IsAuthenticated, IsAdminUser])  
@parser_classes([MultiPartParser])
def create_notification(request):
    if request.method == 'POST':
        notification_type = request.POST.get('type')
        content = request.POST.get('message')
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



@api_view(['GET']) 
@permission_classes([AllowAny])
def get_notifications(request):
    if request.method == 'GET':
        notifications = Notification.objects.all().values('id', 'type', 'content', 'file', 'created_at')
        notifications_list = []
        
        for notification in notifications:
            file_path = notification.get('file')

            if file_path:
                if default_storage.exists(file_path):
                    with default_storage.open(file_path, 'rb') as f:
                        file_data = f.read()
                    file_base64 = base64.b64encode(file_data).decode('utf-8')
                    notification['file'] = file_base64

            notifications_list.append(notification)

        return JsonResponse(notifications_list, safe=False)

    return JsonResponse({'error': 'Invalid method'}, status=405)
