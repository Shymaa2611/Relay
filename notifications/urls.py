from django.urls import path
from .views import create_notification, get_notifications

urlpatterns = [
    path('notifications_create/', create_notification, name='create_notification'),
    path('get_notifications/', get_notifications, name='get_notifications'),
]
