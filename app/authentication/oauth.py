from django.conf import settings
from authlib.integrations.django_client import OAuth


oauth = OAuth()


def init_oauth():
    oauth.register(
        name='google',
        server_metadata_url="""
            https://accounts.google.com/.well-known/openid-configuration""",
        client_id=settings.AUTHLIB_OAUTH_CLIENTS['google']['client_id'],
        client_secret=(
            settings.AUTHLIB_OAUTH_CLIENTS['google']['client_secret']
        ),
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
