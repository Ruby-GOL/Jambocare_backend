from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from .speech_to_text import *

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

class TranslateViewSet(viewsets.ViewSet):
    """
    A ViewSet class that handles the translation of audio files.

    This ViewSet provides functionality for recording audio, transcribing the audio, translating the transcription to the desired language, saving the transcribed and translated text to a file, and converting the translated text to speech.

    Attributes:
        queryset (QuerySet): The queryset of Message objects.
        serializer_class (Serializer): The serializer class for Message objects.
        filterset_class (FilterSet): The filterset class for Message objects.
        permission_classes (list): The list of permission classes.
        http_method_names (list): The list of allowed HTTP methods.
    """

    def create(self, request):
        """
        Translates an audio file to the desired language.

        This method records the audio, transcribes the audio, translates the transcription to the desired language, saves the transcribed and translated text to a file, and converts the translated text to speech.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response containing the transcription, translation, and audio file.
        """
        target_language_code = request.data.get('target_language_code')
        audio_file = request.FILES.get('audio_file')
        filename = default_storage.save(audio_file.name, ContentFile(audio_file.read()))
        audio_path = os.path.join(settings.MEDIA_ROOT, filename)
        transcription = transcribe_audio(audio_path)
        translation = translate_text(transcription, target_language_code)
        text_filename = "text.txt"
        with open(text_filename, "w") as text_file:
            text_file.write(transcription + "\n" + translation)
        audio_filename = "audio.mp3"
        save_text_as_audio(translation, audio_filename)
        return Response({'transcription': transcription, 'translation': translation, 'audio_file': audio_filename}, status=status.HTTP_200_OK)

class RecordView(viewsets.ViewSet):
    """
    A ViewSet class that handles recording audio files.

    This ViewSet provides functionality for recording audio files and returning the recorded audio file.

    Attributes:
        queryset (QuerySet): The queryset of Message objects.
        serializer_class (Serializer): The serializer class for Message objects.
        filterset_class (FilterSet): The filterset class for Message objects.
        permission_classes (list): The list of permission classes.
        http_method_names (list): The list of allowed HTTP methods.
    """

    def create(self, request):
        """
        Records an audio file.

        This method records an audio file and returns the recorded audio file.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response containing the recorded audio file.
        """
        filename = "audio.wav"
        record_audio_manual(filename)
        with open(filename, "rb") as audio_file:
            return Response(audio_file.read(), content_type="audio/wav")


class PlayView(viewsets.ViewSet):
    """
    A ViewSet class that handles playing audio files.

    This ViewSet provides functionality for playing audio files.

    Attributes:
        queryset (QuerySet): The queryset of Message objects.
        serializer_class (Serializer): The serializer class for Message objects.
        filterset_class (FilterSet): The filterset class for Message objects.
        permission_classes (list): The list of permission classes.
        http_method_names (list): The list of allowed HTTP methods.
    """

    def create(self, request):
        """
        Plays an audio file.

        This method plays an audio file.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response containing a success message.
        """
        audio_file = request.FILES.get('audio_file')
        filename = default_storage.save(audio_file.name, ContentFile(audio_file.read()))
        audio_path = os.path.join(settings.MEDIA_ROOT, filename)
        play_audio(audio_path)
        return Response({'message': 'Audio played successfully'}, status=status.HTTP_200_OK)


class TranscribeView(viewsets.ViewSet):
    """
    A ViewSet class that handles transcribing audio files.

    This ViewSet provides functionality for transcribing audio files.

    Attributes:
        queryset (QuerySet): The queryset of Message objects.
        serializer_class (Serializer): The serializer class for Message objects.
        filterset_class (FilterSet): The filterset class for Message objects.
        permission_classes (list): The list of permission classes.
        http_method_names (list): The list of allowed HTTP methods.
    """

    def create(self, request):
        """
        Transcribes an audio file.

        This method transcribes an audio file and returns the transcription.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response containing the transcription.
        """
        audio_file = request.FILES.get('audio_file')
        filename = default_storage.save(audio_file.name, ContentFile(audio_file.read()))
        audio_path = os.path.join(settings.MEDIA_ROOT, filename)
        transcription = transcribe_audio(audio_path)
        return Response({'transcription': transcription}, status=status.HTTP_200_OK)


class SaveView(viewsets.ViewSet):
    """
    A ViewSet class that handles saving transcribed and translated audio files.

    This ViewSet provides functionality for transcribing an audio file, translating the transcription to English, saving the transcribed and translated text to a file, and converting the translated text to speech.

    Attributes:
        queryset (QuerySet): The queryset of Message objects.
        serializer_class (Serializer): The serializer class for Message objects.
        filterset_class (FilterSet): The filterset class for Message objects.
        permission_classes (list): The list of permission classes.
        http_method_names (list): The list of allowed HTTP methods.
    """

    def create(self, request):
        """
        Saves transcribed and translated audio files.

        This method transcribes an audio file, translates the transcription to English, saves the transcribed and translated text to a file, and converts the translated text to speech.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response containing the transcribed and translated audio files.
        """
        audio_file = request.FILES.get('audio_file')
        filename = default_storage.save(audio_file.name, ContentFile(audio_file.read()))
        audio_path = os.path.join(settings.MEDIA_ROOT, filename)
        transcription = transcribe_audio(audio_path)
        translation = translate_text(transcription, 'en')
        text_filename = "text.txt"
        with open(text_filename, "w") as text_file:
            text_file.write(transcription + "\n" + translation)
        audio_filename = "audio.mp3"
        save_text_as_audio(translation, audio_filename)
        return Response({'message': 'Transcription and translation saved successfully', 'text_file': text_filename, 'audio_file': audio_filename}, status=status.HTTP_200_OK)


