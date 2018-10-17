# -*- coding: utf-8 -*-

"""
General Exception Classes for Movie
"""

class BasicAuthException(Exception):

    def __init__(self, *details):
        self.message = details and details[0] or 'Basic Authentication Failed!'
        try:
            self.status_code = details and details[1] or 401
        except IndexError:
            self.status_code = 401

    def __str__(self):
        return '< %s - %s >' % (self.status_code, self.message)


class JWTAuthException(Exception):

    def __init__(self, *details):
        self.message = details and details[0] or 'JWT Based Authentication Failed!'
        try:
            self.status_code = details and details[1] or 401
        except IndexError:
            self.status_code = 401

    def __str__(self):
        return '< %s - %s >' % (self.status_code, self.message)


class MovieAlreadyExists(Exception):
    """
    Raise this exception while creating the movie object and it already exists.
    This is how you'll raise this exception:
    raise MovieAlreadyExists('Movie with title "Lords of the Rings" already exists in our DB', 409)
    """
    def __init__(self, *details):
        self.message = details and details[0] or 'Already Exists!'
        try:
            self.status_code = details and details[1] or 409
        except IndexError:
            self.status_code = 409

        def __str__(self):
            return '< %s - %s >' % (self.status_code, self.message)


class APIAuthorizationException(Exception):
    """
    Raise this exception when the API is not authorized to access due to permissions issues.
    This is how you'll raise this exception:
    raise APIAuthorizationException('"url" API with request method "POST" is unauthorized', 403)
    """

    def __init__(self, *details):
        self.message = details and details[0] or 'Request Forbidden'
        try:
            self.status_code = details and details[1] or 403
        except IndexError:
            self.status_code = 403

        def __str__(self):
            return '< %s - %s >' % (self.status_code, self.message)


class RequestValidationException(Exception):
    """
    Raise this exception when the request doesn't contain a valid data or body.
    This is how you'll raise this exception:
    raise RequestValidationException('Request Validation Errors', 400)
    """

    def __init__(self, *details):
        self.message = details and details[0] or 'Invalid Request Body'
        try:
            self.status_code = details and details[1] or 400
        except IndexError:
            self.status_code = 400

        def __str__(self):
            return '< %s - %s >' % (self.status_code, self.message)