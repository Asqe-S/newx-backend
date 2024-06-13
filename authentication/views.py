from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.tasks import *
from authentication.models import *
from authentication.serializers import *
from authentication.utils import *


class UserRegistrationView(APIView):
    def post(self, request, role):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data.pop('confirm_password', None)

        user = User.objects.create_user(**serializer.validated_data)

        if role == 'merchant':
            user.is_merchant = True

        user.save()

        otp, valid_until = generate_otp_and_validity()
        uid, token = generate_uid_and_token(user)

        subject = 'Account verification mail'

        send_verification_email.delay(
            subject, uid, token, valid_until,  user.username, user.email, otp)

        Link.objects.create(
            user=user, uid=uid,  token=token, otp=otp, valid_until=valid_until)

        return Response({"message": 'Your account has been successfully created. Please check your email to verify your account.'}, status=status.HTTP_201_CREATED)
