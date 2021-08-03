from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from .models import User

from api.serializer import UserSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

@api_view(['GET'])
def getUsers(request):
  users = User.objects.all()
  serializer = UserSerializer(users, many=True)
  
  return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def signIn(request):
  if 'studentId' not in request.data or 'password' not in request.data:
    return Response({'detail': 'body 요소가 누락되었습니다'}, status=status.HTTP_400_BAD_REQUEST)
  
  studentId = request.data['studentId']
  password = request.data['password']
  user = User.objects.filter(student_id=studentId)

  if not user.exists():
    return Response({'detail': '아이디가 없거나 비밀번호가 틀렸습니다'}, status=status.HTTP_404_NOT_FOUND)

  user = User.objects.get(student_id=studentId)
  serializer = UserSerializer(user)

  if not serializer.validate_password(password, user.password):
    return Response({'detail': '아이디가 없거나 비밀번호가 틀렸습니다'}, status=status.HTTP_404_NOT_FOUND)

  payload = jwt_payload_handler(user)
  token = jwt_encode_handler(payload)
  
  return Response({
    'token': token,
    'user': serializer.data
  })