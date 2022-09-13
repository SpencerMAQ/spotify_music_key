import time
from spotipy.oauth2 import SpotifyOAuth

from .models import SpotifyToken
from ._secret_info import CLIENT_ID, CLIENT_SECRET

# https://youtu.be/rYDDWVuv-kI?t=1898
def get_user_tokens(session_id):
    """
    Gets a django Object instant if the spotify token
    if it exists, otherwise return None
    """
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None


def update_or_create_user_tokens(session_id, access_token, expires_in, expires_at, refresh_token):
    """
    updates or creates a new token based on the user/session_id
    """
    sp_token_django_obj = get_user_tokens(session_id=session_id)

    # TODO: make this more efficient?
    if sp_token_django_obj:
        sp_token_django_obj.access_token = access_token
        sp_token_django_obj.expires_in = expires_in
        sp_token_django_obj.expires_at = expires_at
        sp_token_django_obj.refresh_token = refresh_token
        sp_token_django_obj.save(update_fields = ['access_token', 'expires_in', 'expires_at','refresh_token'])
    else:
        sp_token_django_obj = SpotifyToken(
            user=session_id,
            access_token=access_token,
            expires_in=expires_in,
            expires_at=expires_at,
            refresh_token=refresh_token
        )
        sp_token_django_obj.save()
    # print(sp_token_django_obj)


def is_spotify_token_still_valid(session_id) -> bool:
    """
    Only for checking if an existing token is still valid
    NOT for generating a new token

    Will refresh token if expired
    """
    sp_token_django_obj = get_user_tokens(session_id=session_id)
    if sp_token_django_obj:
        now = int(time.time())
        expires_at = sp_token_django_obj.expires_at
        if expires_at - now <= 60:
            # refresh_spotify_token(refresh_token=sp_token_django_obj.refresh_token)
            return False
        else:
            return True

    return False


def refresh_spotify_token(session_id):
    """
    Only use if there is already an existing token but has expired
    Don't use if the user hasn't logged-in in the first place
    """
    sp_token_django_obj = get_user_tokens(session_id=session_id)
    refresh_token = sp_token_django_obj.refresh_token

    sp_oauth = create_spotify_oauth()
    new_sp_token_dict: dict = sp_oauth.refresh_access_token(refresh_token=refresh_token)

    update_or_create_user_tokens(session_id=session_id,
                                 access_token=new_sp_token_dict.get('access_token'),
                                 expires_in=new_sp_token_dict.get('expires_in'),
                                 expires_at=new_sp_token_dict.get('expires_at'),
                                 refresh_token=new_sp_token_dict.get('refresh_token')
                                 )


def logout_and_delete_spotify_tokens(session_id = None):
    """
    Delete objects from a specified user/session ID
    If no session ID is specified, then delete all tokens from the DB
    """
    # TODO: check the last logged in of each session periodically,
    # if a session hasn't logged-in in a week, delete them from DB
    if session_id:
        user_tokens = SpotifyToken.objects.filter(user=session_id)
    else:
        user_tokens = SpotifyToken.objects.all()
    user_tokens.delete()


def create_spotify_oauth():
    """
    Creates a spotipy.oauth2 Oauth object
        Can be used to create a spotify player, with which you can query current playing songs, etc.
    """
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri='http://127.0.0.1:8000/spotify_temp_redirect', # TODO: don't hardcode
        scope=['user-read-currently-playing', 'user-modify-playback-state'],
    )
