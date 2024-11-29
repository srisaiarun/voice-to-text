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
    file_path = fs.url(filename)  # This gives the URL, but we need the actual file path

    # Use the actual path for processing
    full_file_path = Path(settings.MEDIA_ROOT) / filename  # Fixing the path construction

    # Initialize recognizer class (for recognizing the speech)
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(str(full_file_path)) as source:  # Convert path to string
            audio_data = recognizer.record(source)
            # Transcribe audio using Google's API
            transcription = recognizer.recognize_google(audio_data)
            return transcription
    except Exception as e:
        return f"Error transcribing audio: {str(e)}"

def upload_audio(request):
    if request.method == 'POST' and request.FILES.get('file'):  # Ensure the file key exists
        audio_file = request.FILES['file']
        
        # Call the transcription function
        transcription = transcribe_audio(audio_file)
        
        # Render the template with the transcription result
        return render(request, 'transcription/upload.html', {'output': transcription})

    return render(request, 'transcription/upload.html', {'form': AudioFileForm()})
