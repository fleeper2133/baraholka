from django.urls import path
from .views import *

urlpatterns = [
    path('', ProfilesMessage.as_view(), name='messager'),
    path('<int:pk>', get_messages, name='message')
]