from django.utils.text import slugify
from rest_framework import serializers
from properties.models import *


class PropertyPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyPhoto
        fields = ['id', 'photo']

    def update(self, instance, validated_data):
        photo = validated_data.get('photo')

        if photo:
            if instance.photo:
                instance.photo.delete()
        return super().update(instance, validated_data)


class PropertySerializer(serializers.ModelSerializer):
    photos = PropertyPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = ['id', 'city', 'state', 'name',
                  'photos', 'longitude', 'latitude']
