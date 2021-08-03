from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token
from api import auth

urlpatterns = [
  path('user', auth.getUsers, name='get_users'),
  path('signin', auth.signIn, name='signin'),
]