from django.shortcuts import render
from rest_framework.views import APIView
# from django.contrib.auth.models import User
from .serializers import userSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from .authenticate import CustomAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate, logout
from django.conf import settings
from django.middleware import csrf
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

def getUserToken(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh) ,
        'access': str(refresh.access_token)
    }

class VerifyUser(APIView):
    # authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print(request.user)
        user = User.objects.get(username=request.user)
        serializer = userSerializer(user)
        return Response(serializer.data)

class RegisterUser(APIView):
    def post(self, request):
        data = request.data
        print(data)
        serializer = userSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                'status': 500, 
                'error': serializer.errors, 
                'message': "something went wrong"
            })
        
        user = serializer.save()
        print("user: ", type(user))
        refresh = RefreshToken.for_user(user)
        return Response({
            'status': 200, 
            'payload': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Successfull'
        })
    
class LoginUser(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"detail": "No active account found with the given credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        tokens = getUserToken(user)
        response = Response()
        # response.set_cookie(
        #     key=settings.SIMPLE_JWT["AUTH_COOKIE"],
        #     value=tokens["access"],
        #     expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
        #     secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
        #     httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
        #     samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"]
        # )
        # csrf.get_token(request)
        serializer = userSerializer(User.objects.get(username=user))
        print(user)
        response.data = {
            'message': 'Logined successfull',
            'refresh': tokens["refresh"],
            'access': tokens["access"],
            'user': serializer.data
        }
        response.status = status.HTTP_200_OK
        return response

class LogOutUser(APIView):
    def get(self, request):
        logout(request)
        return Response({
            "message": "logout user susseccfull!" 
        })



