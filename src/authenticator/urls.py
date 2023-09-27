from django.urls import path 
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    # path('', views.UserApi.as_view()),
    path('register', views.RegisterUser.as_view()),
    path('login', views.LoginUser.as_view()),
    path('logout', views.LogOutUser.as_view()),
    path('verify', views.VerifyUser.as_view()),
    path('availibility', views.UserAvailability.as_view())
    
]