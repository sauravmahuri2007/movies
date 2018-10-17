# -*- coding: utf-8 -*-

"""
Configuration file for movie.
Please make sure that all config variables should be declared here.
"""

MOVIE_BASIC_AUTH = {
    'username': 'MOVIE_U$ER',
    'password': '0f196474b35837546b9012702705af5ed22a0ab9'  # This is a SHA1 hashed password for security reasons
}

JWT_EXPIRY_TIME = 60 * 60 * 24  # 24 Hours in seconds
JWT_SECRET = 'T[-]IsSecretN3v3RExp0s^'
JWT_ALGORITHM = 'HS256'

GUEST_USER = 'guest_user'