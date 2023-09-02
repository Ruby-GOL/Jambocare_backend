import openai
import sounddevice as sd
import audiofile as af
from scipy.io.wavfile import write
from gtts import gTTS
import audioread

import multiprocessing
import pyttsx3
import keyboard

def say(text):
		p = multiprocessing.Process(target=pyttsx3.speak, args=(text,))
		p.start()
		while p.is_alive():
			if keyboard.is_pressed('enter'):
				p.terminate()
			else:
				continue
		p.join()


def record_audio(filename, sec, sr = 44100):
    audio = sd.rec(int(sec * sr), samplerate=sr, channels=2, blocking=False)
    sd.wait()
    write(filename, sr, audio)

def record_audio_manual(filename, sr = 44100):
    input("  ** Press enter to start recording **")
    audio = sd.rec(int(10 * sr), samplerate=sr, channels=2)
    input("  ** Press enter to stop recording **")
    sd.stop()
    write(filename, sr, audio)

def play_audio(filename):
    signal, sr = af.read(filename)
    sd.play(signal, sr)
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

def transcribe_audio(filename):
    audio_file= open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    audio_file.close()
    return transcript

def translate_text(text, target_language_code):
    translation = openai.Translation.translate(
        api_key=openai.api_key,
        text=text,
        target_language=target_language_code
    )
    return translation

def save_text_as_audio(text, audio_filename):
    myobj = gTTS(text=text, lang='en', slow=False)  
    myobj.save(audio_filename)