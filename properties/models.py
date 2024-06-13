from django.db import models
from authentication.models import User


class Property(models.Model):
    merchant = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = 'properties'

    def __str__(self):
        return f'{self.merchant.username} {self.name}'


def property_photo_upload_path(instance, filename):
   return f"property_photos/{instance.property.id}/{filename}"


class PropertyPhoto(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to=property_photo_upload_path)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f'Photo of {self.property.name}'
