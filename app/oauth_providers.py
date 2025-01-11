import os
from app import oauth

googleOauth = oauth.register(
    name="auth0",
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.getenv('GOOGLE_CLIENT_DOMAIN')}/.well-known/openid-configuration'
)
