from django.db import IntegrityError
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

@api_view(['POST'])
@permission_classes([AllowAny])
def signUp(request):
  if ('studentId' not in request.data or
  'password' not in request.data or
  'email' not in request.data or 
  'name' not in request.data or
  'phone' not in request.data
  ):
    return Response({'detail': 'body 요소가 누락되었습니다'}, status=status.HTTP_400_BAD_REQUEST)
  
  studentId = request.data['studentId']
  password = request.data['password']
  email = request.data['email']
  name = request.data['name']
  phone = request.data['phone']

  try:
    user = User.objects.create_user(studentId, name, email, password, phone)
    serializer = UserSerializer(user)
  except IntegrityError:
    return Response({'detail': '중복된 회원이 존재합니다'}, status=status.HTTP_409_CONFLICT)
  except ValueError:
    return Response({'detail': '데이터 타입이 맞지않습니다'}, status=status.HTTP_400_BAD_REQUEST)
  except TypeError:
    return Response({'detail': '데이터 타입이 맞지않습니다'}, status=status.HTTP_400_BAD_REQUEST)
  
  return Response({'detail': '회원가입이 성공적으로 완료되었습니다', 'user': serializer.data}, status=status.HTTP_200_OK)