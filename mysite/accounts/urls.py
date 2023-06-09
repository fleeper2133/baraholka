from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('', Profile.as_view(), name='profile'),
    path('update/', profile_update, name='profile_update'),
    path('<int:pk>', UserProfile.as_view(), name='profile_user')
]

