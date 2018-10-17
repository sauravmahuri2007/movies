# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.utils.encoding import smart_str
from django.db.models import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.views.generic import View

from .apps import MovieApp
from utils.movieutils import add_movie, get_request_body, search_movie
from utils.auth import JWTAuthMixin, AllowGETMixin
from utils.authorization import APIAuthorizationMixin
from utils.validation import RequestValidationMixin
from moviexceptions.generic import MovieAlreadyExists


class PingAPI(View):
    """
    A simple ping-pong API to get the server running status!
    """

    def get(self, request, *args, **kwargs):
        return JsonResponse('Pong!', status=200, safe=False)


class SearchAPI(View):
    """
    Searches the movies by title, release_date, ratings etc.
    A simple search example using query-params in a web-browser:
    http://www.example.com/search?title='Lord of the rings'
    """

    def get(self, request, *args, **kwargs):
        search_params = get_request_body(request)
        try:
            result = search_movie(search_params) # returns a list of dictionary
        except ValidationError as err:
            return JsonResponse(smart_str(err), status=400, safe=False)
        except Exception:
            return JsonResponse({
                'status': 500, 'error': 'Server Error! Something Went Slightly Wrong!!'}, status=500, safe=False)
        return JsonResponse(result, status=200, safe=False)


class MovieAPI(AllowGETMixin, JWTAuthMixin, APIAuthorizationMixin, RequestValidationMixin, View):
    """
    RESTFul implementation of adding/editing/deleting/getting movies from the DB in JSON format.
    AllowGETMixin: Include this mixin when GET method doesn't require any kind of authentication.
        Make sure that this appears as the 1st mixins in class declaration.
    JWTAuthMixin: Include this mixin for JSONWebToken based authentication for the APIs.
    """

    def get(self, request, *args, **kwargs):
        # getting the movieid either from the query-params or from request URL
        movieid = request.GET.get('movieid') or kwargs.get('movieid')
        try:
            movie_obj = MovieApp(movieid)
            return JsonResponse(movie_obj.response(), status=200, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 404, 'error': 'DoesNotExist'}, status=404, safe=False)

    def post(self, request, *args, **kwargs):
        req_body = get_request_body(request)
        try:
            new_movie = add_movie(req_body)
        except MovieAlreadyExists as err:
            return JsonResponse({'error': err.message, 'status': err.status_code}, status=err.status_code, safe=False)
        return JsonResponse(
            {'status': 'Success', 'movie_id': new_movie.id, 'title': new_movie.title}, status=200, safe=False)

    def patch(self, request, *args, **kwargs):
        movieid = kwargs.get('movieid')
        try:
            movie_obj = MovieApp(movieid)
            update_data = get_request_body(request)
            movie_obj.update(update_data)
            return JsonResponse(movie_obj.response(), status=200, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 404, 'error': 'DoesNotExist'}, status=404, safe=False)
        except MovieAlreadyExists as err:
            return JsonResponse({'error': err.message, 'status': err.status_code}, status=err.status_code, safe=False)

    def delete(self, request, *args, **kwargs):
        req_body = get_request_body(request)
        movieid = kwargs.get('movieid') or req_body.get('movieid')
        try:
            movie_obj = MovieApp(movieid)
            movie_obj.movie.delete()
            return JsonResponse({'status': 'Success', 'message': 'Successfully Deleted'}, status=200, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 404, 'error': 'DoesNotExist'}, status=404, safe=False)


