# -*- coding: utf-8 -*-

"""
Movie API Authentication, views and utilities:
1. Basic Authentication.
2. JSON Web Token Based Authentication.
"""

import jwt
import base64
from datetime import timedelta

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from moviexceptions.generic import BasicAuthException, JWTAuthException
from config import movieconf


def get_token(request):
    username, password = request.username, request.password  # make sure BasicAuthMixin is mixed-in to the view.
    current_dtm = now()
    payload = {
        'username': username,
        'password': password,
        'iat': current_dtm,
        'exp': current_dtm + timedelta(seconds=movieconf.JWT_EXPIRY_TIME),
    }
    token = jwt.encode(payload, movieconf.JWT_SECRET, algorithm=movieconf.JWT_ALGORITHM)
    if isinstance(token, bytes):
        return token.decode('utf-8')
    return token


class BasicAuthMixin(View):
    """
    Add this mixin to the views where basic authentication is needed.
    This mixin is sufficient to raise appropriate exception with proper
    HTTP response code if the basic authentication fails. Raise 'BasicAuthException'
    with ('error message', error_code)
    """

    www_basic_realm = 'movie_basic_authentication'

    def basic_authenticate(self, request):
        use_auth = True
        # Getting the auth header string from request's META dictionary.
        auth = request.META.get('HTTP_AUTHORIZATION')
        if not auth or not auth.startswith('Basic'):
            # There is no auth header.
            # see if the credentials are passed as request's GET params
            username, password = request.GET.get('username') or None, request.GET.get('password') or None

            if username is None or password is None:
                raise BasicAuthException('Invalid Basic Authentication Body', 401)
            # Do not use auth to extract the username and password
            # as it was extracted from query-params.
            use_auth = False

        try:
            if use_auth:
                # An example string for basic auth can be 'Basic a!asdfAsDADFAS1sd1234&'
                basic_auth_token = auth.split('Basic ')[1]
                decoded_token = base64.b64decode(basic_auth_token)
                # Supporting for both Python 2 and Python 3.
                if isinstance(decoded_token, bytes):  # Python 3: decoded token is python bytes object
                    username, password = decoded_token.decode('utf-8').split(':')
                else:
                    username, password = decoded_token.split(':')
            if username == movieconf.MOVIE_BASIC_AUTH['username'] and password == movieconf.MOVIE_BASIC_AUTH['password']:
                return username, password
            raise BasicAuthException('Invalid Credentials', 403)
        except (ValueError, TypeError, IndexError):  # Error decoding the token using base64
            raise BasicAuthException('Token Can Not Be Decoded', 403)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        try:
            if getattr(request, 'username', None) != movieconf.GUEST_USER:
                username, password = self.basic_authenticate(request)
                request.username, request.password = username, password  # we'll use this to create JSON Web Token.
        except BasicAuthException as err:
            response = JsonResponse({
                'status': err.status_code,
                'message': err.message
            }, status=err.status_code, content_type='application/json')
            if err.status_code == 401:  # As per W3 standards, the response must include WWW-Authenticate header.
                response['WWW-Authenticate'] = 'Basic realm="{0}"'.format(self.www_basic_realm)
            return response
        return super(BasicAuthMixin, self).dispatch(request, *args, **kwargs)


class JWTAuthMixin(View):
    """
    Add this mixin to the views where JWT based authentication is required.
    Token must be provided either in query_params or the request's Authorization Header:
    A. Query Param: the key should be passed as 'token'.
        For Example: ...&token=<jwt.based.token..>
    B. Request Authorization Header: Include the token in Auth Header.
        For Example: Authorization: Bearer <jwt.based.token..>
    """

    www_token_realm = 'movie_jwt_authentication'

    def get_token(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION') or ''
        if not auth or not auth.startswith('Bearer'):
            # looks like there is no auth token in Auth Header. Try to get it from GET query param.
            return request.GET.get('token')
        return auth.split('Bearer ')[1]

    def jwt_authenticate(self, request):
        try:
            token = self.get_token(request)  # getting token either from request's Auth Header or GET query Parameter.
            if not token:
                raise JWTAuthException('No JSONWebToken Provided', 401)
            payload = jwt.decode(token, movieconf.JWT_SECRET, algorithms=movieconf.JWT_ALGORITHM)
            username, password = payload.get('username'), payload.get('password')
            if username == movieconf.MOVIE_BASIC_AUTH['username'] and password == movieconf.MOVIE_BASIC_AUTH['password']:
                return username, password
            raise JWTAuthException('Invalid JSONWebToken Credentials', 403)
        except IndexError:
            raise JWTAuthException('Empty JSONWebToken Provided', 403)
        except jwt.ExpiredSignature:
            raise JWTAuthException('JSONWebToken Session Has Expired', 403)
        except jwt.DecodeError:
            raise JWTAuthException('JSONWebToken Can Not BE Decoded', 401)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        try:
            if getattr(request, 'username', None) != movieconf.GUEST_USER:
                request.username, request.password = self.jwt_authenticate(request)
        except JWTAuthException as err:
            response = JsonResponse({
                'status': err.status_code,
                'message': err.message
            }, status=err.status_code, content_type='application/json')
            if err.status_code == 401:  # As per W3 standards, the response must include WWW-Authenticate header.
                response['WWW-Authenticate'] = 'Bearer realm="{0}"'.format(self.www_token_realm)
            return response
        return super(JWTAuthMixin, self).dispatch(request, *args, **kwargs)


class AllowGETMixin(View):
    """
    Include this mixin to the views where 'GET' method doesn't require any kind of authentication.
    But other methods like 'POST', 'PUT', 'DELETE', 'PATCH' etc requires some sort of authentication.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            request.username = movieconf.GUEST_USER
        return super(AllowGETMixin, self).dispatch(request, *args, **kwargs)


class GetJWT(BasicAuthMixin, View):
    """
    This view can be used to get the jwt token using username and password passed in post body or in query params.
    Example using requests module:
    res = requests.get('www.example.com/auth', auth=('<username>', '<password>'))
    Note: Make sure that this view contains the BasicAuthMixin.
          Please check the mixin for more details.
    """

    def get(self, request):
        token = get_token(request)
        return JsonResponse({'username': request.username, 'token': token}, status=200, content_type='application/json')

    def post(self, request):
        token = get_token(request)
        return JsonResponse({'username': request.username, 'token': token}, status=200, content_type='application/json')

