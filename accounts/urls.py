from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('user_delete/<int:user_id>/', UserDeleteView.as_view(), name='user_delete'),
]