"""
Request Validation Mixin and Utilities
"""

from config import movieconf
from moviexceptions.generic import RequestValidationException
from utils.movieutils import get_request_body

from django.http import JsonResponse
from django.views.generic import View


class Validators(object):
    """
    contains the static method which can be called with the value to validate.
    Returns the error message or True if success.
    """

    @staticmethod
    def required(req_body, field):
        if field not in req_body.keys():
            return '`{0}` field is required'.format(field)
        return None

    @staticmethod
    def integer(req_body, field):
        value = req_body.get(field)
        try:
            value = int(value)
        except TypeError:
            return '`{0}` field must be an integer type'.format(field)
        return None

    @staticmethod
    def string(req_body, field):
        value = req_body.get(field)
        if not isinstance(value, str):
            return '`{0}` field must be a string type'.format(field)
        return None


class RequestValidationMixin(View):
    """
    Include this mixin in the views where we want role and permission based API calls.
    For the APIs (URL), their method and the permissions refer URL_PERMISSIONS in config.movieconf.py file
    """

    def request_validate(self, request):
        """
        Validates for each request body and the method as per the request validation config map
        :param request: HTTP Request object
        :return: True if all all went fine else raises RequestValidationException if any errors occurs
        """
        try:
            req_body = get_request_body(request)
        except ValueError:
            raise RequestValidationException('Does not look like a valid JSON request', 400)
        errors = []
        url_name = request.resolver_match.url_name  # eg: 'search', 'movie'
        api_map = movieconf.API_VALIDATION_RULES.get(url_name, {}).get(request.method, {})
        for field, rules in api_map.items():
            for rule in rules:
                # Getting the method from Validators class and calling it with the value to validate
                validation_error = getattr(Validators, rule)(req_body, field)
                if validation_error:
                    errors.append(validation_error.format(field))
        if len(errors) > 0:
            raise RequestValidationException('; '.join(errors), 400)
        return True

    def dispatch(self, request, *args, **kwargs):
        try:
            self.request_validate(request)
        except RequestValidationException as err:
            response = {
                'status': err.status_code,
                'message': err.message
            }
            return JsonResponse(response, status=err.status_code, safe=False)
        return super(RequestValidationMixin, self).dispatch(request, *args, **kwargs)