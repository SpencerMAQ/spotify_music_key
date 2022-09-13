from .models import SpotifyToken

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
    print(sp_token_django_obj)
