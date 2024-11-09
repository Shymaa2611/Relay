import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'Project.settings'  
django.setup()
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs

User = get_user_model()

@database_sync_to_async
def get_user_from_token(token_key):
    try:
        access_token = AccessToken(token_key)
        user_id = access_token['user_id']
        return User.objects.get(id=user_id)
    except Exception:
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        token_key = None
        headers = dict(scope["headers"])
        if b"token" in headers:
            token_key = headers[b"token"].decode()

        if not token_key:
            token_key = dict(parse_qs(scope["query_string"].decode())).get("token", [None])[0]

        scope["user"] = await get_user_from_token(token_key)

        return await super().__call__(scope, receive, send)
