from django.urls import path
from rest_framework.routers import DefaultRouter
from properties.views import *

router = DefaultRouter()
router.register(r'', PropertiesViewSet, basename='property_crud')

urlpatterns = [
    path('property-photo/<int:id>/', PropertyPhotoView.as_view())
]

urlpatterns += router.urls
