from django.urls import path
from api import auth

urlpatterns = [
  path('user', auth.getUsers, name='get_users'),
]