"""
API Authorization Mixin and other utilities
"""

from config import movieconf
from moviexceptions.generic import APIAuthorizationException

from django.http import JsonResponse
from django.views.generic import View


class APIAuthorizationMixin(View):
    """
    Include this mixin in the views where we want role and permission based API calls.
    For the APIs (URL), their method and the permissions refer URL_PERMISSIONS in config.movieconf.py file
    """

    def check_authorization(self, request):
        payload = getattr(request, 'payload', {})
        user_permissions = payload.get('permissions', [])
        url_name = request.resolver_match.url_name
        method = request.method
        url_permissions = movieconf.URL_PERMISSIONS.get(url_name, {}).get(method, None)
        if url_permissions is None:
            # Allowing the request if the permissions for URL is not defined
            return False
        # Check if at least one permission matched
        permission_match = [permission for permission in url_permissions if permission in user_permissions]
        # If the permission_match is empty then not even one user permission is
        # in the allowed permissions list for this URL. Return 403, Forbidden ASAP
        if not len(permission_match):
            msg = "'{0}' is unauthorized to access '{1}' API for '{2}' method call".format(
                request.username, request.path, method)
            raise APIAuthorizationException(msg, 403)
        return True

    def dispatch(self, request, *args, **kwargs):
        try:
            # Ignore if request's method is GET and user is movieconf.GUEST_USER
            if getattr(request, 'username', None) != movieconf.GUEST_USER:
                self.check_authorization(request)
        except APIAuthorizationException as err:
            response = {
                'status': err.status_code,
                'message': err.message
            }
            return JsonResponse(response, status=err.status_code, safe=False)
        return super(APIAuthorizationMixin, self).dispatch(request, *args, **kwargs)