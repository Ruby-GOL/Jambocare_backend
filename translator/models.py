from django.db import models
from rest_framework import serializers

class Translation(models.Model):
    text = models.CharField(max_length=200)
    transcription = models.CharField(max_length=200)
    translation = models.CharField(max_length=200)
    source_language_code = models.CharField(max_length=10)
    target_language_code = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.text} ({self.source_language_code} -> {self.target_language_code})'


