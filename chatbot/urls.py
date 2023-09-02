from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('dialogues', DialogModelViewSet, basename='dialogues')
router.register('messages', MessageModelViewSet, basename='messages')

urlpatterns = [
    path('api/', include(router.urls)),
    path('record/', record_audio_api, name='record_audio_api'),
    path('play/', play_audio_api, name='play_audio_api'),
    path('transcribe/', transcribe_audio_api, name='transcribe_audio_api'),
    path('save/', save_text_as_audio_api, name='save_text_as_audio_api'),

]