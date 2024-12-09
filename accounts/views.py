from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from .models import newUser
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token

class LoginView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
           
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
            })
        return Response({"detail": "Invalid credentials or user is not an admin."}, status=status.HTTP_401_UNAUTHORIZED)

class AdminProtectedView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        return Response({'message': 'admin'})


def get_all_users(request):
    users= newUser.objects.all()
    user_data = [
        {   'id':user.id,
            'username': user.user.username,
            'password': user.plaintext_password
        }
        for user in users
    ]
    return JsonResponse(user_data, safe=False)
 
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if username and password:
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                )
                newuser = newUser.objects.create(
                    user=user,
                    plaintext_password=password
                )

                return JsonResponse({'message': 'User created successfully', 'user_id': user.id})

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Username and password are required'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'DELETE':
        user = get_object_or_404(newUser, id=user_id)
        user.user.delete()  
        user.delete() 
        return JsonResponse({'message': 'User deleted successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from notifications.models import Notification

@csrf_exempt
def delete_all_users(request):
    try:
       
        Notification.objects.all().delete()

        return JsonResponse({'status': 'success', 'message': 'All Use have been deleted.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
 