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


class OtpVerifyView(APIView):

    def get(self, request, uid, token):
        user, verify_otp = checkuidtoken(uid, token)
        if not (user and verify_otp):
            return Response({'message': "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Good to go.'}, status=status.HTTP_200_OK)

    def post(self, request, uid, token):
        user, verify_otp = checkuidtoken(uid, token)
        if not (user and verify_otp):
            return Response({'message': "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)

        if not verify_otp.valid_until >= timezone.now():
            return Response({"message": 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserOtpVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data['otp']

        if verify_otp.otp == otp:
            user.is_verified = True
            user.save()
            verify_otp.delete()
            pos = 'merchant' if user.is_merchant else 'user'
            return Response({'message': 'User successfully verified', 'role': pos}, status=status.HTTP_200_OK)
        else:
            return Response({"message": 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


class ResendOtpView(APIView):
    def get(self, request, uid, token):
        user, verify_otp = checkuidtoken(uid, token)
        if not (user and verify_otp):
            return Response({'message': "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)

        otp, valid_until = generate_otp_and_validity()

        subject = 'Account verification mail'

        send_verification_email.delay(
            subject, uid, token, valid_until,  user.username, user.email, otp)

        verify_otp.otp = otp
        verify_otp.valid_until = valid_until
        verify_otp.save()
        return Response({"message": 'OTP successfully resent. Please check your email.'}, status=status.HTTP_200_OK)
