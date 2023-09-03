from rest_framework import serializers
from .models import Translation

class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['id', 'text', 'transcription', 'translation', 'source_language_code', 'target_language_code']