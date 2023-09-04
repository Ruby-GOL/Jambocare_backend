from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from .speech_to_text import *
# from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
# from .models import Translation
# from .serializers import TranslationSerializer

# List of language codes and names
LANGUAGES = [
    ("som_Latn", "Somali"),
    ("kik_Latn", "Kikuyu"),
    ("luo_Latn", "Luo"),
    ("kam_Latn", "Kamba"),
    ("zul_Latn", "Zulu"),
    ("swa_Latn", "Swahili"),
    ("fra_Latn", "French"),
    ("eng_Latn", "English"),
    ("deu_Latn", "German"),
]
@csrf_exempt
def translator(request):
    transcription = None
    translation =None

    if request.method == 'POST':
        source_language_code = request.POST.get('source_language_code')
        target_language_code = request.POST.get('target_language_code')

        if not any(lang_tuple[0] == source_language_code for lang_tuple in LANGUAGES) or not any(
                lang_tuple[0] == target_language_code for lang_tuple in LANGUAGES):
            return JsonResponse({'error': 'Invalid source or target language code'}, status=400)

        audio_path = os.path.join(settings.MEDIA_ROOT, 'audio.wav')
        if not os.path.exists(audio_path):
            return JsonResponse({'error': 'Audio file not found'}, status=404)

        transcription = transcribe_audio(audio_path)

        # # Translate the transcribed text
        # translation = translate_text(transcription, source_language_code, target_language_code)

        # return JsonResponse({'source_language_code': source_language_code,
        #                      'target_language_code': target_language_code,
        #                      'transcription': transcription,
        #                      'translation': translation})

    return render(request, 'translate.html', {'LANGUAGES': LANGUAGES, 'transcription': transcription, 'translation': translation})

@csrf_exempt
def record_audio(request):
    if request.method == 'POST':
        source_language_code = request.POST.get('source_language_code')
        target_language_code = request.POST.get('target_language_code')

        if not any(lang_tuple[0] == source_language_code for lang_tuple in LANGUAGES) or not any(
                lang_tuple[0] == target_language_code for lang_tuple in LANGUAGES):
            return JsonResponse({'error': 'Invalid source or target language code'}, status=400)
        
    return render(request, 'translate.html', {'LANGUAGES': LANGUAGES})

@csrf_exempt
def save_audio(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio')
        if audio_file:
            # Define the file name
            file_name = 'audio.wav'
            
            # Construct the full path to the audio file
            audio_path = os.path.join(settings.MEDIA_ROOT, file_name)
            
            # Delete the existing audio.wav file if it exists
            if default_storage.exists(audio_path):
                default_storage.delete(audio_path)
            
            # Save the new audio file in Django's MEDIA folder
            file_path = default_storage.save(audio_path, audio_file)

            print("Audio file saved at:", file_path)  # Add this line for debugging

            return JsonResponse({'message': 'Audio saved successfully', 'file_path': file_path})

    return JsonResponse({'error': 'Failed to save audio'},status=400)


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
        Translates an audio file.

        This method translates an audio file and returns the translated transcription.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response containing the translated transcription.
        """
        # Get the selected source and target language codes from the request
        source_language_code = request.data.get('source_language_code')
        target_language_code = request.data.get('target_language_code')

        # Check if the selected language codes are in the supported list
        if not any(lang_tuple[0] == source_language_code for lang_tuple in LANGUAGES) or not any(lang_tuple[0] == target_language_code for lang_tuple in LANGUAGES):

            return Response({'error': 'Invalid source or target language code'}, status=status.HTTP_400_BAD_REQUEST)

        audio_path = os.path.join(settings.MEDIA_ROOT, 'audio.wav')

        if not default_storage.exists(audio_path):
            return Response({'error': 'Audio file not found'}, status=status.HTTP_404_NOT_FOUND)

        transcription = transcribe_audio(audio_path)

        # Translate the transcription from source language to target language
        translation = translate_text(transcription, source_language_code, target_language_code)

        return Response({'translation': translation}, status=status.HTTP_200_OK)
    
# class RecordView(viewsets.ViewSet):
#     """
#     A ViewSet class that handles recording audio files.

#     This ViewSet provides functionality for recording audio files and returning the recorded audio file.

#     Attributes:
#         queryset (QuerySet): The queryset of Message objects.
#         serializer_class (Serializer): The serializer class for Message objects.
#         filterset_class (FilterSet): The filterset class for Message objects.
#         permission_classes (list): The list of permission classes.
#         http_method_names (list): The list of allowed HTTP methods.
#     """

    
#     def create(self, request):
#         """
#         Records an audio file.

#         This method records an audio file and saves it in the media directory as "audio.wav".
#         It overwrites the existing "audio.wav" file if it exists.
#         It returns the URL of the recorded audio file.

#         Args:
#             request (HttpRequest): The HTTP request object.

#         Returns:
#             Response: The HTTP response containing the URL of the recorded audio file.
#         """
#         filename = "audio.wav"
#         record_audio_manual(filename)

#         # Define the path where the audio file will be saved in the media root
#         audio_path = os.path.join(settings.MEDIA_ROOT, filename)

#         # Delete the existing audio file if it exists
#         if default_storage.exists(audio_path):
#             default_storage.delete(audio_path)


#         # Save the recorded audio to the media directory using default_storage
#         with open(filename, "rb") as audio_file:
#             default_storage.save(audio_path, ContentFile(audio_file.read()))

#         # Generate the URL for the saved audio file
#         audio_url = default_storage.url(audio_path)

#         return Response({'audio_url': audio_url}, status=status.HTTP_201_CREATED)

# class PlayView(viewsets.ViewSet):
#     """
#     A ViewSet class that handles playing audio files.

#     This ViewSet provides functionality for playing audio files.

#     Attributes:
#         queryset (QuerySet): The queryset of Message objects.
#         serializer_class (Serializer): The serializer class for Message objects.
#         filterset_class (FilterSet): The filterset class for Message objects.
#         permission_classes (list): The list of permission classes.
#         http_method_names (list): The list of allowed HTTP methods.
#     """

#     def create(self, request):
#         """
#         Plays an audio file.

#         This method plays an audio file and returns a success message.

#         Args:
#             request (HttpRequest): The HTTP request object.

#         Returns:
#             Response: The HTTP response containing a success message.
#         """
#         # Assuming the 'audio.wav' file is saved in the MEDIA root directory
#         audio_path = os.path.join(settings.MEDIA_ROOT, 'audio.wav')

#         if not default_storage.exists(audio_path):
#             return Response({'error': 'Audio file not found'}, status=status.HTTP_404_NOT_FOUND)

#         # Implement the play_audio function to play the 'audio.wav' file
#         play_audio(audio_path)

#         return Response({'message': 'Audio played successfully'}, status=status.HTTP_200_OK)

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
        audio_path = os.path.join(settings.MEDIA_ROOT, 'audio.wav')

        if not default_storage.exists(audio_path):
            return Response({'error': 'Audio file not found'}, status=status.HTTP_404_NOT_FOUND)

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
        # Assuming the 'audio.wav' file is saved in the MEDIA root directory
        audio_path = os.path.join(settings.MEDIA_ROOT, 'audio.wav')

        if not default_storage.exists(audio_path):
            return Response({'error': 'Audio file not found'}, status=status.HTTP_404_NOT_FOUND)

        transcription = transcribe_audio(audio_path)
        translation = translate_text(transcription, 'en')
        text_filename = "text.txt"
        audio_filename = "audio.mp3"

        # Save the transcribed and translated text to a file
        with open(text_filename, "w") as text_file:
            text_file.write(transcription + "\n" + translation)

        # Convert the translated text to speech and save it as an audio file
        save_text_as_audio(translation, audio_filename)

        return Response({
            'message': 'Transcription and translation saved successfully',
            'text_file': text_filename,
            'audio_file': audio_filename
        }, status=status.HTTP_200_OK)

