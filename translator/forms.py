from django import forms

class AudioForm(forms.Form):
    audio = forms.FileField(label='Upload an audio file')
