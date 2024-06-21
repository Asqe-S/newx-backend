from rest_framework import generics
from django.core.files.storage import default_storage
from userprofile.serializers import *
from userprofile.utils import UserAuth
from properties.models import *


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [UserAuth]
    serializer_class = UserDataSerializer

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        user = instance
        if user.profile_picture:
            default_storage.delete(user.profile_picture.path)
        if user.is_merchant:
            properties = Property.objects.filter(merchant=user)
            for property in properties:
                property_photos = PropertyPhoto.objects.filter(
                    property=property)
                for property_photo in property_photos:
                    if property_photo.photo:
                        default_storage.delete(property_photo.photo.path)
                        property_photo.delete()
                property.delete()
        # user.delete()
