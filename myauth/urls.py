from django.urls import path
from .views import *

urlpatterns =  [
    path('signup', RegistrationAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login')
]