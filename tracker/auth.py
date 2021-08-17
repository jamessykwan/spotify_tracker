from requests.sessions import session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.utils import timezone
from datetime import timedelta
from requests import Request, post
from .models import SpotifyToken


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

def spotify_callback(request, format=None):
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
    refresh_token = response.get('refresh_token')
    token_type = response.get('token-type')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_user_tokens(request.session.session_key, access_token, refresh_token, token_type, expires_in)

def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None

def update_user_tokens(session_id, access_token, refresh_token, token_type, expires_in):
    tokens = get_user_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token','refresh_token','expires_in','token_type'])
    else:
        tokens = SpotifyToken(user=session_id, access_token=access_token, refresh_token=refresh_token, expires_in=expires_in, token_type=token_type)
        tokens.save()

def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)
        
        return True

    return False

def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token',data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    token_type = response.get('token-type')
    expires_in = response.get('expires_in')

    update_user_tokens(session_id, access_token, refresh_token, expires_in, token_type)
