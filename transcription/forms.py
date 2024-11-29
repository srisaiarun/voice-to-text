from django import forms

class AudioFileForm(forms.Form):
    file = forms.FileField(label="Upload an Audio File")
