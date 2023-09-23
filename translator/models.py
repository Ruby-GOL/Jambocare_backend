from django.db import models
import uuid
from django.urls.base import reverse

class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voice_record = models.FileField(upload_to="records")
    language = models.CharField(max_length=50, null=True, blank=True)


    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("record_detail", kwargs={"id": str(self.id)})

class Translation(models.Model):
    text = models.CharField(max_length=200)
    transcription = models.CharField(max_length=200)
    translation = models.CharField(max_length=200)
    source_language_code = models.CharField(max_length=10)
    target_language_code = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.text} ({self.source_language_code} -> {self.target_language_code})'


