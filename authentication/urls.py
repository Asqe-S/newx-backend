from django.urls import path
from authentication.views import *

urlpatterns = [
    path('register/<str:role>/',
         UserRegistrationView.as_view(), name='user_register'),

    path('verify-otp/<str:uid>/<str:token>/',
         OtpVerifyView.as_view(), name='verify_otp'),
    path('resend-otp/<str:uid>/<str:token>/',
         ResendOtpView.as_view(), name='resend_otp'),
         
]