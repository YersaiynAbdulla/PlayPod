from django.urls import path
from . import views

urlpatterns = [
    path('', views.track_list, name='track_list'),
    path('track/<int:pk>/', views.track_detail, name='track_detail'),
    path('favorite/<int:pk>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.favorite_tracks, name='favorite_tracks'),
    path('albums/', views.album_list, name='album_list'),
    path('albums/<int:pk>/', views.album_detail, name='album_detail'),
    path('tracks/add/', views.track_add, name='track_add'),
    path('albums/add/', views.album_add, name='album_add'),
    path('track/<int:pk>/edit/', views.track_edit, name='track_edit'),
    path('track/<int:pk>/delete/', views.track_delete, name='track_delete'),
    path('track/<int:pk>/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('albums/<int:pk>/edit/', views.album_edit, name='album_edit'),
    path('albums/<int:pk>/delete/', views.album_delete, name='album_delete'),
    path('tracks/<int:pk>/json/', views.track_json, name='track_json'),
]
