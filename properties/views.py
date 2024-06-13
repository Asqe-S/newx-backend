from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet

from properties.models import *
from properties.serializers import *
from userprofile.utils import MerchantAuth
from django.core.files.storage import default_storage


class PropertiesViewSet(ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [MerchantAuth]
    lookup_field = 'id'

    def get_queryset(self):
        return Property.objects.filter(merchant=self.request.user)

    def perform_create(self, serializer):
        serializer.save(merchant=self.request.user)

    def perform_destroy(self, instance):
        properties_photo = PropertyPhoto.objects.filter(property=instance)
        for property_photo in properties_photo:
            if property_photo.photo:
                default_storage.delete(property_photo.photo.path)
            property_photo.delete()
        instance.delete()


class PropertyPhotoView(RetrieveUpdateDestroyAPIView, CreateAPIView):
    permission_classes = [MerchantAuth]
    serializer_class = PropertyPhotoSerializer
    lookup_field = 'id'
    queryset = PropertyPhoto.objects.all()

    def perform_create(self, serializer):
        property_id = self.kwargs.get('id')
        property = get_object_or_404(Property, id=property_id)
        serializer.save(property=property)

    def perform_destroy(self, instance):
        default_storage.delete(instance.photo.path)
        instance.delete()
