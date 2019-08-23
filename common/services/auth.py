import json

import requests
from django.conf import settings
from django.core import exceptions

def get_token_from_auth_header(request):
    token = None
    try:
        token = request.headers['Authorization'] if request.headers['Authorization'] else None
        token = str.split(token)[1]
    except KeyError:
        pass
    return token

def get_user_from_auth_header(request):
    user = None
    token = get_token_from_auth_header(request)
    current_user_url = f'{settings.AUTH_SERVER_BASE_URL}/auth/current_user'
    r = requests.get(current_user_url, headers={
        'Authorization': f'Bearer {token}',
    })
    response = json.loads(r.text)
    print(response)
    if 'error' not in response.keys():
        user = response
    return user

def user_is_authenticated(func):
    def wrap(obj, request, *args, **kwargs):
        user = get_user_from_auth_header(request)
        if user is None:
            raise exceptions.PermissionDenied('User is not authenticated')
        return func(obj, request, *args, **kwargs)
    return wrap
