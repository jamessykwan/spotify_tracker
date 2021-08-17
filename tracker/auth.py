import spotipy
from spotipy.oauth2 import SpotifyOAuth
from requests import Request, post


CLIENT_ID = '670c083902ee4f6e9ded059a85e9dc6d'
CLIENT_SECRET = '711293c9db644ac1b8adbb9ed0cf4125'
SPOTIFY_AUTHORIZE = 'https://accounts.spotify.com/authorize'
REDIRECT_URL = 'http://127.0.0.1:8000/'

SCOPES = 'playlist-read-private'

auth_url = SPOTIFY_AUTHORIZE #Add base auth url
auth_url += '?client_id=' + CLIENT_ID #Add client ID
auth_url += '&response_type=code'
auth_url += '&redirect_uri=' + REDIRECT_URL
auth_url += '&show_dialog=true'
auth_url += '&scope=' + SCOPES

def create_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=auth_url,
        scope=SCOPES
    )

def get_tokens(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token',data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URL,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token-type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')