from django import forms
from .models import Album, Track

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'artist', 'genre', 'album', 'audio_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}),
            'artist': forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}),
            'genre': forms.TextInput(attrs={'class': 'form-control bg-dark text-white'}),
            'album': forms.Select(attrs={'class': 'form-select bg-dark text-white'}),
            'audio_file': forms.ClearableFileInput(attrs={'class': 'form-control bg-dark text-white'}),
        }

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'artist', 'cover']