# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('<str:room_name>/', views.room, name='room'),
    path('webrtc/<str:room_name>/', views.webrtc, name='webrtc'),
]