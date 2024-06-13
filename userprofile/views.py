from rest_framework import generics
from django.core.files.storage import default_storage
from userprofile.serializers import *
from userprofile.utils import UserAuth


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [UserAuth]
    serializer_class = UserDataSerializer

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        user = instance
        if user.profile_picture:
            default_storage.delete(user.profile_picture.path)
        # user.delete()
