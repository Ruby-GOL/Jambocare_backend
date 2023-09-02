import environ
import rest_framework.exceptions
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .filters import MessageFilter
from .models import Dialog, Message
from .permissions import IsOwnerDialog, IsOwnerMessage
from .serializers import DialogModelSerializer, MessageModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from accounts.permissions import IsEmailConfirm

from .speech_to_text import *


User = get_user_model()

env = environ.Env()
environ.Env.read_env()
FRONTEND_URL = env('FRONTEND_URL')


class DialogModelViewSet(ModelViewSet):
    """
    ViewSet class for the Dialog model.

    This ViewSet provides CRUD functionality for Dialog objects.

    Attributes:
        queryset (QuerySet): The queryset of Dialog objects.
        serializer_class (Serializer): The serializer class for Dialog objects.
        permission_classes (list): The list of permission classes.
        http_method_names (list): The list of allowed HTTP methods.
    """

    queryset = Dialog.objects.all()
    serializer_class = DialogModelSerializer
    permission_classes = [IsOwnerDialog, IsEmailConfirm]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        """
        Get the queryset of Dialog objects.

        This method filters the queryset based on the user's ownership.

        Returns:
            QuerySet: The filtered queryset of Dialog objects.
        """

        owner_queryset = self.queryset.filter(user_id=self.request.user)
        return owner_queryset

    def destroy(self, request, *args, **kwargs):
        """
        Destroy a Dialog object.

        This method deletes the specified Dialog object and returns a success message.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response containing the success message.
        """

        item = self.get_object()
        item.delete()
        response = {
            'message': 'Dialog deletes successfully',
        }

        return Response(response, status=status.HTTP_200_OK)


class MessageModelViewSet(ModelViewSet):
    """
    ViewSet class for the Message model.

    This ViewSet provides CRUD functionality for Message objects.

    Attributes:
        queryset (QuerySet): The queryset of Message objects.
        serializer_class (Serializer): The serializer class for Message objects.
        filterset_class (FilterSet): The filterset class for Message objects.
        permission_classes (list): The list of permission classes.
        http_method_names (list): The list of allowed HTTP methods.
    """

    queryset = Message.objects.all()
    serializer_class = MessageModelSerializer
    filterset_class = MessageFilter
    permission_classes = [IsOwnerMessage, IsEmailConfirm]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        """
        Get the queryset of Message objects.

        This method filters the queryset based on the user's ownership and dialog ID.

        Returns:
            QuerySet: The filtered queryset of Message objects.
        """

        user_dialogs = Dialog.objects.filter(user_id=self.request.user)
        owner_queryset = self.queryset.filter(dialog_id__in=user_dialogs)

        dialog_id = self.request.query_params.get('dialog_id')
        if not user_dialogs.filter(id=dialog_id).exists() and dialog_id:
            raise rest_framework.exceptions.PermissionDenied(
                {
                    "errors": {
                        "details": "Available only for the owner"
                    }
                }
            )
        return owner_queryset

    def destroy(self, request, *args, **kwargs):
        """
        Destroy a Message object.

        This method deletes the specified Message object and returns a success message.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response containing the success message.
        """

        item = self.get_object()
        item.delete()
        response = {
            'message': 'Message deletes successfully',
        }

        return Response(response, status=status.HTTP_200_OK)

def record_audio_api(request):
    filename = 'output.wav'  # Set the desired filename
    record_audio_manual(filename)
    
    response_data = {
        'status': 'success',
        'message': 'Recording completed successfully.',
    }
    
    return JsonResponse(response_data)

def transcribe_audio_api(request):
    # Replace 'input.wav' with the actual filename you want to transcribe
    filename = 'output.wav'
    transcript = transcribe_audio(filename)
    
    # You can add additional data to the response if needed
    response_data = {
        'transcript': transcript,
        'status': 'success',
    }
    
    return JsonResponse(response_data)

def play_audio_api(request):
    filename = 'output.wav'
    play_audio(filename)
    
    response_data = {
        'status': 'success',
        'message': 'Audio playback initiated.',
    }
    
    return JsonResponse(response_data)

def save_text_as_audio_api(request):
    text = 'Hello, this is a test.'  # Replace with the desired text
    filename = 'test.mp3'  # Set the desired filename and format
    save_text_as_audio(text, filename)
    
    response_data = {
        'status': 'success',
        'message': 'Text saved as audio successfully.',
    }
    
    return JsonResponse(response_data)

# import openai

# # Set up the API key
# openai.api_key = "YOUR_API_KEY"

# # Load the audio file
# with open("path/to/audio/file", "rb") as audio_file:
#     audio_data = audio_file.read()

# # Transcribe the audio file
# transcription = openai.Audio.transcribe(
#     api_key=openai.api_key,
#     model="whisper-1",
#     audio=audio_data,
#     language="en-US"
# )

# # Translate the transcription to the desired language
# translation = openai.Translation.translate(
#     api_key=openai.api_key,
#     text=transcription,
#     target_language="es"
# )

# # Save the transcribed and translated text to your Django model
# my_model = MyModel.objects.create(voice_record="path/to/audio/file", transcription=transcription, translation=translation)
