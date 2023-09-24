from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'translate', TranslateViewSet, basename='translate')
# router.register(r'record', RecordView, basename='record')
# router.register(r'play', PlayView, basename='play')
router.register(r'transcribe', TranscribeView, basename='transcribe')
router.register(r'save', SaveView, basename='save')

urlpatterns = [
    path('api/', include(router.urls)),    
    path("", record, name="record"),
    path("record/detail/<uuid:id>/", record_detail, name="record_detail"),
    path('translate-audio/', translate_audio, name='translate_audio'),
    # To dELETE
    path('translate/', record_audio, name='record_audio'),
    path('translator/',translator, name='translator'),
    path('save_audio/', save_audio, name='save_audio'),



]
