from django.urls import path 
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('', views.UserApi.as_view()),
    path('register', views.RegisterUser.as_view()),
    path('login', views.LoginUser.as_view()),
    
]