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
    path('', translator, name='translator'),


]
