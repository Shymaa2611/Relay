import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'Project.settings'  
django.setup()
from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token  

@database_sync_to_async
def get_user_from_authToken(auth_token_key):
    try:
        token = Token.objects.get(key=auth_token_key)
        print(f"Token found: {auth_token_key} for user: {token.user}")
        return token.user
    except Token.DoesNotExist:
        print(f"Token not found: {auth_token_key}")
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        print("Scope:", scope)  
        headers = {key.lower(): value for key, value in dict(scope["headers"]).items()}  
        print("Headers:", headers)
        print("Query String:", scope["query_string"])  

        auth_token_key = None
        if b"token" in headers:  
            auth_token_key = headers[b"token"].decode()
            print(f"authToken found in headers: {auth_token_key}")
        else:
            print("authToken not found in headers")

        if not auth_token_key:
            query_params = dict(parse_qs(scope["query_string"].decode()))
            auth_token_key = query_params.get("token", [None])[0]
            if auth_token_key:
                print(f"authToken found in query params: {auth_token_key}")
            else:
                print("authToken not found in query params either")
        scope["user"] = await get_user_from_authToken(auth_token_key)

        return await super().__call__(scope, receive, send)
