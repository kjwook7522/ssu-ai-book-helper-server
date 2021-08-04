from django.db import IntegrityError
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from .models import User

from api.serializer import UserSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

@api_view(['GET', 'DELETE'])
def handleUser(request):
  if request.method == 'GET':
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
  
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  if request.method == 'DELETE':
    user = request.user
    user.delete()
    return Response({'detail': '%d님 삭제가 완료되었습니다' % user.student_id})

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

  user = user.first()

  if not check_password(password, user.password):
    return Response({'detail': '아이디가 없거나 비밀번호가 틀렸습니다'}, status=status.HTTP_404_NOT_FOUND)

  token = publishToken(user)
  updateUserToken(user, token)
  serializer = UserSerializer(user)

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

@api_view(['POST'])
def signOut(request):
  user = request.user
  updateUserToken(user, None)
  return Response({'detail': '로그아웃이 완료되었습니다'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def refreshToken(request):
  user = request.user
  token = publishToken(user)
  updateUserToken(user, token)

  return Response({'token': token}, status=status.HTTP_200_OK)

def publishToken(user):
  payload = jwt_payload_handler(user)
  token = jwt_encode_handler(payload)
  return token

def updateUserToken(user, token):
  user.token = token
  user.save()