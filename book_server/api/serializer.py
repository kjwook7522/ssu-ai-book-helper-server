from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User as test
from api.models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    exclude = ('token', 'password', 'groups', 'user_permissions')
  
  def validate_password(self, password, userPassword):
    return check_password(password, userPassword)