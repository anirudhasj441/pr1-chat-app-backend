from django.urls import path
from . import views

urlpatterns = [
    path('', views.index.as_view()),
    path('search/', views.search.as_view())
]