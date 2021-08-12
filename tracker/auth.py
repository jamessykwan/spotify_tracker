import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = '670c083902ee4f6e9ded059a85e9dc6d'
CLIENT_SECRET = '711293c9db644ac1b8adbb9ed0cf4125'
SPOTIFY_AUTHORIZE = 'https://accounts.spotify.com/authorize'
REDIRECT_URL = 'http://127.0.0.1:8000/'

SCOPES = 'user-library-read'

auth_url = SPOTIFY_AUTHORIZE #Add base auth url
auth_url += '?client_id=' + CLIENT_ID #Add client ID
auth_url += '&response_type=code'
auth_url += '&redirect_uri=' + REDIRECT_URL
auth_url += '&show_dialog=true'
auth_url += '&scope=' + SCOPES

print(auth_url)

def getCode():
    return