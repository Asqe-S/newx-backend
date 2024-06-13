from django.urls import path
from authentication.views import *

urlpatterns = [
    path('register/<str:role>/',
         UserRegistrationView.as_view(), name='user_register'),


]