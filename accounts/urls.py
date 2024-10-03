from django.urls import path
from accounts.views import *

urlpatterns = [
    path('login/', AdminTokenObtainPairView.as_view(), name='admin_token_obtain_pair'),
    path('admin/protected/', AdminProtectedView.as_view(), name='admin_protected'),
    path('admin/profile/update/', AdminProfileUpdateView.as_view(), name='admin_update')

]