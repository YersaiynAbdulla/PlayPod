from django.db import models
from django.contrib.auth.models import User

class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='covers/')

    def __str__(self):
        return self.title

class Track(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    audio_file = models.FileField(upload_to='tracks/')
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name='favorite_tracks', blank=True)
    duration = models.CharField(max_length=8, blank=True, null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.audio_file:
            try:
                from mutagen import File
                audio = File(self.audio_file)
                if audio and audio.info.length:
                    minutes = int(audio.info.length // 60)
                    seconds = int(audio.info.length % 60)
                    self.duration = f"{minutes}:{seconds:02d}"
            except Exception as e:
                print(f"Не удалось извлечь длительность: {e}")
        super().save(*args, **kwargs)
