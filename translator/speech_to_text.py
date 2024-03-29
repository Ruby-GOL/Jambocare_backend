import openai
import os
#import sounddevice as sd
import audiofile as af
from scipy.io.wavfile import write
from gtts import gTTS
import audioread

import multiprocessing
import pyttsx3
import keyboard
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

openai.api_key = os.getenv('OPENAI_API_KEY')


# # Define global variables for the model and huggingface api token

# api_token = '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'
# model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M", use_auth_token=api_token)

# def translate_text(text, source_language_code, target_language_code):
#     # Load the Hugging Face tokenizer
#     tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M", use_auth_token=api_token, src_lang=source_language_code)

#     # Prepare the input text for translation
#     inputs = tokenizer(text, return_tensors="pt")

#     # Translate the text to the desired language
#     translated_tokens = model.generate(
#          **inputs, forced_bos_token_id=tokenizer.lang_code_to_id[target_language_code], max_length=30
#     )

#     # Decode the translated tokens into text
#     translation = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

#     return translation

def transcribe_audio(filename):
    audio_file= open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    audio_file.close()
    return transcript

# def transcribe_audio(filename):
#     transcriber = pipeline(model="openai/whisper-large")
#     result = transcriber(filename)

#     if result and 'text' in result[0]:
#         transcription = result[0]['text']
#         return transcription
#     else:
#         return "Transcription not available."


def say(text):
		p = multiprocessing.Process(target=pyttsx3.speak, args=(text,))
		p.start()
		while p.is_alive():
			if keyboard.is_pressed('enter'):
				p.terminate()
			else:
				continue
		p.join()


def save_text_as_audio(text, audio_filename):
    myobj = gTTS(text=text, lang='en', slow=False)  
    myobj.save(audio_filename)
	


# def play_audio(filename):
#     with audioread.audio_open(filename) as f:
#         sr = f.samplerate
#         channels = f.channels

#     if channels == 1:
#         mono_signal, _ = af.read(filename)
#         sd.play(mono_signal, sr, channels=1)
#     elif channels == 2:
#         stereo_signal, _ = af.read(filename)
#         sd.play(stereo_signal, sr, channels=2)
#     else:
#         # Handle unsupported number of channels
#         raise ValueError("Unsupported number of audio channels in the file.")

#     sd.wait()


# def record_audio(filename, sec, sr = 44100):
#     audio = sd.rec(int(sec * sr), samplerate=sr, channels=2, blocking=False)
#     sd.wait()
#     write(filename, sr, audio)

# def record_audio_manual(filename, sr = 44100):
#     input("  ** Press enter to start recording **")
#     audio = sd.rec(int(10 * sr), samplerate=sr, channels=2)
#     input("  ** Press enter to stop recording **")
#     sd.stop()
#     write(filename, sr, audio)

# def play_audio(filename):
#     signal, sr = af.read(filename)
#     sd.play(signal, sr)