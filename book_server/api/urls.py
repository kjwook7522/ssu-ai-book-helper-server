from django.urls import path
from api import auth

urlpatterns = [
  path('user', auth.getUsers, name='get_users'),
  path('signin', auth.signIn, name='signin'),
  path('signup', auth.signUp, name='signup'),
  path('refresh', auth.refreshToken, name='refresh'),
]