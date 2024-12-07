from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from .models import Notification
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(['POST'])
@authentication_classes([JWTAuthentication])  
@permission_classes([IsAuthenticated])  
@parser_classes([JSONParser])
def create_notification(request):
    if request.method == 'POST':
        data = request.data
        notification_type = data.get('type')
        content = data.get('message')

        if notification_type not in ['text', 'voice', 'image']:
            return JsonResponse({'error': 'Invalid type'}, status=400)

        notification = Notification(type=notification_type, content=content)
        notification.save()

        return JsonResponse({'message': 'Notification created', 'id': notification.id}, status=201)

    return JsonResponse({'error': 'Invalid method'}, status=405)


@api_view(['GET']) 
@permission_classes([AllowAny])
def get_notifications(request):
    if request.method == 'GET':
        notifications = Notification.objects.all().order_by('-created_at')[:20].values('id', 'type', 'content', 'created_at')
        print(len(list(notifications)))
        return JsonResponse(list(notifications), safe=False)

    return JsonResponse({'error': 'Invalid method'}, status=405)

