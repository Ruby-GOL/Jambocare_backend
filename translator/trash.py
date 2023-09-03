from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from .speech_to_text import *
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from .models import Translation
from .serializers import TranslationSerializer

class TranslationViewSet(viewsets.ModelViewSet):
    serializer_class = TranslationSerializer
    queryset = Translation.objects.all()

    def create(self, request):
        # Get the input text and selected languages from the request data
        text = request.data.get('text')
        source_language_code = request.data.get('source_language')
        target_language_code = request.data.get('target_language')

        # Load the NLLB model and tokenizer for the target language
        model_name = f'Helsinki-NLP/opus-mt-{target_language_code}-en'
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Encode the input text
        inputs = tokenizer(text, return_tensors='pt')

        # Transcribe the audio file
        audio_path = os.path.join(settings.MEDIA_ROOT, 'audio.wav')
        if not default_storage.exists(audio_path):
            return Response({'error': 'Audio file not found'}, status=status.HTTP_404_NOT_FOUND)
        transcription = transcribe_audio(audio_path)

        # Translate the input text
        outputs = model.generate(**inputs)
        translation = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Create a new Translation object with the input text, transcription, translation, and selected languages
        translation_obj = Translation.objects.create(
            text=text,
            transcription=transcription,
            translation=translation,
            source_language_code=source_language_code,
            target_language_code=target_language_code,
        )

        # Serialize the Translation object and return it as JSON response
        serializer = TranslationSerializer(translation_obj)
        return Response(serializer.data)
    
from rest_framework import viewsets, status
from rest_framework.response import Response
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from django.conf import settings
import os

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

class TranslateViewSet(viewsets.ViewSet):
    def create(self, request):
        # Get the selected source and target language codes from the request
        source_language_code = request.data.get('source_language_code')
        target_language_code = request.data.get('target_language_code')

        # Check if the selected language codes are in the supported list
        if not (source_language_code, _) in LANGUAGES or not (target_language_code, _) in LANGUAGES:
            return Response({'error': 'Invalid source or target language code'}, status=status.HTTP_400_BAD_REQUEST)

        audio_path = os.path.join(settings.MEDIA_ROOT, 'audio.wav')

        if not default_storage.exists(audio_path):
            return Response({'error': 'Audio file not found'}, status=status.HTTP_404_NOT_FOUND)

        transcription = transcribe_audio(audio_path)

        # Translate the transcription from source language to target language
        translation = translate_text(transcription, source_language_code, target_language_code)

        return Response({'translation': translation}, status=status.HTTP_200_OK)

    
class RecordView(viewsets.ViewSet): 
    
    def create(self, request):
 
        filename = "audio.wav"
        record_audio_manual(filename)

        # Define the path where the audio file will be saved in the media root
        audio_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Delete the existing audio file if it exists
        if default_storage.exists(audio_path):
            default_storage.delete(audio_path)


        # Save the recorded audio to the media directory using default_storage
        with open(filename, "rb") as audio_file:
            default_storage.save(audio_path, ContentFile(audio_file.read()))

        # Generate the URL for the saved audio file
        audio_url = default_storage.url(audio_path)

        return Response({'audio_url': audio_url}, status=status.HTTP_201_CREATED)

class PlayView(viewsets.ViewSet):

    def create(self, request):
     
        audio_path = os.path.join(settings.MEDIA_ROOT, 'audio.wav')

        if not default_storage.exists(audio_path):
            return Response({'error': 'Audio file not found'}, status=status.HTTP_404_NOT_FOUND)

        play_audio(audio_path)

        return Response({'message': 'Audio played successfully'}, status=status.HTTP_200_OK)

class TranscribeView(viewsets.ViewSet): 

    def create(self, request):
     
        audio_path = os.path.join(settings.MEDIA_ROOT, 'audio.wav')

        if not default_storage.exists(audio_path):
            return Response({'error': 'Audio file not found'}, status=status.HTTP_404_NOT_FOUND)

        transcription = transcribe_audio(audio_path)

        return Response({'transcription': transcription}, status=status.HTTP_200_OK)


class SaveView(viewsets.ViewSet):
    
    def create(self, request):
     
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

def translator(request):
    if request.method == 'POST':
        source_language_code = request.POST.get('source_language_code')
        target_language_code = request.POST.get('target_language_code')

        # Check if source and target languages are valid (similar to what we discussed earlier)
        if not any(lang_tuple[0] == source_language_code for lang_tuple in LANGUAGES) or not any(lang_tuple[0] == target_language_code for lang_tuple in LANGUAGES):
            return render(request, 'translate.html', {'error': 'Invalid source or target language code'})

        # Record audio and perform other operations as needed
        filename = "audio.wav"
        record_audio(filename)
        audio_path = os.path.join(settings.MEDIA_ROOT, filename)
        transcription = transcribe_audio(audio_path)
        translation = translate_text(transcription, target_language_code)

        return render(request, 'translate.html', {'source_language_code': source_language_code,
                                                  'target_language_code': target_language_code,
                                                  'transcription': transcription,
                                                  'translation': translation})

    return render(request, 'translate.html')
