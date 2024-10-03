from django.urls import path
#from .views import send_notification,index
from .views import index
urlpatterns = [
    #path("send-notification/", send_notification, name="send_notification"),
    #path("", notification_test, name="notification_test"),
    path("",index, name="index")
 
]
