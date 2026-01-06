import speech_recognition as sr
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from pathlib import Path
from django.shortcuts import render
from .forms import AudioFileForm

def transcribe_audio(file):
    # Save the file to disk
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    filename = fs.save(file.name, file)
    file_path = fs.url(filename)  # URL for playback in template

    # Use the actual path for processing
    full_file_path = Path(settings.MEDIA_ROOT) / filename

    # Initialize recognizer class (for recognizing the speech)
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(str(full_file_path)) as source:  # Convert path to string
            audio_data = recognizer.record(source)
            # Transcribe audio using Google's API
            transcription = recognizer.recognize_google(audio_data)
            return transcription, file_path
    except Exception as e:
        return f"Error transcribing audio: {str(e)}", file_path

def upload_audio(request):
    if request.method == 'POST' and request.FILES.get('file'):  # Ensure the file key exists
        audio_file = request.FILES['file']
        
        # Call the transcription function
        transcription, audio_url = transcribe_audio(audio_file)
        
        # Render the template with the transcription and audio URL for playback
        return render(request, 'transcription/upload.html', {'output': transcription, 'audio_url': audio_url})

    return render(request, 'transcription/upload.html', {'form': AudioFileForm()})
