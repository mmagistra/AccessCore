import jwt
from django.conf import settings

from apps.custom_auth.models import CustomUser


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            try:
                token = auth_header[7:]
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                email = payload['email']
                request.email = email
            except (jwt.ExpiredSignatureError, jwt.DecodeError, CustomUser.DoesNotExist):
                request.email = None
        else:
            request.email = None
        response = self.get_response(request)
        return response
