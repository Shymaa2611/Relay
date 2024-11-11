from django.urls import path
from accounts.views import *
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    #path('users_login/', UsersLogin.as_view(), name='admin_token_obtain_pair'),
    path('admin/protected/', AdminProtectedView.as_view(), name='admin_protected'),
    path('create_user/',create_user, name='create_user'),
    path('delete_user/<int:user_id>/',delete_user, name='delete_user'),
    path('get_users/',get_all_users, name='get_users'),
    #path('delete_all/',delete_all_users, name='delete_all'),



]