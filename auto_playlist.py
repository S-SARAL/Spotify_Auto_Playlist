import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import logging
from fuzzywuzzy import fuzz
from tracks import tracks_to_search, playlist_name, playlist_description, playlist_public

# Logging ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# .env dosyasını yükle
load_dotenv()

# Spotify kimlik bilgilerini al
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

# Spotify API yetkilendirme
scope = 'playlist-modify-private playlist-modify-public playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Kullanıcı ID'sini al
user_id = sp.current_user()['id']

# Şarkı URI'larını almak için fonksiyon
def get_track_uri(track_name):
    results = sp.search(q=track_name, type='track', limit=1)
    items = results['tracks']['items']
    if items:
        return items[0]['uri']
    return None

# Var olan çalma listesini bul veya yeni oluştur
def find_or_create_playlist():
    playlists = sp.current_user_playlists(limit=50)
    for playlist in playlists['items']:
        if playlist['name'].strip().lower() == playlist_name.strip().lower():
            return playlist['id']
    new_playlist = sp.user_playlist_create(user_id, playlist_name, public=playlist_public, description=playlist_description)
    return new_playlist['id']

# Çalma listesini güncelle
playlist_id = find_or_create_playlist()
track_uris = [get_track_uri(track) for track in tracks_to_search if get_track_uri(track)]
sp.playlist_replace_items(playlist_id, track_uris)

logging.info(f"Playlist '{playlist_name}' başarıyla güncellendi!")
