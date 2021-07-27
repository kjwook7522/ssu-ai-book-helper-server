from django.urls import path, include
from api import auth

urlpatterns = [
  path('user', auth.getUsers, name='get_users')
]