from django.urls import path, include
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("translator/", record, name="record"),
    path("record/detail/<uuid:id>/", record_detail, name="record_detail"),
    path('translate-audio/', translate_audio, name='translate_audio'),
    # To dELETE
    path('translate/', record_audio, name='record_audio'),
    path('translat/',translator, name='translator'),
    path('save_audio/', save_audio, name='save_audio'),
]
