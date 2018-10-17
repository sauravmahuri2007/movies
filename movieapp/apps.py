# -*- coding: utf-8 -*-

"""
Class based implementation of the Movie so that all the functionality related to
a single movie can be handled by a single object.
"""

from django.apps import AppConfig

from .models import Movie, Cast
from moviexceptions.generic import MovieAlreadyExists
from utils.movieutils import get_or_create_genre, get_or_create_person

class MovieappConfig(AppConfig):
    name = 'movieapp'


class MovieApp(object):
    """
    A class to wrap all movie related functionality like search, add, edit movies their casts etc.
    """

    def __init__(self, movieid):
        self.movie = Movie.objects.get(id=movieid)  # It may raise ObjectDoesNotExist if movieid doesn't exist
        self.casts = Cast.objects.filter(movie_id=movieid)

    def response(self):
        """
        Builds a dictionary having complete information about the movie, genres, casts etc.
        :return: a dictionary.
        """
        resp = {
            'movie_id': self.movie.id,
            'name': self.movie.title,
            'imdb_score': float(self.movie.rating),
            'director': self.movie.director.name,
            'release_date': str(self.movie.release_date),
            'run_time': self.movie.run_time,
            'plot': self.movie.plot,
            'genres': [genre.title for genre in self.movie.genres.all()],
            'casts': [{'name': cast.person_id.name, 'person_id': cast.person_id.id} for cast in self.casts],
        }
        return resp

    def update(self, update_data):
        """
        Update the movie object and the related fields
        :param update_data: movie data to update
        :return: None
        """
        # check if there exists a another movie with same title and director for update_data's title and director
        title = update_data.get('name')
        director_name = update_data.get('director')
        existing_movies = Movie.objects.filter(
            title__iexact=title, director__name__iexact=director_name).exclude(id=self.movie.id)
        if existing_movies:
            # There exists another movie with same title and director name
            raise MovieAlreadyExists(
                '"{0}" directed by "{1}" can not be updated as another copy already exists'.format(
                    title, director_name), 409)
        self.movie.release_date = update_data.get('release_date') or self.movie.release_date
        self.movie.rating = update_data.get('imdb_score') or self.movie.rating
        self.movie.run_time = update_data.get('run_time') or self.movie.run_time
        self.movie.title = update_data.get('name') or self.movie.title
        self.movie.plot = update_data.get('plot') or self.movie.plot
        self.movie.director = update_data.get('director') and \
                              get_or_create_person(update_data.get('director'))[0] or self.movie.director
        genres = update_data.get('genre')
        if genres and isinstance(genres, list):
            # 1st delete the existing genres in movie object
            [self.movie.genres.remove(genre) for genre in self.movie.genres.all()]
            # and then add the new genres provided in the update_data
            for genre in genres:
                genre_obj, is_created = get_or_create_genre(str(genre).strip())
                self.movie.genres.add(genre_obj)




