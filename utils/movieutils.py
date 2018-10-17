# -*- coding: utf-8 -*-

"""
General Movies Utilities, Functions and Helper Functions.
"""

import hashlib
import json

from django.db import transaction
from django.contrib.auth.models import User
from django.utils.timezone import now

from moviexceptions.generic import MovieAlreadyExists
from movieapp.models import Movie, Person, Role, Genre


def get_or_create_person(director):
    """
    For passed director name check if the Person object exists.
    If doesn't exist create a Role object with title 'director' then create the Person object with role the same role
    Note: In case of multiple Person objects found with same director name, it selects the 1st Person always
    :param director: name of the director
    :return: Person model object, True/False
    """
    persons = Person.objects.filter(name__iexact=director)  # case-insensitive exact match of the director's name
    if len(persons) >= 1:
        return persons[0], False
    # No Person object found! Create a Person with Role as 'director'
    with transaction.atomic():
        role, is_created = Role.objects.get_or_create(title='director')
        person = Person.objects.create(name=director)
        person.roles.add(role)
        person.save()
    return person, True


def get_or_create_genre(genre_title):
    """
    For passed genre_title get the genre object or create a genre if not exists
    :param genre_title: name of the genre like 'Fantasy', 'Sci-Fi', 'Drama', 'Romance' etc
    :return: genre_obj, True/False
    """
    genres = Genre.objects.filter(title__iexact=genre_title)
    if len(genres) >= 1:
        return genres[0], False
    return Genre.objects.create(title=genre_title), True


def add_movie(req_body):
    """
    Adds a Movie to the DB. Also checks whether the movie with the same title and director already exists.
    :param req_body: dictionary of the movie details which was received as JSON request.
    :return: Movie model object if successfully created a Movie or raise MovieAlreadyExists otherwise.
    """
    title = req_body.get('name')
    director = req_body.get('director')
    if Movie.objects.filter(title__iexact=title, director__name__iexact=director).exists():
        # Movie instance with same title and director's name already exists!
        raise MovieAlreadyExists('"{0}" directed by "{1}" already exists!'.format(req_body.get('name'), director), 409)
    # Everything is fine! Create a Movie instance
    person, is_created = get_or_create_person(req_body.get('director'))  # Returns a Person model object
    author = User.objects.get(id=1)
    rating = req_body.get('imdb_score')
    release_date = req_body.get('release_date')
    plot = req_body.get('plot')
    run_time = req_body.get('run_time')
    genres = req_body.get('genre')  # expecting a list of genre string
    with transaction.atomic():
        movie = Movie.objects.create(
            title=title, director=person, author=author, rating=rating, release_date=release_date, plot=plot,
            run_time=run_time)
        if genres and isinstance(genres, list):
            for genre in genres:
                genre_obj, is_created = get_or_create_genre(str(genre).strip())
                movie.genres.add(genre_obj)
    return movie


def search_movie(search_params):
    """
    Filter out the necessary fields as per Movie model in search_params and searches the movies in DB
    :param search_params: a dictionary of Movie attributes
    :return: List of dictionary
    """
    if not search_params or not isinstance(search_params, dict):
        return []
    qs = Movie.objects.filter(created_dtm__lte=now())  # initial query-set with all movies created before current date
    for key, value in search_params.items():
        key_lower = key.lower()
        if key_lower in ('name', 'title'):
            qs = qs.filter(title__icontains=value)
        elif key_lower in ('imdb_score', 'rating'):
            qs = qs.filter(rating__lte=value)
        elif key_lower == 'director':
            qs = qs.filter(director__name__iexact=value)
        elif key_lower == 'release_date':
            qs = qs.filter(release_date=value)
        elif key_lower == 'genre':
            if isinstance(value, list):
                qs = qs.filter(genres__title__in=value)
            elif isinstance(value, str):
                qs = qs.filter(genres__title=value)
    qs = qs.order_by('id')
    result = [get_movie_response(movie) for movie in qs]
    return result


def get_movie_response(movie, **kwargs):
    resp = {
        'movie_id': movie.id,
        'name': movie.title,
        'imdb_score': float(movie.rating),
        'director': movie.director.name,
        'release_date': str(movie.release_date),
        'run_time': movie.run_time,
        'plot': movie.plot,
        'genres': [genre.title for genre in movie.genres.all()],
    }
    casts = kwargs.get('casts')
    if casts:
        resp['casts'] = [{'name': cast.person_id.name, 'person_id': cast.person_id.id} for cast in casts]
    return resp


def get_request_body(request):
    """
    A generic implementation to get the request body irrespective of the RESTful APIs methods.
    """

    method = request.method
    if method == 'DELETE':
        body = request.resolver_match.kwargs
    elif method == 'GET':
        body = request.GET.copy()
    elif method == 'POST':
        try:
            body = request.POST.copy() or request.body and json.loads(request.body)
        except TypeError:
            # Supporting Python3: everything is bytes even request.body.
            body = request.body and json.loads(request.body.decode('utf-8'))
    else:
        # For other methods like PUT, PATCH etc..
        try:
            body = json.loads(request.body)
        except TypeError:
            # Supporting Python3: everything is bytes even request.body.
            body = json.loads(request.body.decode('utf-8'))
    return body


def get_hash(string):
    """
    Just returns the SHA1 hash of the string. Usually used to do the password match
    :param string: any string. Usually the password string
    :return: hash of the string
    """
    byte_string = string.encode('utf-8')
    return hashlib.sha1(byte_string).hexdigest()