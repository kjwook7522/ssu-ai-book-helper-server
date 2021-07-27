from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from api.serializer import UserSerializer

@api_view(['GET'])
def getUsers(request):
  users = User.objects.all()
  serializer = UserSerializer(users, many=True)
  
  return Response(serializer.data)