from django.urls import path
from api import auth

urlpatterns = [
  path('user', auth.handleUser, name='handle_user'),
  path('signin', auth.signIn, name='signin'),
  path('signup', auth.signUp, name='signup'),
  path('signout', auth.signOut, name='signout'),
  path('refresh', auth.refreshToken, name='refresh'),
]