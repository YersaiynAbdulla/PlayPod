from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Track, Album
from .forms import AlbumForm, TrackForm

def track_detail(request, pk):
    track = get_object_or_404(Track, pk=pk)
    next_url = request.GET.get('next') or reverse('track_list')
    favorites = request.session.get('favorites', [])

    tracks = list(Track.objects.filter(album=track.album).order_by('id'))
    current_index = next((i for i, t in enumerate(tracks) if t.pk == track.pk), None)

    prev_track_url = None
    next_track_url = None

    if current_index is not None:
        if current_index > 0:
            prev_track_url = reverse('track_detail', args=[tracks[current_index - 1].pk])
        if current_index + 1 < len(tracks):
            next_track_url = reverse('track_detail', args=[tracks[current_index + 1].pk])

    return render(request, 'music/track_detail.html', {
        'track': track,
        'favorite_tracks': favorites,
        'next_url': next_url,
        'prev_track_url': prev_track_url,
        'next_track_url': next_track_url,
    })

def track_list(request):
    query = request.GET.get('q', '')
    genre = request.GET.get('genre', '')
    selected_artist = request.GET.get('artist', '')

    tracks = Track.objects.all()

    if query:
        tracks = tracks.filter(title__icontains=query) | tracks.filter(artist__icontains=query)
    if genre:
        tracks = tracks.filter(genre=genre)
    if selected_artist:
        tracks = tracks.filter(artist=selected_artist)

    genres = Track.objects.values_list('genre', flat=True).distinct()
    artists = Track.objects.values_list('artist', flat=True).distinct()

    favorites = request.session.get('favorites', [])

    return render(request, 'music/track_list.html', {
        'tracks': tracks,
        'query': query,
        'genre': genre,
        'genres': genres,
        'selected_artist': selected_artist,
        'artists': artists,
        'favorite_tracks': favorites,
    })


def add_to_favorites(request, pk):
    favorites = request.session.get('favorites', [])
    if pk not in favorites:
        favorites.append(pk)
        request.session['favorites'] = favorites
    return redirect('track_list')


def favorite_tracks(request):
    favorite_ids = request.session.get('favorites', [])
    tracks = Track.objects.filter(pk__in=favorite_ids)
    return render(request, 'music/favorite_tracks.html', {'tracks': tracks})


def album_list(request):
    albums = Album.objects.all()
    return render(request, 'music/album_list.html', {'albums': albums})

#######################################

def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)

    query = request.GET.get('q', '')
    genre = request.GET.get('genre', '')
    artist = request.GET.get('artist', '')

    tracks = Track.objects.filter(album=album)

    if query:
        tracks = tracks.filter(title__icontains=query)
    if genre:
        tracks = tracks.filter(genre=genre)
    if artist:
        tracks = tracks.filter(artist=artist)

    genres = Track.objects.values_list('genre', flat=True).distinct()
    artists = Track.objects.values_list('artist', flat=True).distinct()

    return render(request, 'music/album_detail.html', {
        'album': album,
        'tracks': tracks,
        'query': query,
        'genre': genre,
        'artist': artist,
        'genres': genres,
        'artists': artists,
    })


#####################


# def album_detail(request, pk):
#     album = get_object_or_404(Album, pk=pk)
#     return render(request, 'music/album_detail.html', {'album': album})


def track_add(request):
    if request.method == 'POST':
        form = TrackForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('track_list')
    else:
        form = TrackForm()
    return render(request, 'music/track_form.html', {'form': form, 'title': 'Добавить трек'})


def album_add(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('album_list')
    else:
        form = AlbumForm()
    return render(request, 'music/album_form.html', {'form': form, 'title': 'Добавить альбом'})


def track_edit(request, pk):
    track = get_object_or_404(Track, pk=pk)
    next_url = request.GET.get('next') or reverse('track_list')

    if request.method == 'POST':
        form = TrackForm(request.POST, request.FILES, instance=track)
        if form.is_valid():
            form.save()
            return redirect('track_list')
    else:
        form = TrackForm(instance=track)
    return render(request, 'music/track_form.html', {'form': form, 'title': 'Редактировать трек', 'next_url': next_url})


def track_delete(request, pk):
    track = get_object_or_404(Track, pk=pk)
    if request.method == 'POST':
        track.delete()
        return redirect('track_list')
    return render(request, 'music/track_confirm_delete.html', {'track': track})


def toggle_favorite(request, pk):
    favorites = request.session.get('favorites', [])
    if pk in favorites:
        favorites.remove(pk)
    else:
        favorites.append(pk)
    request.session['favorites'] = favorites
    return redirect(request.META.get('HTTP_REFERER', 'track_list'))


def album_edit(request, pk):
    album = get_object_or_404(Album, pk=pk)
    next_url = request.GET.get('next') or reverse('album_list')
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            return redirect(next_url)
    else:
        form = AlbumForm(instance=album)
    return render(request, 'music/album_form.html', {'form': form, 'title': 'Редактировать альбом', 'next_url': next_url})


def album_delete(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':
        album.delete()
        return redirect('album_list')
    return render(request, 'music/album_confirm_delete.html', {'album': album})


def track_json(request, pk):
    track = get_object_or_404(Track, pk=pk)
    return JsonResponse({'audio_url': track.audio.url})
