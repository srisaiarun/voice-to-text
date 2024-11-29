from django.db import models

class AudioFile(models.Model):
    file = models.FileField(upload_to='audio_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Audio File {self.id}'
