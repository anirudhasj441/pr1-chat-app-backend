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
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import os

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
    
class UserAvailability(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.filter(username = data['username']).first()
        if user is None:
            return Response({
                'user_available': True
            }, status.HTTP_200_OK)
            
        return Response({
            'user_available': False
        }, status.HTTP_200_OK)

class ChackPhoneNumber(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.filter(phone_number=data['phone_number']).first()
        if user is None:
            return Response({
                'phone_number_exists': False
            }, status.HTTP_200_OK)
        
        return Response({
            'phone_number_exists': True
        }, status.HTTP_200_OK)

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

class UpdateUser(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        # data = request.data
        serializer = userSerializer(request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({
                'status': 500, 
                'error': serializer.errors, 
                'message': "something went wrong"
            }, status.HTTP_200_OK)

        serializer.save()
        return Response({
            'user': serializer.data,
            'message': 'Details updated successfully'
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


# signals
@receiver(pre_save, sender=User)
def deleteOldProfilePic(sender, instance, **kwargs):
    profilePicPath = instance.__class__.objects.get(id=instance.id).profile_pic
    newProfilePicPath = instance.profile_pic
    if profilePicPath == newProfilePicPath:
        return
    if profilePicPath == '':
        return
    if os.path.exists(profilePicPath.path):
        os.remove(profilePicPath.path)

# @receiver(post_delete, sender=User)
# def deleteProfilePic(sender, instance, **kwargs):
