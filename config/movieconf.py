# -*- coding: utf-8 -*-

"""
Configuration file for movie.
Please make sure that all config variables should be declared here.
"""

# Make sure to give the password as SHA1 hashed.
# To generate a SHA1 hash password, refer get_hash() function in utils.movieutils.
MOVIE_USERS = {
    'admin': {
        'password': 'fda3bd2f7686a850c37f91c5f8e28e16e702407f',
        'permissions': ['view_movie', 'add_movie', 'delete_movie', 'update_movie']
    },
    'associate': {
        'password': '13be887b57481d3e4d0c20b879ff95c5cb976e2c',
        'permissions': ['view_movie', 'update_movie']
    },
}

# Make sure to give only the URL name as the key here:
# For example name='movie'. Check movieapp.urls.py for the name of the URLs
URL_PERMISSIONS = {
    'movie': {
        'GET': ['view_movie'],  # i,e Movie's GET API requires 'view_movie' permission
        'POST': ['add_movie'],  # similarly, POST API to add a movie requires 'add_movie' permission
        'PATCH': ['update_movie'],
        'DELETE': ['delete_movie'],
    },
}

API_VALIDATION_RULES = {
    'movie': {
        'DELETE': {
            'movieid': ['required', 'integer'], # Make sure there exists a staticmethod
            # for given validation in Validators class. Check Validators class in utils.validation
        },
        'POST': {
            'name': ['required', 'string'],
            'director': ['required', 'string'],
        },
        'PATCH': {
            'movieid': ['required', 'integer'],
        },
    }
}

JWT_EXPIRY_TIME = 60 * 60 * 24  # 24 Hours in seconds
JWT_SECRET = 'T[-]IsSecretN3v3RExp0s^'
JWT_ALGORITHM = 'HS256'

GUEST_USER = 'guest_user'