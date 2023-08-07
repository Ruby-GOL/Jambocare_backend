from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('dialogues', DialogModelViewSet, basename='dialogues')
router.register('messages', MessageModelViewSet, basename='messages')

urlpatterns = [
    path('api/', include(router.urls)),
]